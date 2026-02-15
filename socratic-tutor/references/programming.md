# Programming Teaching Patterns

Reference for teaching algorithms, data structures, and programming concepts with clarity and rigor.

---

## Algorithm Explanation Pattern

### Complete Algorithm Presentation

❌ **BAD: Just code without context**
```typescript
function binarySearch(arr: number[], target: number): number {
  let left = 0;
  let right = arr.length - 1;
  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    if (arr[mid] === target) return mid;
    if (arr[mid] < target) left = mid + 1;
    else right = mid - 1;
  }
  return -1;
}
```
**Why it's bad:** No explanation of why this works, what it assumes, or how to use it.

✅ **GOOD: Full pedagogical treatment**
```
Algorithm: Binary Search

Purpose: Find the index of a target value in a sorted array

Precondition: Array must be sorted in ascending order
Time Complexity: O(log n)
Space Complexity: O(1)

Intuition:
Like finding a word in a dictionary - open to the middle, check if your word
comes before or after, then repeat on the relevant half. Each step eliminates
half the remaining possibilities.

Visual Example:
Array: [1, 3, 5, 7, 9, 11, 13, 15]  Target: 7
       
Step 1: Check middle (index 3): 7 < 7? No. 7 > 7? No. Found at index 3!

Array: [1, 3, 5, 7, 9, 11, 13, 15]  Target: 12

Step 1: Check middle (index 3): arr[3]=7, 12 > 7, search right half
        [1, 3, 5, 7,|9, 11, 13, 15]
        
Step 2: Check middle (index 5): arr[5]=11, 12 > 11, search right half
        [9, 11,|13, 15]
        
Step 3: Check middle (index 6): arr[6]=13, 12 < 13, search left half
        [13,|15]  → no elements between 11 and 13 → not found (-1)

Implementation:
```typescript
/**
 * Binary search - finds index of target in sorted array
 * @param arr - Sorted array of numbers (ascending)
 * @param target - Value to find
 * @returns Index of target, or -1 if not found
 * @complexity Time: O(log n), Space: O(1)
 */
function binarySearch(arr: number[], target: number): number {
  // Initialize search range to entire array
  let left = 0;
  let right = arr.length - 1;
  
  // Continue while search range is valid
  while (left <= right) {
    // Find middle index (avoid overflow with left + (right-left)/2)
    const mid = Math.floor((left + right) / 2);
    
    // Check if we found the target
    if (arr[mid] === target) {
      return mid;
    }
    
    // Target is in right half
    if (arr[mid] < target) {
      left = mid + 1;  // Exclude mid and everything left
    } 
    // Target is in left half
    else {
      right = mid - 1;  // Exclude mid and everything right
    }
  }
  
  // Target not found
  return -1;
}
```

Edge Cases:
- Empty array: Returns -1 (no elements to search)
- Single element: Checks that element, returns index or -1
- Target at boundaries: Works correctly for first or last element
- Duplicates: Returns index of one occurrence (not guaranteed which)

Common Mistakes:
1. Forgetting array must be sorted - binary search fails on unsorted data
2. Using `mid = (left + right) / 2` which can overflow for large arrays
3. Using `while (left < right)` instead of `<=`, missing single element case
```

---

## Data Structure Teaching Pattern

### Multi-Level Explanation

❌ **BAD: Only implementation**
```typescript
class Stack {
  private items: number[] = [];
  push(item: number) { this.items.push(item); }
  pop(): number | undefined { return this.items.pop(); }
}
```
**Why it's bad:** No context for when/why to use a stack.

