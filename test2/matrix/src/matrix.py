class Matrix:
    def __init__(self, data):
        if not data:
            raise ValueError("Matrix is empty")

        first_row_length = len(data[0])
        all_same_length = True
        for row in data:
            if len(row) != first_row_length:
                all_same_length = False
                break
        if not all_same_length:
            raise ValueError("Rows have different length")

        self.data = [row[:] for row in data]
        self.rows = len(data)
        self.cols = first_row_length

    def __getitem__(self, key):
        i, j = key
        return self.data[i][j]

    def __iter__(self):
        for row in self.data:
            for element in row:
                yield element

    def __str__(self):
        result = []
        for row in self.data:
            row_str = " ".join(str(element) for element in row)
            result.append(row_str)
        return "\n".join(result)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result_matrix = []
            for i in range(self.rows):
                new_row = []
                for j in range(self.cols):
                    original_element = self[i, j]
                    multiplied_element = original_element * other
                    new_row.append(multiplied_element)
                result_matrix.append(new_row)
            return Matrix(result_matrix)
        elif isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError("Matrices can't be multiplied")
            result_matrix = []
            for i in range(self.rows):
                new_row = []
                for j in range(other.cols):
                    elements_mul = 0
                    for k in range(self.cols):
                        first_element = self[i, k]
                        second_element = other[k, j]
                        elements_mul += first_element * second_element
                    new_row.append(elements_mul)
                result_matrix.append(new_row)
            return Matrix(result_matrix)
        else:
            raise TypeError("Can't be multiplied")

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Can't be added to")

        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices should be the same size")

        result = []
        for i in range(self.rows):
            current_row = []
            for j in range(self.cols):
                first_element = self[i, j]
                second_element = other[i, j]
                sum_element = first_element + second_element
                current_row.append(sum_element)
            result.append(current_row)
        return Matrix(result)

    def determinant(self, matrix):
        if self.rows != self.cols:
            raise ValueError("Size of rows is not equal to size of cols")

        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        if n == 3:
            a, b, c = matrix[0]
            d, e, f = matrix[1]
            g, h, i = matrix[2]
            return (a * e * i + b * f * g + c * d * h) - (
                c * e * g + b * d * i + a * f * h
            )

        det = 0
        for j in range(n):
            minor = []
            for row_index in range(1, n):
                new_row = []
                for col_index in range(n):
                    if col_index != j:
                        new_row.append(matrix[row_index][col_index])
                minor.append(new_row)

            minor_det = self.determinant(minor)

            if j % 2 == 0:
                sign = 1
            else:
                sign = -1

            det += sign * matrix[0][j] * minor_det

        return det

    def to_mtx(self):
        not_null = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.data[i][j] != 0:
                    not_null += 1

        lines = ["%%MatrixMarket matrix coordinate real general"]
        lines.append(f"{self.rows} {self.cols} {not_null}")

        for i in range(self.rows):
            for j in range(self.cols):
                value = self.data[i][j]
                if value != 0:
                    lines.append(f"{i + 1} {j + 1} {value}")

        return "\n".join(lines)

    def from_mtx(self, mtx_string):
        lines = mtx_string.strip().split("\n")

        data_line_index = 0
        for i, line in enumerate(lines):
            if not line.startswith("%"):
                data_line_index = i
                break

        size_line = lines[data_line_index]
        rows, cols, not_null = map(int, size_line.split())

        matrix_data = [[0.0] * cols for _ in range(rows)]

        for i in range(data_line_index + 1, data_line_index + 1 + not_null):
            if i < len(lines):
                parts = lines[i].strip().split()
                if len(parts) >= 3:
                    row_idx = int(parts[0]) - 1
                    col_idx = int(parts[1]) - 1
                    value = float(parts[2])

                    if 0 <= row_idx < rows and 0 <= col_idx < cols:
                        matrix_data[row_idx][col_idx] = value

        return Matrix(matrix_data)


def main():
    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[5, 6], [7, 8]])

    print("Matrix A:")
    print(A)
    print("\nMatrix B:")
    print(B)

    print("\nA + B:")
    print(A + B)

    print("\nA * 10:")
    print(A * 10)

    print("\nA * B:")
    print(A * B)

    print("\nMatrix A iteration:")
    for elem in A:
        print(elem, end=" ")

    print("\n\nMatrix A determinant:")
    det = A.determinant(A.data)
    print(det)

    print("\nMTX")
    C = Matrix(
        [
            [1.0, 0.0, 0.0, 5.0],
            [0.0, 2.0, 3.0, 0.0],
            [0.0, 3.0, 4.0, 0.0],
            [0.0, 0.0, 0.0, 6.0],
        ]
    )

    print("\nMatrix C:")
    print(C)

    mtx_data = C.to_mtx()
    print("\nSerialized:")
    print(mtx_data)

    restored_matrix = C.from_mtx(mtx_data)
    print("\nDeserialized:")
    print(restored_matrix)


if __name__ == "__main__":
    main()
