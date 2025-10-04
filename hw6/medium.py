"""
 Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
 HW6
 --------------------------------------------------------------------
 Medium Q2 — Second largest (distinct)
 Big-O (time): O(n) | Big-O (space): O(1)
 ChatGPT prompts used:
 "Find the second largest DISTINCT number in a list; handle edge cases; add Big-O analysis."
"""

from typing import Iterable, Optional

def second_largest(nums: Iterable[int]) -> Optional[int]:
    first = None
    second = None
    for x in nums:  # O(n)
        if first is None or x > first:
            if x != first:
                second = first
                first = x
        elif x != first and (second is None or x > second):
            second = x
    return second

if __name__ == "__main__":
    print(second_largest([5, 1, 9, 9, 3, 7]))  
    print(second_largest([2, 2]))  