✅ **GOOD: Concept, visualization, implementation, usage**
```
Data Structure: Stack

Concept:
Last-In-First-Out (LIFO) data structure. Elements are added and removed
from the same end (called the "top"). Like a stack of plates - you add to
the top and remove from the top.

Operations:
- push(item): Add item to top - O(1)
- pop(): Remove and return top item - O(1)
- peek(): View top item without removing - O(1)
- isEmpty(): Check if stack is empty - O(1)

Visual Representation:
```
push(1)    push(2)    push(3)    pop()      pop()
  |          |          |          |          |
  v          v          v          v          v
         ┌───┐      ┌───┐      ┌───┐      ┌───┐
         │ 2 │      │ 3 │      │ 2 │      │ 1 │
┌───┐    ├───┤      ├───┤      └───┘      └───┘
│ 1 │    │ 1 │      │ 2 │
└───┘    └───┘      ├───┤
                    │ 1 │
                    └───┘
```

When to Use:
- Function call management (call stack)
- Undo/redo functionality
- Expression evaluation (infix to postfix)
- Depth-first search traversal
- Bracket matching

Implementation (Array-based):
```typescript
/**
 * Stack implementation using dynamic array
 * @template T - Type of elements in stack
 */
class Stack<T> {
  private items: T[] = [];
  
  /**
   * Add element to top of stack
   * @param item - Element to add
   * @complexity O(1) amortized
   */
  push(item: T): void {
    this.items.push(item);
  }
  
  /**
   * Remove and return top element
   * @returns Top element, or undefined if empty
   * @complexity O(1)
   */
  pop(): T | undefined {
    return this.items.pop();
  }
  
  /**
   * View top element without removing
   * @returns Top element, or undefined if empty
   * @complexity O(1)
   */
  peek(): T | undefined {
    return this.items[this.items.length - 1];
  }
  
  /**
   * Check if stack is empty
   * @returns true if empty, false otherwise
   * @complexity O(1)
   */
  isEmpty(): boolean {
    return this.items.length === 0;
  }
  
  /**
   * Get number of elements in stack
   * @returns Number of elements
   * @complexity O(1)
   */
  size(): number {
    return this.items.length;
  }
}
```

Example Usage:
```typescript
const stack = new Stack<number>();

// Push elements
stack.push(10);
stack.push(20);
stack.push(30);

console.log(stack.peek());  // 30 (top element)
console.log(stack.pop());   // 30 (removed)
console.log(stack.pop());   // 20 (removed)
console.log(stack.size());  // 1 (only 10 remains)
```

Alternative Implementation (Linked List):
[Could show linked list version for comparison]

Trade-offs:
- Array: Simple, cache-friendly, but may need resizing
- Linked List: No resizing, but pointer overhead and cache misses
```

---

## Complexity Analysis Teaching

### From Counting to Big-O

❌ **BAD: Just stating complexity**
```
This algorithm is O(n²).
```
**Why it's bad:** Learner doesn't understand why or how to derive it.

✅ **GOOD: Step-by-step derivation**
```
Algorithm: Find all pairs with sum equal to target

```typescript
function findPairs(arr: number[], target: number): [number, number][] {
  const pairs: [number, number][] = [];
  
  for (let i = 0; i < arr.length; i++) {           // Line 1
    for (let j = i + 1; j < arr.length; j++) {     // Line 2
      if (arr[i] + arr[j] === target) {            // Line 3
        pairs.push([arr[i], arr[j]]);              // Line 4
      }
    }
  }
  
  return pairs;
}
```

Step 1: Count operations in terms of input size n

Let n = arr.length

Line 1: Outer loop runs n times
Line 2: Inner loop runs:
  - (n-1) times when i=0
  - (n-2) times when i=1
  - (n-3) times when i=2
  - ...
  - 1 time when i=n-2
  - 0 times when i=n-1

Total inner loop iterations: (n-1) + (n-2) + ... + 1 + 0 = n(n-1)/2

Line 3: Runs once per inner loop iteration → n(n-1)/2 times
Line 4: Worst case (all pairs match) → n(n-1)/2 times

Step 2: Express total operations

T(n) = n(n-1)/2 comparisons + n(n-1)/2 potential pushes
     = n(n-1) operations
     = n² - n

Step 3: Apply Big-O definition

For large n, the n² term dominates:
T(n) = n² - n < n² for all n > 0

By definition of Big-O, if T(n) ≤ c·f(n) for some constant c and n ≥ n₀,
then T(n) = O(f(n)).

Here: n² - n ≤ 1·n² for all n ≥ 1

Therefore: T(n) = O(n²)

Intuition: Nested loops over array of size n → quadratic complexity

Can we do better?
Yes! Use hash set for O(n) solution:
```typescript
function findPairsOptimized(arr: number[], target: number): [number, number][] {
  const seen = new Set<number>();
  const pairs: [number, number][] = [];
  
  for (const num of arr) {                    // O(n) iterations
    const complement = target - num;
    if (seen.has(complement)) {               // O(1) hash lookup
      pairs.push([complement, num]);
    }
    seen.add(num);                            // O(1) hash insert
  }
  
  return pairs;
}
```

Optimized complexity: O(n) time, O(n) space
```

