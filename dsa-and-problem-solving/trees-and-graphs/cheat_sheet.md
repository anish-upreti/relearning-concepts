# Week 4 — Trees & Graphs Cheat Sheet

---

## The One Skeleton (memorize this)

Every recursive tree function follows this exact shape. The only thing that changes is **where you put "do something"** and **what you return**.

```python
def solve(node):
    if node is None:        # base case — always first
        return <something>
    # do something
    solve(node.left)
    solve(node.right)
    return <something>
```

---

## Vocabulary

| Term | Meaning |
|------|---------|
| Root | Top node, no parent |
| Leaf | Node with no children |
| Height | Longest **edge** path from node to a leaf. Single leaf = 0. Empty node = -1. |
| Depth | Number of **nodes** from root to a node. Root = 1. Empty node = 0. |
| Subtree | Any node + everything below it |

> **Height vs Depth:** Height counts edges (base case = -1). Depth counts nodes (base case = 0). `maxDepth` on LeetCode counts nodes so base case is 0, not -1.

---

## TreeNode

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

---

## The Three DFS Traversals

The only difference between all three is **where you process the node** relative to recursing into children.

| Traversal | Order | Use |
|-----------|-------|-----|
| Inorder | L → Node → R | BST gives sorted output automatically |
| Preorder | Node → L → R | Serialize or copy a tree — process parent before children |
| Postorder | L → R → Node | Compute from leaves up — need children's results first (height, size) |

> **Memory trick:** "Pre" = process me first. "Post" = process me last. "In" = process me in between (left, then me, then right).

```python
def inorder(node, result=None):
    if result is None: result = []
    if node is None: return result
    inorder(node.left, result)
    result.append(node.val)     # Node processed in the middle
    inorder(node.right, result)
    return result
```

---

## BFS vs DFS

| | BFS | DFS |
|--|-----|-----|
| Data structure | Queue (`deque`) | Stack or recursion |
| Order | Level by level | Branch by branch |
| Best for | Level output, shortest path | Subtree problems, path problems |
| Space | O(w) — max width of tree | O(h) — height of tree |

> **When tree is wide** → DFS uses less memory.  
> **When tree is deep** → BFS uses less memory.  
> **Iterative DFS:** Push **right child first**, then left — stack is LIFO so left gets popped first.

**Level order BFS trick:** `level_size = len(queue)` at the start of each level tells you exactly how many nodes belong to that level. Process only that many, then move to the next level.

```python
def levelOrder(root):
    if root is None: return []
    queue = deque([root])
    result = []
    while queue:
        level_size = len(queue)   # snapshot — only process this many nodes
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

---

## Recursion Patterns

### Pattern 1 — Return a value up (postorder)
> Think: "I need my children's answers before I can compute my own answer."  
> Used for: height, count_nodes, maxDepth

```python
def height(node):
    if node is None: return -1
    return 1 + max(height(node.left), height(node.right))
```

### Pattern 2 — Pass bounds down (preorder)
> Think: "My children need context from me about where they are in the tree."  
> Used for: isValidBST — local neighbor check is NOT enough, must pass global bounds.

```python
def isValidBST(root, min_val=float('-inf'), max_val=float('inf')):
    if root is None: return True
    if not (min_val < root.val < max_val): return False
    return isValidBST(root.left, min_val, root.val) and \
           isValidBST(root.right, root.val, max_val)
```

### Pattern 3 — Check two trees together
> Think: "I need to walk both trees in lockstep, comparing at every node."  
> Used for: isSameTree — 3 cases: both None → True, one None → False, check val + recurse.

```python
def isSameTree(p, q):
    if p is None and q is None: return True
    if p is None or q is None:  return False
    if p.val != q.val:          return False
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

### Pattern 4 — Two-function pattern
> Think: "I need to ask a question at every possible starting point in the tree."  
> Outer function walks every node. Inner function checks a condition at each position.  
> Used for: isSubtree — at each node, ask "does the tree starting here match subRoot?"

```python
def isSubtree(root, subRoot):
    if root is None: return False
    if isSameTree(root, subRoot): return True   # check at this position
    return isSubtree(root.left, subRoot) or \
           isSubtree(root.right, subRoot)       # check all other positions
```

---

