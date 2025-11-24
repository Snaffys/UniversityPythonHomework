import heapq


class HuffmanNode:
    def __init__(self, symbol=None, frequency=0):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


def build_huffman_tree(text):
    if not text:
        return None

    frequency = {}
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1

    heap = []
    for char, freq in frequency.items():
        heapq.heappush(heap, HuffmanNode(char, freq))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(frequency=left.frequency + right.frequency)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heapq.heappop(heap) if heap else None


def build_encoding_table(root):
    def traverse(node, code, table):
        if node is None:
            return
        if node.symbol is not None:
            table[node.symbol] = code
            return
        traverse(node.left, code + "0", table)
        traverse(node.right, code + "1", table)

    table = {}
    traverse(root, "", table)

    return table


def encode(msg: str) -> tuple[str, dict[str, str]]:
    if not msg:
        return "", {}

    root = build_huffman_tree(msg)
    table = build_encoding_table(root)
    encoded_text = "".join(table[char] for char in msg)

    return encoded_text, table


def decode(encoded: str, table: dict[str, str]) -> str:
    if not encoded:
        return ""

    code_to_char_table = {code: char for char, code in table.items()}

    decoded_chars = []
    current_code = ""
    for bit in encoded:
        current_code += bit
        if current_code in code_to_char_table:
            decoded_chars.append(code_to_char_table[current_code])
            current_code = ""

    return "".join(decoded_chars)


class BinaryFileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()


def calculate_byte_size(value):
    if value == 0:
        return 1
    return (value.bit_length() + 7) // 8


def serialize_table(table):
    items = []
    for char, code in table.items():
        char_bytes = char.encode("utf-8")
        items.append((char_bytes, code))

    table_data = bytearray()
    num_items = len(items)
    size_bytes = calculate_byte_size(num_items)

    table_data.extend(size_bytes.to_bytes(1, "big"))  # size of number of elements
    table_data.extend(num_items.to_bytes(size_bytes, "big"))  # amount of elements

    for char_bytes, code in items:
        symbol_len_bytes = calculate_byte_size(len(char_bytes))
        table_data.extend(symbol_len_bytes.to_bytes(1, "big"))  # size of length of char
        table_data.extend(
            len(char_bytes).to_bytes(symbol_len_bytes, "big")  # length of char
        )
        table_data.extend(char_bytes)  # char in bytes

        code_len_bytes = calculate_byte_size(len(code))
        table_data.extend(code_len_bytes.to_bytes(1, "big"))  # size of length of code
        table_data.extend(len(code).to_bytes(code_len_bytes, "big"))  # length of code

        code_bytes, code_padding = bits_to_bytes(code)
        table_data.extend(code_padding.to_bytes(1, "big"))  # padding
        table_data.extend(code_bytes)  # code in bytes

    return table_data


def deserialize_table(table_data):
    table = {}
    data = bytearray(table_data)
    index = 0

    size_bytes = int.from_bytes(data[index : index + 1], "big")
    index += 1
    num_entries = int.from_bytes(data[index : index + size_bytes], "big")
    index += size_bytes

    for _ in range(num_entries):
        symbol_len_bytes = int.from_bytes(data[index : index + 1], "big")
        index += 1
        char_len = int.from_bytes(data[index : index + symbol_len_bytes], "big")
        index += symbol_len_bytes

        char_bytes = data[index : index + char_len]
        char = char_bytes.decode("utf-8")
        index += char_len

        code_len_bytes = int.from_bytes(data[index : index + 1], "big")
        index += 1
        code_len = int.from_bytes(data[index : index + code_len_bytes], "big")
        index += code_len_bytes

        code_padding = int.from_bytes(data[index : index + 1], "big")
        index += 1
        code_bytes_len = (code_len + 7) // 8
        code_bytes = data[index : index + code_bytes_len]
        index += code_bytes_len
        code = bytes_to_bits(code_bytes, code_padding)
        code = code[:code_len]

        table[char] = code

    return table


def bits_to_bytes(bit_string):
    if not bit_string:
        return bytearray(), 0

    padding = 8 - (len(bit_string) % 8)
    if padding == 8:
        padding = 0

    bit_string = bit_string + "0" * padding
    bytes_data = bytearray()
    for i in range(0, len(bit_string), 8):
        byte_str = bit_string[i : i + 8]
        bytes_data.append(int(byte_str, 2))

    return bytes_data, padding


def bytes_to_bits(byte_data, padding):
    if not byte_data:
        return ""

    bit_string = ""
    for byte in byte_data:
        bit_string += format(byte, "08b")

    if padding > 0:
        bit_string = bit_string[:-padding]

    return bit_string


def compress_file(input_filepath, output_filepath):
    try:
        with open(input_filepath, "r", encoding="utf-8") as f:
            text = f.read()

        encoded_bits, table = encode(text)
        encoded_bytes, padding = bits_to_bytes(encoded_bits)
        table_bytes = serialize_table(table)

        with BinaryFileManager(output_filepath, "wb") as f:
            table_len = len(table_bytes)
            table_len_size = calculate_byte_size(table_len)
            f.write(table_len_size.to_bytes(1, "big"))
            f.write(table_len.to_bytes(table_len_size, "big"))
            f.write(table_bytes)
            f.write(padding.to_bytes(1, "big"))
            f.write(encoded_bytes)

        print("File was compressed successfully!")

    except Exception as e:
        print(f"Couldn't compress the file: {e}")


def decompress_file(input_filepath, output_filepath):
    try:
        with BinaryFileManager(input_filepath, "rb") as f:
            table_len_size = int.from_bytes(f.read(1), "big")
            table_len = int.from_bytes(f.read(table_len_size), "big")
            table_bytes = f.read(table_len)

            padding = int.from_bytes(f.read(1), "big")

            encoded_bytes = f.read()

        table = deserialize_table(table_bytes)
        encoded_bits = bytes_to_bits(encoded_bytes, padding)
        decoded_text = decode(encoded_bits, table)

        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(decoded_text)

        print("File was decompressed successfully!")

    except Exception as e:
        print(f"Couldn't decompress the file: {e}")


def main():
    test_msg = "Hello world!"
    encoded, table = encode(test_msg)
    decoded = decode(encoded, table)
    print("String test")
    print(f"Original: {test_msg}")
    print(f"Encoded: {encoded}")
    print("Table:")
    for symbol, code in table.items():
        print(f"'{symbol}': {code}")
    print(f"Decoded: {decoded}")
    print(f"Success: {test_msg == decoded}")

    print("\nFile test")
    test_content = "Test file for Huffman coding."
    print(f"Original: {test_content}")
    with open("test_input.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    encoded_bits, file_table = encode(test_content)
    print(f"Encoded: {encoded_bits}")
    print("Table:")
    for symbol, code in file_table.items():
        print(f"'{symbol}': {code}")
    compress_file("test_input.txt", "compressed.huff")
    decompress_file("compressed.huff", "test_output.txt")
    with (
        open("test_input.txt", "r", encoding="utf-8") as f1,
        open("test_output.txt", "r", encoding="utf-8") as f2,
    ):
        original = f1.read()
        decoded = f2.read()
        print(f"Decoded: {decoded}")
        print(f"Success: {original == decoded}")


if __name__ == "__main__":
    main()

