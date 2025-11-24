from hypothesis import given, strategies as strat
from collections import Counter
from src.heap_sort import heap_sort
from src.sorts import python_sorted, quick_sort

SORTING_ALGORITHMS = [heap_sort, python_sorted, quick_sort]


class TestHeapSortProperties:
    @given(strat.lists(strat.integers(), max_size=50))
    def test_heapsort_equals_other_sorts(self, arr):
        heapsort_result = heap_sort(arr.copy())
        for other_sort in [quick_sort, python_sorted]:
            other_result = other_sort(arr.copy())
            assert heapsort_result == other_result

    @given(strat.lists(strat.integers()))
    def test_heapsort_preserves_length(self, arr):
        result = heap_sort(arr.copy())
        assert len(result) == len(arr)

    @given(strat.lists(strat.integers()))
    def test_heapsort_produces_sorted_output(self, arr):
        result = heap_sort(arr.copy())
        for i in range(len(result) - 1):
            assert result[i] <= result[i + 1]

    @given(strat.lists(strat.integers()))
    def test_heapsort_preserves_elements(self, arr):
        result = heap_sort(arr.copy())
        assert Counter(result) == Counter(arr)

    @given(strat.lists(strat.integers(), min_size=2, max_size=20))
    def test_heapsort_with_duplicates(self, arr):
        test_arr = arr + arr.copy()
        heapsort_result = heap_sort(test_arr.copy())
        python_result = python_sorted(test_arr.copy())
        assert heapsort_result == python_result
        
