"""
Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
HW7 - Easy: Insert into a Binary Search Tree (BST)
--------------------------------------------------------------------
ChatGPT prompts used:
1) "Write a Python function to insert a value into a binary search tree. The function should take the root and the value as parameters."
2) "Match the instructor's bst.py style (Node, insert, inorder, main)."
"""

# ---------------- A Binary Tree Node ----------------
class Node:
    # Constructor to create a new node
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

# ---------------- Insert into BST ----------------
def insert(node, key):
    # If the tree is empty, return a new node
    if node is None:
        return Node(key)
    # Otherwise recur down the tree
    if key < node.key:
        node.left = insert(node.left, key)
    else:
        node.right = insert(node.right, key)
    # return the (unchanged) node pointer
    return node

# ---------------- Inorder traversal ----------------
def inorder(root):
    if root is not None:
        inorder(root.left)
        print(root.key, end=" ")
        inorder(root.right)

# ---------------- ASCII Display (from print_tree.py style) ----------------
def display(root):
    if root is None:
        print("(empty)")
        return
    lines, *_ = display_aux(root)
    for line in lines:
        print(line)

def display_aux(root):
    # Returns list of strings, width, height, and horizontal coordinate of the root.
    if root.right is None and root.left is None:
        s = f"{root.key}"
        return [s], len(s), 1, len(s)//2
    if root.right is None:
        lines, n, p, x = display_aux(root.left)
        s = f"{root.key}"; u = len(s)
        first  = (x+1)*" " + (n-x-1)*"_" + s
        second = x*" " + "/" + (n-x-1+u)*" "
        shifted = [line + u*" " for line in lines]
        return [first, second] + shifted, n+u, p+2, n + u//2
    if root.left is None:
        lines, n, p, x = display_aux(root.right)
        s = f"{root.key}"; u = len(s)
        first  = s + x*"_" + (n-x)*" "
        second = (u+x)*" " + "\\" + (n-x-1)*" "
        shifted = [u*" " + line for line in lines]
        return [first, second] + shifted, n+u, p+2, u//2
    left, n, p, x = display_aux(root.left)
    right, m, q, y = display_aux(root.right)
    s = f"{root.key}"; u = len(s)
    first  = (x+1)*" " + (n-x-1)*"_" + s + y*"_" + (m-y)*" "
    second = x*" " + "/" + (n-x-1+u+y)*" " + "\\" + (m-y-1)*" "
    if p < q:
        left += [n*" "]* (q-p)
    elif q < p:
        right += [m*" "]* (p-q)
    lines = [a + u*" " + b for a,b in zip(left, right)]
    return [first, second] + lines, n+m+u, max(p,q)+2, n + u//2

# ---------------- main: build & show ----------------
def main():
    # tree:
    root = None
    for v in [50, 30, 70, 20, 40, 60, 80]:
        root = insert(root, v)

    print("Inorder (sorted):")
    inorder(root); print("\n")
    display(root)

main()
