from src.heap_sort import heap_sort


class TestHeapSort:
    def test_empty_array(self):
        assert heap_sort([]) == []

    def test_single_element(self):
        assert heap_sort([5]) == [5]

    def test_two_elements_unsorted(self):
        assert heap_sort([2, 1]) == [1, 2]

    def test_positive_numbers(self):
        assert heap_sort([4, 2, 8, 1, 3]) == [1, 2, 3, 4, 8]

    def test_negative_numbers(self):
        assert heap_sort([-3, -1, -2, -5]) == [-5, -3, -2, -1]

    def test_mixed_numbers(self):
        assert heap_sort([3, -2, 0, -1, 5]) == [-2, -1, 0, 3, 5]

    def test_duplicate_values(self):
        assert heap_sort([3, 1, 3, 2, 1]) == [1, 1, 2, 3, 3]

    def test_already_sorted(self):
        assert heap_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert heap_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_identical_elements(self):
        assert heap_sort([7, 7, 7, 7]) == [7, 7, 7, 7]
        