## BST Rules

- **The property:** Left subtree < node < right subtree — at EVERY node, not just immediate children. A node can violate BST rules because of an ancestor, not just its parent.
- **Inorder traversal** of a BST always gives sorted output — key insight for kth smallest.
- **Search/Insert:** O(log n) average. Worst case O(n) when tree is skewed (inserting in sorted order creates a linked list).
- **Duplicates:** Not allowed in a standard BST. It means you can't have two nodes with the same value.

The BST rule is left < node < right — strict inequalities. If you try to insert a duplicate, it's neither less than nor greater than the current node, so the rule breaks down and you don't know which side it belongs on.

### BST Search
> Follow the BST property — go left if target is smaller, right if larger. Stop when found or hit None.

```python
def bst_search(root, target):
    if root is None:       return None
    if target == root.val: return root
    if target < root.val:  return bst_search(root.left, target)
    return bst_search(root.right, target)
```

### BST Insert
> Follow the same path as search. When you hit None, that's where the new node belongs.  
> **Key:** Return root at every step — this is how parent nodes stay connected to newly inserted node.

```python
def bst_insert(root, val):
    if root is None: return TreeNode(val)          # insert here
    if val < root.val: root.left = bst_insert(root.left, val)
    else:              root.right = bst_insert(root.right, val)
    return root
```

### BST Delete — 3 cases
> **Case 1 (leaf):** Return None — just remove it.  
> **Case 2 (one child):** Return the existing child — replace node with its child.  
> **Case 3 (two children):** Find inorder successor (smallest in right subtree), copy its value here, then delete that successor from the right subtree.

```python
def bst_delete(root, val):
    if root is None: return None
    if val < root.val:   root.left = bst_delete(root.left, val)
    elif val > root.val: root.right = bst_delete(root.right, val)
    else:
        if root.left is None:  return root.right   # case 1 & 2
        if root.right is None: return root.left    # case 2
        successor = root.right                     # case 3: find min in right subtree
        while successor.left:
            successor = successor.left
        root.val = successor.val                   # copy successor's value
        root.right = bst_delete(root.right, successor.val)  # delete successor
    return root
```

### Lowest Common Ancestor (BST)
> The BST property tells you which direction to go. When p and q split to different sides (or one equals current node), you've found the LCA — no need to check both subtrees.

```python
def LCA(root, p, q):
    if p.val < root.val and q.val < root.val: return LCA(root.left, p, q)
    if p.val > root.val and q.val > root.val: return LCA(root.right, p, q)
    return root   # they split here — this node is the LCA
```

---

## LeetCode Problems

| Problem | Pattern | Key insight |
|---------|---------|-------------|
| Invert Binary Tree (#226) | Postorder | Swap children *after* recursing — need children inverted first |
| Max Depth (#104) | Return value up | `1 + max(left, right)`, base case = 0 (counting nodes not edges) |
| Level Order (#102) | BFS | `level_size = len(queue)` captures the current level boundary |
| Same Tree (#100) | Two trees together | 3 cases: both None → True, one None → False, check val + recurse |
| Validate BST (#98) | Pass bounds down | Local neighbor check is not enough — need global min/max bounds |
| Kth Smallest (#230) | Inorder = sorted | Inorder gives sorted order, answer is at index `k-1` |
| Subtree of Another (#572) | Two-function | Outer walks all nodes, inner checks `isSameTree` at each position |
| Lowest Common Ancestor (#235) | BST property | When p and q split to different sides, current node is the LCA |

---

## ML Connections

**Decision Tree:** Each internal node is a BST-like split (`feature < threshold?`). `predict()` traverses from root to leaf using DFS. Tree height directly controls model complexity — deeper = more overfitting.

**Random Forest:** N decision trees trained on bootstrap samples. `predict()` averages leaf values across all trees. `max_depth` in sklearn caps tree height to control overfitting.

**XGBoost/LightGBM:** Gradient-boosted trees — each new tree corrects the residuals of all previous ones. Same DFS traversal logic, different training objective.

**RAG Chunking :** LangChain's `RecursiveCharacterTextSplitter` uses the exact same recursion pattern — try splitting by paragraph, then sentence, then word, until chunks are small enough. Same base case + recurse structure as tree problems.
