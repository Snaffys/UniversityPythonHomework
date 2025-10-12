def bitwise_n_queens(n):
    bitmask = (1 << n) - 1

    def count_solutions(row=0, cols=0, ascending_diag=0, descending_diag=0):
        if row == n:
            return 1

        solutions_count = 0

        all_attacks = cols | ascending_diag | descending_diag
        available_positions = ~all_attacks & bitmask  # 1 = available

        while available_positions:
            col_bit = available_positions & -available_positions  # Rightmost available position
            available_positions ^= col_bit

            solutions_count += count_solutions(
                row + 1,
                cols | col_bit,
                (ascending_diag | col_bit) << 1,  # Diagonals shift as we move down
                (descending_diag | col_bit) >> 1,
            )

        return solutions_count

    return count_solutions()


def main():
    BOARD_SIZE = 8
    print("result:")
    print(bitwise_n_queens(BOARD_SIZE))


if __name__ == "__main__":
    main()
