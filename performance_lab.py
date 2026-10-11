import time
import random

# 🔍 Problem 1: Find Most Frequent Element
# Given a list of integers, return the value that appears most frequently.
# If there's a tie, return any of the most frequent.
#
# Example:
# Input: [1, 3, 2, 3, 4, 1, 3]
# Output: 3

def most_frequent(numbers):
    if not numbers:
        return None
    counts = {}
    best_value = numbers[0]
    best_count = 0
    for num in numbers:
        counts[num] = counts.get(num, 0) + 1
        if counts[num] > best_count:
            best_count = counts[num]
            best_value = num
    return best_value

"""
Time and Space Analysis for problem 1:
- Best-case: O(n) - every element must be counted at least once.
- Worst-case: O(n) - one pass; dict get/set is O(1) on average.
- Average-case: O(n)
- Space complexity: O(k), k = number of distinct values (O(n) if all unique).
- Why this approach? A hash map counts in a single pass and tracks the best
  value as it goes. Calling list.count() for every element would be O(n^2).
- Could it be optimized? Time is already optimal (must read every element).
  Boyer-Moore voting uses O(1) space but only works if a majority element
  (> n/2) is guaranteed.
"""


# 🔍 Problem 2: Remove Duplicates While Preserving Order
# Write a function that returns a list with duplicates removed but preserves order.
#
# Example:
# Input: [4, 5, 4, 6, 5, 7]
# Output: [4, 5, 6, 7]

def remove_duplicates(nums):
    seen = set()
    result = []
    for num in nums:
        if num not in seen:
            seen.add(num)
            result.append(num)
    return result

"""
Time and Space Analysis for problem 2:
- Best-case: O(n) - every element must still be inspected.
- Worst-case: O(n) - set membership and add are O(1) on average.
- Average-case: O(n)
- Space complexity: O(n) - the seen set plus the result list.
- Why this approach? The set gives O(1) "seen it?" checks, and the result
  list preserves first-occurrence order. Using `num in result` (a list) would
  be O(n) per check and O(n^2) overall.
- Could it be optimized? Time is already optimal. list(dict.fromkeys(nums))
  is a shorter O(n) alternative (Python 3.7+). Trade-off: less explicit and
  relies on dict ordering.
"""


# 🔍 Problem 3: Return All Pairs That Sum to Target
# Write a function that returns all unique pairs of numbers in the list that sum to a target.
# Order of output does not matter. Assume input list has no duplicates.
#
# Example:
# Input: ([1, 2, 3, 4], target=5)
# Output: [(1, 4), (2, 3)]

def find_pairs_brute_force(nums, target):
    """ORIGINAL solution: check every pair."""
    pairs = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                pairs.append((nums[i], nums[j]))
    return pairs


def find_pairs(nums, target):
    """
    OPTIMIZED solution (refactored from find_pairs_brute_force).

    Optimization: the original compared every pair of elements (nested loops,
    O(n^2) time, O(1) extra space). This version makes a single pass and
    stores seen numbers in a set. For each number, it checks in O(1) whether
    its complement (target - num) was already seen. This trades O(n) extra
    memory for dropping time from O(n^2) to O(n).
    """
    seen = set()
    pairs = []
    for num in nums:
        complement = target - num
        if complement in seen:
            pairs.append((complement, num))
        seen.add(num)
    return pairs

"""
Time and Space Analysis for problem 3 (optimized version):
- Best-case: O(n) - still one full pass even if no pairs exist.
- Worst-case: O(n) - set lookups/inserts are O(1) on average.
- Average-case: O(n)
- Space complexity: O(n) for the seen set, plus O(p) for the output pairs.
- Why this approach? Brute force is O(n^2) time with O(1) space. The set
  approach is O(n) time with O(n) space, which scales far better.
- Could it be optimized? Time is optimal for unsorted input (must read every
  element). Alternative: sort + two pointers gives O(n log n) time and O(1)
  extra space (ignoring output and sort internals).
- Trade-offs: hash set = fastest but uses extra memory. Two pointers = less
  memory but slower (sorting) and reorders the data.

Performance comparison (original vs. optimized):
- Brute force: O(n^2) time, O(1) extra space.
- Set-based:   O(n) time,   O(n) extra space.
- Benchmark results (my machine):
  n = 1000:  brute force 0.0237 s  |  optimized 0.000096 s
  n = 2000:  brute force 0.0529 s  |  optimized 0.000191 s
  n = 5000:  brute force 0.3622 s  |  optimized 0.000469 s
  At n = 5000 the optimized version is about 770x faster. Brute force growth
  is roughly quadratic (n went 2.5x from 2000 to 5000, time went ~6.8x);
  optimized growth is roughly linear (~2.5x).
"""


# 🔍 Problem 4: Simulate List Resizing (Amortized Cost)
# Create a function that adds n elements to a list that has a fixed initial capacity.
# When the list reaches capacity, simulate doubling its size by creating a new list
# and copying all values over (simulate this with print statements).
#
# Example:
# add_n_items(6) → should print when resizing happens.

def add_n_items(n, initial_capacity=2):
    """Adds n items to a fixed-capacity array, doubling when full.
    Returns the total number of element copies made during resizes."""
    capacity = max(1, initial_capacity)
    storage = [None] * capacity
    size = 0
    total_copies = 0

    for i in range(n):
        if size == capacity:
            new_capacity = capacity * 2
            print(f"Resize at item {i + 1}: capacity {capacity} -> {new_capacity}, "
                  f"copying {size} items")
            new_storage = [None] * new_capacity
            for j in range(size):
                new_storage[j] = storage[j]
            storage = new_storage
            capacity = new_capacity
            total_copies += size
        storage[size] = i
        size += 1

    return total_copies

