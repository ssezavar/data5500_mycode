"""
 Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
 HW6
--------------------------------------------------------------------
 Easy Q1 — Sum of array
 Big-O (time): O(n) | Big-O (space): O(1)
 ChatGPT prompts used:
 "Given an array of integers, write a Python function to calculate the sum of all elements. Add Big-O analysis."
"""

from typing import Iterable

def sum_array(nums: Iterable[int]) -> int:
    total = 0
    for x in nums:  # O(n)
        total += x
    return total

if __name__ == "__main__":
    sample = [3, -2, 7, 4]
    print(sum_array(sample))  # 12