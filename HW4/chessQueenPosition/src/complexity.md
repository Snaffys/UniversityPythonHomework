# Оценка сложности / Complexity analysis

## 1. Переборное решение / Brute-force solution

Сложность: O(N! * N^2)
Обоснование: N! перестановок * O(N^2) проверка корректности всех пар ферзей (N(N-1)/2 сравнений)

Complexity: O(N! * N^2)
Explanation: N! permutations * O(N^2) validity check of all queen pairs (N(N-1)/2 comparisons)

## 2. Рекурсивное решение / Recursive solution

Сложность: O(N! * N)
Обоснование: N! расстановок * O(N) проверка корректности для каждого нового ферзя

Complexity: O(N! * N)
Explanation: N! configurations * O(N) validity check for each new queen

## 3. Побитовое решение / Bitwise solution

Сложность: O(N!)
Обоснование: N! расстановок * O(1) битовые операции

Complexity: O(N!)
Explanation: N! configurations * O(1) bitwise operations

