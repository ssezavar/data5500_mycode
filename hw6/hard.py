"""
 Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
 HW6
 --------------------------------------------------------------------
 Hard Q3 — Max difference between ANY two numbers
 Big-O (time): O(n) | Big-O (space): O(1)
 ChatGPT prompts used:
 "Return the maximum difference between any two numbers in an integer array; clarify assumption; add Big-O."
 Assumption: order does NOT matter (not a stock-profit problem).
"""

from typing import Iterable

def max_difference_any(nums: Iterable[int]) -> int:
    it = iter(nums)
    try:
        first = next(it)
    except StopIteration:
        raise ValueError("array must contain at least two elements")
    mn = mx = first
    for x in it:  # O(n)
        if x < mn: mn = x
        if x > mx: mx = x
    return mx - mn

if __name__ == "__main__":
    print(max_difference_any([2, 7, 1, 9, -3]))
    print(max_difference_any([5, 5, 5]))