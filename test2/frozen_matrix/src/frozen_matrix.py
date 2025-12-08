class FrozenMatrix:
    def __init__(self, data):
        if not data:
            raise ValueError("Matrix is empty")

        matrix = []
        for row in data:
            matrix.append(tuple(row))
        self.data = tuple(matrix)
        if self.data:
            cols = len(self.data[0])
            for row in self.data:
                if len(row) != cols:
                    raise ValueError("Rows have length")
        
        self.hash_value = None
    
    def __eq__(self, other):
        if not isinstance(other, FrozenMatrix):
            return False
        return self.data == other.data
    
    def __hash__(self):
        if self.hash_value is None:
            self.hash_value = hash(self.data)
        return self.hash_value
    
    def __str__(self):
        rows = []
        for row in self.data:
            row_str = ", ".join(str(element) for element in row)
            rows.append(f"[{row_str}]")        
        return "[" + ", ".join(rows) + "]"


if __name__ == "__main__":
    print("SET")

    matrix_set = {
        FrozenMatrix([[1, 2], [3, 4]]),
        FrozenMatrix([[5, 6], [7, 8]])
    }
    
    print(f"Set consists of {len(matrix_set)} elements")
    print("Elements:")
    for matrix in matrix_set:
        print(f"{matrix}")
    
    print("\nDICT")
    matrix_dict = {
        FrozenMatrix([[1, 2], [3, 4]]): "first_value",
        FrozenMatrix([[5, 6], [7, 8]]): "second_value"
    }
    
    for matrix, value in matrix_dict.items():
        print(f"Key: {matrix}    Value: '{value}'")
    

    m1 = FrozenMatrix([[1, 2], [3, 4]])
    print(f"matrix_dict[m1] = '{matrix_dict[m1]}'")