---

## Debugging and Error Patterns

### Common Bug Categories

❌ **BAD: Just showing broken code**
```typescript
function reverse(arr: number[]): number[] {
  for (let i = 0; i < arr.length / 2; i++) {
    const temp = arr[i];
    arr[i] = arr[arr.length - i];
    arr[arr.length - i] = temp;
  }
  return arr;
}
```
**Why it's bad:** Doesn't explain what's wrong or how to fix it.

✅ **GOOD: Identify bug, explain, fix, test**
```
Common Bug: Off-by-One Error

Broken Code:
```typescript
function reverse(arr: number[]): number[] {
  for (let i = 0; i < arr.length / 2; i++) {
    const temp = arr[i];
    arr[i] = arr[arr.length - i];      // BUG: should be length - i - 1
    arr[arr.length - i] = temp;        // BUG: should be length - i - 1
  }
  return arr;
}
```

What's Wrong:
Array indices are 0-based. For array of length n:
- Valid indices: 0, 1, 2, ..., n-1
- arr[arr.length] accesses arr[n], which is OUT OF BOUNDS

Example: arr = [1, 2, 3] (length = 3)
- When i=0: arr[3] is accessed (out of bounds!)
- Should access: arr[2] (last element)

Formula: To access element k positions from the end:
  Correct: arr[length - k - 1]  (0-indexed)
  Wrong: arr[length - k]        (1-indexed assumption)

Fixed Code:
```typescript
function reverse(arr: number[]): number[] {
  for (let i = 0; i < arr.length / 2; i++) {
    const temp = arr[i];
    const oppositeIndex = arr.length - i - 1;  // Explicit calculation
    arr[i] = arr[oppositeIndex];
    arr[oppositeIndex] = temp;
  }
  return arr;
}
```

Test Cases:
```typescript
// Test 1: Odd length
reverse([1, 2, 3, 4, 5]);  // [5, 4, 3, 2, 1] ✓

// Test 2: Even length
reverse([1, 2, 3, 4]);     // [4, 3, 2, 1] ✓

// Test 3: Single element
reverse([1]);              // [1] ✓

// Test 4: Empty array
reverse([]);               // [] ✓
```

Lesson: Always verify index calculations with concrete examples before 
        assuming they're correct. Off-by-one errors are extremely common.
```

---

## Recursion Teaching Pattern

### Build Recursion Intuition

❌ **BAD: Just recursive code**
```typescript
function factorial(n: number): number {
  if (n === 0) return 1;
  return n * factorial(n - 1);
}
```
**Why it's bad:** Doesn't build understanding of how recursion works.

