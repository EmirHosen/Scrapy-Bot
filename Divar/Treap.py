import random

class Node:
    def __init__(self, key):
        self.key = key
        self.priority = random.randint(1, 100)
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root = None

    def rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        return y

    def rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        return y 

    def insert_util(self, root, key):
        if not root:
            return Node(key)

        if key < root.key:
            root.left = self.insert_util(root.left, key)

            if root.left.priority > root.priority:
                root = self.rotate_right(root)
        else:
            root.right = self.insert_util(root.right, key)

            if root.right.priority > root.priority:
                root = self.rotate_left(root)

        return root

    def insert(self, key):
        self.root = self.insert_util(self.root, key)

    def inorder_util(self, root, result):
        if root:
            self.inorder_util(root.left, result)
            result.append(root.key)
            self.inorder_util(root.right, result)

    def inorder(self):
        result = []
        self.inorder_util(self.root, result)
        return result

# نمونه استفاده
treap = Treap()
data = [4, 2, 5, 1, 3]

for key in data:
    treap.insert(key)

print(treap.inorder())  # Output: [1, 2, 3, 4, 5]