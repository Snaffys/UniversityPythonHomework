def is_pos_safe(queen_positions, new_pos):
    for q_pos in queen_positions:
        # Diagonal attack occurs when |row1 - row2| == |col1 - col2|
        if abs(q_pos[0] - new_pos[0]) == abs(q_pos[1] - new_pos[1]):
            return False
    return True


def recursive_n_queens(n, row=0, queen_positions=None, used_cols=None):
    if queen_positions is None:
        queen_positions = []
    if used_cols is None:
        used_cols = set()

    if row == n:
        return 1

    solutions_count = 0

    for col in range(n):
        if col in used_cols:
            continue

        if is_pos_safe(queen_positions, [row, col]):
            queen_positions.append([row, col])
            used_cols.add(col)

            solutions_count += recursive_n_queens(n, row + 1, queen_positions, used_cols)

            # Backtrack
            queen_positions.pop()
            used_cols.remove(col)

    return solutions_count


def main():
    BOARD_SIZE = 8
    print("result:")
    print(recursive_n_queens(BOARD_SIZE))


if __name__ == "__main__":
    main()

