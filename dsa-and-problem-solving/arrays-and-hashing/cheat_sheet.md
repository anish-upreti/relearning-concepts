# Arrays & Hashing — Patterns Cheat Sheet
Week 3 (Days 15-19)

---

## 1. Hash Maps

**Core idea:** key → value, O(1) lookup, O(1) insert, O(1) delete

```python
# build
d = {}
d[key] = value

# safe lookup (no KeyError)
d.get(key, default)

# check membership — O(1)
key in d

# iterate
for k, v in d.items()
for k in d.keys()
for v in d.values()
```

**Use when:**
- Need O(1) lookup by a key
- Counting, grouping, caching
- Avoiding O(n) search through a list

**Collision handling:** chaining — each bucket holds a list of pairs

---

## 2. Frequency Counting

**Core idea:** count how many times each item appears

```python
# manual
freq = {}
for item in collection:
    freq[item] = freq.get(item, 0) + 1

# shortcut
from collections import Counter
freq = Counter(collection)

# top k by frequency
sorted(freq, key=lambda x: freq[x], reverse=True)[:k]
Counter(collection).most_common(k)
```

**Use when:** "how many times does X appear?"

---

## 3. Grouping Pattern

**Core idea:** collect items that share a property under the same key

```python
groups = {}
for item in collection:
    key = some_function(item)          # canonical key
    groups.setdefault(key, []).append(item)

return list(groups.values())
```

**Use when:** "which items share property X?"

**Key trick for anagrams:** `"".join(sorted(word))` — all anagrams produce the same sorted string

---

## 4. Prefix Sums

**Core idea:** precompute running totals, answer range queries in O(1)

```python
# build — O(n), done once
prefix = [0]
for num in nums:
    prefix.append(prefix[-1] + num)

# range query — O(1)
def range_sum(prefix, i, j):
    return prefix[j + 1] - prefix[i]

# rolling window of size N ending at index i
prefix[i + 1] - prefix[i + 1 - N]
```

**Complexity:**
- Build: O(n) once
- Query: O(1) per query
- Use when: many range queries on the same array

**Use when:** "what is the sum from index i to j?" asked many times

**Not worth it when:** only one query — just loop through the range

---

## 5. Sliding Window

### Fixed Size
```python
# build first window manually
window_sum = sum(nums[0:k])
max_sum = window_sum

# slide
for i in range(k, len(nums)):
    window_sum = window_sum + nums[i] - nums[i - k]
    max_sum = max(max_sum, window_sum)
```

**Formula:** `window_sum + nums[i] - nums[i-k]`
- `nums[i]`   → entering from right
- `nums[i-k]` → leaving from left

### Variable Size
```python
left = 0
window = set()   # or dict if you need counts
max_window = 0

for right in range(len(nums)):
    # shrink from left while condition violated
    while nums[right] in window:
        window.remove(nums[left])
        left += 1
    window.add(nums[right])
    max_window = max(max_window, len(window))

return max_window
```

**Use when:** "find longest/shortest subarray satisfying a condition"

**Why set not list:** `x in set` is O(1), `x in list` is O(n) → list makes whole solution O(n²)

---

## Sliding Window vs Prefix Sum

| | Sliding Window | Prefix Sum |
|--|---------------|------------|
| Window size | fixed or variable | fixed |
| Queries | one pass, find best window | many arbitrary range queries |
| Data | works on live streams | needs full array upfront |
| Use when | find optimal subarray | answer multiple range queries |

---

## Pattern Recognition — Which to Use?

| Problem says... | Use |
|----------------|-----|
| "how many times" / "frequency" / "count" | Frequency counting |
| "group by" / "which ones share" | Grouping |
| "sum from i to j" / "range query" / "rolling window" (many queries) | Prefix sum |
| "longest/shortest subarray with condition" | Sliding window (variable) |
| "max/min sum of subarray of size k" | Sliding window (fixed) |
| "O(1) lookup" / "seen before" / "cache" | Hash map |

---

## Common Mistakes

- Using `list` instead of `set` for membership checks → O(n²)
- Using `split(" ")` instead of `split()` → empty strings from multiple spaces
- Variable shadowing: `for word in words` then using `word` as both loop var and parameter
- Forgetting `return list(groups.values())` — returning dict instead of list of lists
- Prefix sum: starting loop at `i=0` instead of `i=k` → negative index wraps around silently
- Sliding window: returning `len(set)` at end instead of tracking `max_window` during loop
- TF-IDF: not splitting before `word in doc` → substring matches instead of whole word matches
