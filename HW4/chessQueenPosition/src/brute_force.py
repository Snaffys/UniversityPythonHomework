import itertools


def check_diagonal_attacks(queen_positions):
    for i in range(len(queen_positions) - 1):
        for j in range(i + 1, len(queen_positions)):
            # Diagonal attack occurs when |row1 - row2| == |col1 - col2|
            if abs(queen_positions[i][0] - queen_positions[j][0]) == abs(queen_positions[i][1] - queen_positions[j][1]):
                return False
    return True


def brute_force_n_queens(n):
    solutions_count = 0
    # Generate all collumn non-repeating permutations (queens will be in different rows anyway)
    all_col_permutations = itertools.permutations(range(n))

    for col_positions in all_col_permutations:
        # Assign rows to each column and put results in the list
        queen_positions = list(enumerate(col_positions))
        if check_diagonal_attacks(queen_positions):
            solutions_count += 1

    return solutions_count


def main():
    BOARD_SIZE = 8
    print("result:")
    print(brute_force_n_queens(BOARD_SIZE))


if __name__ == "__main__":
    main()

