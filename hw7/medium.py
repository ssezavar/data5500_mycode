"""
Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
HW7 - Medium: Search in a Binary Search Tree (BST)
Return True if the value exists, else False.
--------------------------------------------------------------------
ChatGPT prompts used:
1) "Implement a Python function to search for a value in a BST (True/False)."
2) "Match instructor style with Node, insert, and a small test."
"""

from typing import Optional

class Node:
    def __init__(self, key: int):
        self.key = key
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None

def insert(root: Optional[Node], value: int) -> Node:
    if root is None:
        return Node(value)
    if value < root.key:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)  # duplicates to the right
    return root

def search(root: Optional[Node], target: int) -> bool:
    """Return True if target exists in BST; otherwise False."""
    if root is None:
        return False
    if target == root.key:
        return True
    if target < root.key:
        return search(root.left, target)
    return search(root.right, target)

# Optional local sanity test
if __name__ == "__main__":
    vals = [50, 30, 70, 20, 40, 60, 80]
    r: Optional[Node] = None
    for v in vals:
        r = insert(r, v)

    tests = [60, 10, 80, 35, 50]
    for t in tests:
        print(f"search({t}) -> {search(r, t)}")
