"""
Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
HW7 - Easy: Insert into a Binary Search Tree (BST)
--------------------------------------------------------------------
ChatGPT prompts used:
1) "Write a Python function to insert a value into a binary search tree. The function should take the root and the value as parameters."
2) "Match the instructor's bst.py style (Node, insert, inorder, main)."
"""

from typing import Optional

class Node:
    def __init__(self, key: int):
        self.key = key
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None

def insert(root: Optional[Node], value: int) -> Node:
    """Insert value into BST and return the (possibly new) root."""
    if root is None:
        return Node(value)
    if value < root.key:
        root.left = insert(root.left, value)
    else:
        # duplicates go to the right by policy
        root.right = insert(root.right, value)
    return root

# Optional local sanity test
if __name__ == "__main__":
    def inorder(n: Optional[Node]) -> None:
        if not n: return
        inorder(n.left)
        print(n.key, end=" ")
        inorder(n.right)

    vals = [50, 30, 70, 20, 40, 60, 80]
    r: Optional[Node] = None
    for v in vals:
        r = insert(r, v)

    print("Inorder traversal (should be sorted):", end=" ")
    inorder(r)
    print()