✅ **GOOD: Intuition, visualization, trace, implementation**
```
Concept: Factorial (n!)

Definition: n! = n × (n-1) × (n-2) × ... × 2 × 1
            0! = 1 (by convention)

Example: 5! = 5 × 4 × 3 × 2 × 1 = 120

Recursive Insight:
Notice the pattern:
  5! = 5 × (4 × 3 × 2 × 1) = 5 × 4!
  4! = 4 × (3 × 2 × 1) = 4 × 3!
  3! = 3 × (2 × 1) = 3 × 2!
  2! = 2 × 1 = 2 × 1!
  1! = 1 = 1 × 0!
  0! = 1 (base case)

Pattern: n! = n × (n-1)!  for n > 0
         0! = 1

This is a RECURSIVE DEFINITION:
- Base case: 0! = 1
- Recursive case: n! = n × (n-1)!

Execution Trace for factorial(3):
```
factorial(3)
  ├─ 3 × factorial(2)
  │    ├─ 2 × factorial(1)
  │    │    ├─ 1 × factorial(0)
  │    │    │    └─ return 1  (base case)
  │    │    └─ return 1 × 1 = 1
  │    └─ return 2 × 1 = 2
  └─ return 3 × 2 = 6
```

Call Stack Visualization:
```
Step 1: factorial(3) called
  Stack: [factorial(3)]
  
Step 2: factorial(3) calls factorial(2)
  Stack: [factorial(3), factorial(2)]
  
Step 3: factorial(2) calls factorial(1)
  Stack: [factorial(3), factorial(2), factorial(1)]
  
Step 4: factorial(1) calls factorial(0)
  Stack: [factorial(3), factorial(2), factorial(1), factorial(0)]
  
Step 5: factorial(0) returns 1 (base case)
  Stack: [factorial(3), factorial(2), factorial(1)]
  
Step 6: factorial(1) returns 1 × 1 = 1
  Stack: [factorial(3), factorial(2)]
  
Step 7: factorial(2) returns 2 × 1 = 2
  Stack: [factorial(3)]
  
Step 8: factorial(3) returns 3 × 2 = 6
  Stack: []
  
Final result: 6
```

Implementation:
```typescript
/**
 * Compute factorial recursively
 * @param n - Non-negative integer
 * @returns n! = n × (n-1) × ... × 2 × 1
 * @complexity Time: O(n), Space: O(n) for call stack
 */
function factorial(n: number): number {
  // Base case: 0! = 1 by definition
  if (n === 0) {
    return 1;
  }
  
  // Recursive case: n! = n × (n-1)!
  // Trust that factorial(n-1) works (recursive leap of faith)
  return n * factorial(n - 1);
}
```

Key Recursion Principles:
1. **Base case**: Must have terminating condition
2. **Progress toward base**: Each recursive call must get closer to base case
3. **Recursive leap of faith**: Assume recursive call works for smaller input
4. **Combine results**: Use result from recursive call to compute current case

Iterative Alternative (for comparison):
```typescript
function factorialIterative(n: number): number {
  let result = 1;
  for (let i = 1; i <= n; i++) {
    result *= i;
  }
  return result;
}
```

Trade-offs:
- Recursive: More intuitive for problems with recursive structure, but uses call stack (O(n) space)
- Iterative: More efficient (O(1) space), but may be less intuitive for some problems
```

---

## Type System Teaching

### Progressive Type Introduction

❌ **BAD: Complex types without context**
```typescript
type Mapper<T, U> = (value: T) => U;
const map = <T, U>(arr: T[], fn: Mapper<T, U>): U[] => arr.map(fn);
```
**Why it's bad:** Overwhelming for beginners without type foundation.

✅ **GOOD: Build from simple to complex**
```
Level 1: Basic Types
```typescript
// Primitive types
const age: number = 25;
const name: string = "Alice";
const isActive: boolean = true;

// Array types
const numbers: number[] = [1, 2, 3, 4, 5];
const names: string[] = ["Alice", "Bob"];
```

Level 2: Function Types
```typescript
// Function parameter and return types
function add(a: number, b: number): number {
  return a + b;
}

// Function type annotation
const multiply: (x: number, y: number) => number = (x, y) => x * y;
```

Level 3: Object Types
```typescript
// Object literal types
type Person = {
  name: string;
  age: number;
  email: string;
};