"""
Time and Space Analysis for problem 4:
- When do resizes happen? When the array is full and a new item arrives:
  at initial_capacity * 2^k items (capacity 2: adding the 3rd, 5th, 9th,
  17th... items).
- What is the worst-case for a single append? O(n) - the append that triggers
  a resize copies all n existing elements.
- What is the amortized time per append overall? O(1). Total copies for n
  appends are at most 1 + 2 + 4 + ... + n/2 < n, so O(n) total work across
  n appends.
- Space complexity: O(n) - capacity is at most 2n. During a resize, the old
  and new arrays briefly coexist.
- Why does doubling reduce the cost overall? Resizes get exponentially rarer
  as the array grows, so the expensive copies are spread over many cheap
  appends. Growing by a constant amount would resize far more often and give
  O(n) amortized cost per append.
"""


# 🔍 Problem 5: Compute Running Totals
# Write a function that takes a list of numbers and returns a new list
# where each element is the sum of all elements up to that index.
#
# Example:
# Input: [1, 2, 3, 4]
# Output: [1, 3, 6, 10]
# Because: [1, 1+2, 1+2+3, 1+2+3+4]

def running_total(nums):
    result = []
    total = 0
    for num in nums:
        total += num
        result.append(total)
    return result

"""
Time and Space Analysis for problem 5:
- Best-case: O(n) - every element must be read (empty list is O(1)).
- Worst-case: O(n)
- Average-case: O(n)
- Space complexity: O(n) for the output list; O(1) auxiliary (just `total`).
- Why this approach? Each element is added once to a running sum. Recomputing
  sum(nums[:i+1]) at every index would be O(n^2).
- Could it be optimized? Time is already optimal. itertools.accumulate is
  faster in practice (runs in C). Doing it in place gives O(1) extra space,
  but destroys the original data.
"""


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_most_frequent():
    assert most_frequent([1, 3, 2, 3, 4, 1, 3]) == 3
    assert most_frequent([]) is None
    assert most_frequent([7]) == 7
    assert most_frequent([5, 5, 5, 5]) == 5
    assert most_frequent([1, 2, 1, 2]) in (1, 2)           # tie
    assert most_frequent([-1, -1, 2]) == -1                # negatives
    assert most_frequent([0, 0, 1]) == 0                   # zero
    print("Problem 1 tests passed")


def test_remove_duplicates():
    assert remove_duplicates([4, 5, 4, 6, 5, 7]) == [4, 5, 6, 7]
    assert remove_duplicates([]) == []
    assert remove_duplicates([1]) == [1]
    assert remove_duplicates([2, 2, 2, 2]) == [2]
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3]       # already unique
    assert remove_duplicates([3, 1, 3, 2, 1]) == [3, 1, 2] # order preserved
    print("Problem 2 tests passed")


def test_find_pairs():
    for fn in (find_pairs_brute_force, find_pairs):
        assert sorted(sorted(p) for p in fn([1, 2, 3, 4], 5)) == [[1, 4], [2, 3]]
        assert fn([], 5) == []
        assert fn([3], 6) == []
        assert fn([1, 2, 3], 100) == []
        assert sorted(sorted(p) for p in fn([-1, 1, 0, 2], 1)) == [[-1, 2], [0, 1]]
        assert sorted(sorted(p) for p in fn([0, 5], 5)) == [[0, 5]]
    print("Problem 3 tests passed")


def test_add_n_items():
    assert add_n_items(0) == 0                             # nothing to add
    assert add_n_items(2) == 0                             # fits, no resize
    assert add_n_items(3) == 2                             # one resize (copy 2)
    assert add_n_items(6) == 2 + 4                         # resizes at 3rd, 5th
    assert add_n_items(100) < 2 * 100                      # amortized O(1)
    assert add_n_items(5, initial_capacity=0) >= 0         # bad capacity guarded
    print("Problem 4 tests passed")


def test_running_total():
    assert running_total([1, 2, 3, 4]) == [1, 3, 6, 10]
    assert running_total([]) == []
    assert running_total([5]) == [5]
    assert running_total([-1, -2, -3]) == [-1, -3, -6]     # negatives
    assert running_total([0, 0, 0]) == [0, 0, 0]
    assert running_total([5, -5, 5]) == [5, 0, 5]
    nums = [1, 2, 3]
    running_total(nums)
    assert nums == [1, 2, 3]                               # input not mutated
    print("Problem 5 tests passed")


def benchmark_find_pairs():
    print("\nBenchmark: find_pairs_brute_force vs. find_pairs (optimized)")
    for n in (1000, 2000, 5000):
        nums = random.sample(range(n * 10), n)
        target = n * 5

        start = time.perf_counter()
        slow = find_pairs_brute_force(nums, target)
        slow_time = time.perf_counter() - start

        start = time.perf_counter()
        fast = find_pairs(nums, target)
        fast_time = time.perf_counter() - start

        assert sorted(sorted(p) for p in slow) == sorted(sorted(p) for p in fast)
        print(f"n={n:>5}: brute force {slow_time:.4f}s | optimized {fast_time:.6f}s")

if __name__ == "__main__":
    test_most_frequent()
    test_remove_duplicates()
    test_find_pairs()
    print("\nProblem 4 demo (add_n_items(6)):")
    add_n_items(6)
    test_add_n_items()
    test_running_total()

    benchmark_find_pairs()