const alice: Person = {
  name: "Alice",
  age: 30,
  email: "alice@example.com"
};
```

Level 4: Generic Types
```typescript
// Generic function - works with any type
function identity<T>(value: T): T {
  return value;
}

const num = identity<number>(42);     // T = number
const str = identity<string>("hi");   // T = string

// Generic array operations
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

first([1, 2, 3]);      // T inferred as number
first(["a", "b"]);     // T inferred as string
```

Level 5: Higher-Order Function Types
```typescript
// Type alias for mapping function
type Mapper<T, U> = (value: T) => U;

// map takes array of T and function T→U, returns array of U
function map<T, U>(arr: T[], fn: Mapper<T, U>): U[] {
  const result: U[] = [];
  for (const item of arr) {
    result.push(fn(item));
  }
  return result;
}

// Example usage:
const numbers = [1, 2, 3, 4, 5];
const doubled = map(numbers, (x) => x * 2);         // number[]
const strings = map(numbers, (x) => x.toString());  // string[]
```

Why Generics Matter:
Without generics:
```typescript
// Need separate function for each type
function mapNumbers(arr: number[], fn: (x: number) => number): number[] { ... }
function mapStrings(arr: string[], fn: (x: string) => string): string[] { ... }
// This doesn't scale!
```

With generics:
```typescript
// One function works for all types
function map<T, U>(arr: T[], fn: (x: T) => U): U[] { ... }
```
```

---

## Testing and Verification

### Systematic Test Case Design

❌ **BAD: Random test cases**
```typescript
console.log(binarySearch([1, 2, 3], 2));  // Test 1
console.log(binarySearch([5], 5));        // Test 2
```
**Why it's bad:** Doesn't cover edge cases or demonstrate systematic thinking.

✅ **GOOD: Comprehensive test suite with categories**
```
Test Suite for binarySearch(arr, target)

Category 1: Happy Path (element exists)
```typescript
test("Target in middle of array", () => {
  expect(binarySearch([1, 3, 5, 7, 9], 5)).toBe(2);
});

test("Target at start of array", () => {
  expect(binarySearch([1, 3, 5, 7, 9], 1)).toBe(0);
});

test("Target at end of array", () => {
  expect(binarySearch([1, 3, 5, 7, 9], 9)).toBe(4);
});
```

Category 2: Element Not Found
```typescript
test("Target less than all elements", () => {
  expect(binarySearch([1, 3, 5, 7, 9], 0)).toBe(-1);
});

test("Target greater than all elements", () => {
  expect(binarySearch([1, 3, 5, 7, 9], 10)).toBe(-1);
});

test("Target in gap between elements", () => {
  expect(binarySearch([1, 3, 5, 7, 9], 4)).toBe(-1);
});
```

Category 3: Edge Cases
```typescript
test("Empty array", () => {
  expect(binarySearch([], 5)).toBe(-1);
});

test("Single element - found", () => {
  expect(binarySearch([5], 5)).toBe(0);
});

test("Single element - not found", () => {
  expect(binarySearch([5], 3)).toBe(-1);
});

test("Two elements - found first", () => {
  expect(binarySearch([1, 5], 1)).toBe(0);
});

test("Two elements - found second", () => {
  expect(binarySearch([1, 5], 5)).toBe(1);
});
```

Category 4: Duplicates (if applicable)
```typescript
test("Duplicate elements", () => {
  const result = binarySearch([1, 3, 3, 3, 5], 3);
  // Returns index of ONE occurrence (not specified which)
  expect([1, 2, 3]).toContain(result);
});
```

Test Design Principles:
1. **Boundary testing**: First, last, empty, single element
2. **Equivalence classes**: Found vs not found
3. **Edge cases**: Empty, minimal input, maximum input
4. **Invalid inputs**: (if applicable) null, undefined, unsorted array
```
