# Socratic Tutor

> **Note:**
> This document provides implementation patterns for tutoring sessions. Load this when you need specific templates for lesson structure, question design, or assessment creation.

---

## Abstract

Implementation guide for interactive tutoring using Socratic methods. Includes lesson templates, question frameworks, and assessment patterns. Load sections as needed during tutoring sessions.

---

## How to Use This Guide

1. **Start with SKILL.md**: Follow the main tutoring workflow
2. **Load templates when needed**: Reference specific sections during lesson preparation
3. **Adapt patterns**: These are templates, not rigid scripts - adjust for domain and learner

---

## Quick Reference

- [1.0 Zero-Knowledge Teaching Patterns](#10-zero-knowledge-teaching-patterns)
- [1.1 Lesson Structure Templates](#11-lesson-structure-templates)
- [1.2 Socratic Question Frameworks](#12-socratic-question-frameworks)
- [1.3 Exercise Design Patterns](#13-exercise-design-patterns)
- [1.4 Assessment Types](#14-assessment-types)
- [1.5 Explanation Techniques](#15-explanation-techniques)
- [1.6 Session Management and Checkpoints](#16-session-management-and-checkpoints)

---

## 1. Implementation Patterns

### 1.0 Zero-Knowledge Teaching Patterns

**CRITICAL PRINCIPLE: Same detailed content for everyone. User's responses determine pace naturally.**

**No Pacing Pre-Judgment:**

The tutor doesn't decide in advance how much time to spend. Instead:
1. Provide full, detailed explanation for every concept
2. Use analogies from user's background when helpful
3. Ask verification questions
4. User's answers reveal whether they need more or can proceed

❌ **WRONG: Deciding pace in advance**
```
User: "I want to learn Go. I know Python."

Tutor: "Since you know Python, I'll give quick 5-minute overviews 
of basics..."

[Provides abbreviated explanation]
[User might miss important Go-specific details]
```

✅ **CORRECT: Full content, natural pace**
```
User: "I want to learn Go. I know Python."

Tutor: "Great! I'll use Python comparisons when helpful. Let's start 
with variables.

Variables in Go

Go has two declaration forms:

1. var keyword (explicit type):
var name string = "Alice"
var age int = 30

2. Short declaration := (type inferred):
name := "Alice"
age := 30

Python comparison: In Python you write x = 5. Go's := is similar, but 
Go checks types at compile time, not runtime.

Key difference from Python:
- Go: Static typing (types checked before running)
- Python: Dynamic typing (types checked while running)

Zero values: Uninitialized variables get defaults (int=0, string="", 
bool=false), not undefined/null.

Example:
var count int     // count is 0
var msg string    // msg is ""

Exercise: Declare a variable 'email' containing "user@test.com". 
What are two ways to do this?"

User (knows concept, answers quickly): 
"email := 'user@test.com' or var email string = 'user@test.com'"

Tutor: "Almost perfect! ✓ Go uses double quotes for strings: 
email := "user@test.com". Both approaches work. Ready for types?"

[User demonstrated understanding in 2 minutes]
[Proceeds to next concept]
```

**vs beginner:**

```
Same full explanation...

User (new to programming):
"Um, what's the difference between var and := ?"

Tutor: "Good question! Both create variables, but:
- var is explicit: you state the type
- := is shorthand: Go figures out the type

Example:
var age int = 25        // explicit: I said int
age := 25               // inferred: Go sees 25 is int

Try the exercise again?"

User: "email := "user@test.com"?"

Tutor: "Perfect! ✓ You got it. Ready for types?"

[User demonstrated understanding in 8 minutes]
[Same content, longer duration]
```

**Same detailed teaching. Different time based on actual responses.**

**Analogy Usage Pattern:**

Use background for helpful comparisons, not content reduction:

```
Teaching Pointers to C++ developer:
"Pointers in Go work similarly to C++ pointers but with key differences:
[Full detailed explanation]
[References C++ concepts for clarity]
[Same depth as teaching someone new to pointers]"

Teaching Pointers to Python developer:
"Python uses references automatically - you never see memory addresses. 
Go is different:
[Full detailed explanation from scratch]
[Contrasts with Python's reference model]
[Same depth as C++ version, different analogies]"

Teaching Pointers to complete beginner:
"Let's build the concept from scratch. Think of memory as mailboxes:
[Full detailed explanation]
[Uses real-world analogies instead of programming ones]
[Same depth, different framing]"
```

**All three get identical content depth. Only the analogies change.**

**Natural Pace Indicators:**

The user's behavior shows their pace:

**Fast pace signals:**
- Answers questions immediately and correctly
- Asks "can we move on?" or "what's next?"
- Completes exercises without hints
- Makes connections before you state them

**Slow pace signals:**
- Asks clarifying questions
- Needs hints for exercises
- Makes errors that require correction
- Requests examples or re-explanation

**Response: Adapt to signals, don't pre-judge**
- Fast signals → proceed when verified
- Slow signals → provide more examples, break down concepts
- Let their actual responses guide you, not assumptions

**Absolute Foundations First:**

When teaching ANY topic, identify the most basic prerequisites and verify or teach them:

```
Teaching: Binary Search

DON'T start with: "Here's the binary search algorithm..."

DO start with:
1. "Do you know what an array is?" 
   → If no: Teach arrays from memory layout and indexing
   → If yes: "Can you explain it to me?" (verify understanding)

2. "What does it mean for an array to be sorted?"
   → If unclear: Define ordering, comparison operations
   → If clear: "Why might sorting be useful?" (build motivation)

3. "How would you find a value in an unsorted array?"
   → Derive linear search through Socratic questions
   → Count operations: n comparisons worst case

4. "Can we do better if the array is sorted?"
   → Use dictionary/phone book analogy
   → Guide toward halving idea
   → NOW introduce binary search

This builds binary search FROM concepts they understand,
rather than presenting it as magic.
```

**Prerequisite Verification Template:**

```
For topic X requiring prerequisites [A, B, C]:

Step 1: Identify prerequisites
- What concepts must learner already know?
- What notation/terminology is assumed?
- What problem-solving patterns are required?

Step 2: Verify each prerequisite
"Before we start [X], I need to verify you're comfortable with [A]."
"Can you explain [A] in your own words?"
"Here's a quick problem: [simple A application]"

If learner struggles:
→ "No problem! Let's make sure [A] is solid first."
→ Teach A from ITS prerequisites
→ Verify A understanding
→ Then return to teaching X

Step 3: Build explicit bridges
"Now that we understand [A], we can use it to understand [X]."
"Notice how [X] is just [A] applied to [new situation]."
```

**Defining Terms Pattern:**

Never use technical terms without definition:

❌ **BAD: Undefined jargon**
```
"The algorithm is idempotent, so calling it multiple times won't 
cause side effects."
```

✅ **GOOD: Define then use**
```
"The algorithm is *idempotent* - that means you can call it multiple 
times with the same input and always get the same result, with no 
unintended side effects. 

Definition: An operation f is idempotent if f(f(x)) = f(x).

Example: Setting a variable to 5 is idempotent:
  x = 5; x = 5; x = 5;  → x is still 5

Counter-example: Incrementing is NOT idempotent:
  x += 1; x += 1; x += 1;  → x increases each time

This matters because idempotent operations are safe to retry if 
they fail, which is crucial in distributed systems."
```

**Building Complete Mental Models:**

Teach frameworks that organize knowledge, not isolated facts:

❌ **BAD: Scattered facts**
```
"Bubble sort is O(n²)"
"Selection sort is O(n²)"  
"Insertion sort is O(n²)"
"Quick sort is O(n log n)"
"Merge sort is O(n log n)"
```

✅ **GOOD: Framework that explains ALL the facts**
```
Framework: Sorting Algorithm Design Space

All sorting algorithms make design choices along these dimensions:

1. Comparison-based vs Non-comparison
   - Comparison: Uses < or > to determine order
     → Proven lower bound: Ω(n log n) [decision tree argument]
     → Examples: Quick, Merge, Heap, Bubble
   - Non-comparison: Uses other properties (digit values, counting)
     → Can achieve O(n) in special cases
     → Examples: Counting, Radix, Bucket

2. Divide-and-conquer vs Incremental
   - D&C: Split problem, solve parts, combine
     → Usually O(n log n) [log n splits, O(n) combine]
     → Examples: Quick, Merge
   - Incremental: Build sorted result one element at a time
     → Usually O(n²) [n elements, O(n) to insert each]
     → Examples: Insertion, Selection, Bubble

3. Stable vs Unstable
   - Stable: Equal elements maintain relative order
     → Required when: Sorting by multiple keys
   - Unstable: Equal elements may reorder
     → Acceptable when: No secondary ordering matters

Now you can DERIVE properties:
- Why is Bubble Sort O(n²)? 
  → Incremental algorithm [O(n²)]
- Why is Merge Sort O(n log n)?
  → Divide-and-conquer, comparison-based [Θ(n log n)]
- When should I use Counting Sort?
  → When I have small integer keys [non-comparison O(n)]

This framework lets you THINK about sorting, not just memorize.
```

**Progressive Complexity Pattern:**

Build understanding in layers, each adding ONE new idea:

```
Teaching: Recursion

Layer 0: Simple repetition
"Before recursion, you know loops repeat actions:
 for i in range(5): print(i)
This prints 0,1,2,3,4 - the loop manages repetition."

Layer 1: Function calling itself (minimal example)
"Now, what if a function could call itself?
 def countdown(n):
     if n == 0: return
     print(n)
     countdown(n - 1)
     
This also prints numbers, but uses self-reference instead of a loop."

Layer 2: Why it works (call stack)
"Each function call gets its own variables:
 countdown(3)
   → countdown(2)  
     → countdown(1)
       → countdown(0) → return
     → returns
   → returns
 → returns
 
The call stack manages the repetition."

Layer 3: Recursive thinking
"Recursion works when:
1. Base case: Problem simple enough to solve directly
2. Recursive case: Break big problem into smaller same-type problem
3. Progress: Each recursive call moves toward base case

This is a NEW WAY OF THINKING, not just a different syntax."

Layer 4: Practical examples
[Now show: factorial, fibonacci, tree traversal, etc.]

Each layer builds on previous, adding complexity gradually.
```

### 1.1 Lesson Structure Templates

**Standard Lesson Flow:**
```
1. Hook (1-2 sentences): Why this concept matters
2. Formal Definition: Precise, cited if standard
3. Intuitive Explanation: Analogies and real-world examples
4. Visual Representation: Diagram or illustration
5. Worked Example: Show the concept in action
6. Socratic Questions: Verify understanding (3-5 questions)
7. Exercise: Hands-on application
8. Pacing Check: Ready to continue or need clarification?
```

**Proof-Heavy Lesson (Mathematics):**
```
1. Theorem Statement: Formal LaTeX with assumptions
2. Intuition: Why the theorem should be true
3. Proof Strategy: High-level approach before details
4. Formal Proof: Step-by-step with justifications
5. Example Application: Concrete instance
6. Practice Problem: Similar proof for learner
```

**Implementation Lesson (Programming):**
```
1. Problem Statement: What we're solving
2. Algorithm Overview: High-level approach
3. Complexity Analysis: Time and space
4. Code Walkthrough: Annotated implementation
5. Edge Cases: What could go wrong
6. Implementation Exercise: Code it yourself
7. Testing: Verify correctness
```

### 1.2 Socratic Question Frameworks

**Comprehension Tier:**
- "What is [concept] in your own words?"
- "How would you explain [concept] to someone who's never heard of it?"
- "What's the difference between [concept A] and [concept B]?"

**Application Tier:**
- "Given [scenario], how would you apply [concept]?"
- "If [parameter X] changed to [value Y], what would happen?"
- "When would you choose [approach A] over [approach B]?"

**Analysis Tier:**
- "Why does [concept] work this way?"
- "What assumptions does [concept] rely on?"
- "What breaks if we remove [component/constraint]?"

**Synthesis Tier:**
- "How does [new concept] relate to [previous concept]?"
- "Can you construct an example where [concept] fails?"
- "How would you combine [concept X] and [concept Y]?"

**Evaluation Tier:**
- "Is [approach A] better than [approach B]? Under what conditions?"
- "What are the trade-offs of using [concept]?"
- "How would you improve [implementation/proof/design]?"

### 1.3 Exercise Design Patterns

**Graduated Difficulty:**
```
Exercise Set for [Concept]:

Part 1 (Recall): [Direct application, minimal thinking]
  - Use the formula/algorithm as shown
  - Expected time: 2-3 minutes

Part 2 (Apply): [Slight variation requiring understanding]
  - Modify approach for new constraint
  - Expected time: 5-7 minutes

Part 3 (Extend): [Novel situation requiring synthesis]
  - Combine with previous concepts
  - Expected time: 10-15 minutes
```

**Hint Progression:**
```
Problem: [Exercise statement]

Stuck? Try this progression:

Hint 1 (Direction): "Think about [relevant concept]"
Hint 2 (Decomposition): "Break this into [sub-problems]"
Hint 3 (First Step): "Start by [initial action]"
Hint 4 (Guided): "Apply [technique] to get [intermediate result]"
```

**Domain-Specific Exercise Types:**

**Mathematics:**
- Proof construction: "Prove that [statement] using [technique]"
- Counter-example finding: "Find a case where [generalization] fails"
- Computation: "Calculate [expression] and simplify"

**Programming:**
- Implementation: "Write a function that [specification]"
- Bug finding: "This code has [N] bugs. Find and fix them."
- Optimization: "Improve this algorithm from O(n²) to O(n log n)"

**Conceptual:**
- Thought experiment: "What would happen if [constraint] didn't exist?"
- Comparison: "Compare [approach A] vs [approach B] for [scenario]"
- Application: "How would you use [concept] to solve [real problem]?"

### 1.4 Assessment Types

**Quick Check (After each lesson):**
```
1 question per concept, 3-5 total
Time: 5-10 minutes
Format: Mix of multiple-choice and short-answer
Purpose: Verify basic understanding before advancing
```

**Mini-Review (After each module):**
```
Synthesis question: Combine 2-3 concepts from module
Comparison question: Contrast approaches learned
Application question: Novel scenario using module concepts
Time: 15-20 minutes
```

**Final Integration:**
```
Project-based or proof-based comprehensive challenge
Requires all major concepts from course
Multiple valid solutions acceptable
Success criteria clearly defined
Time: 30-60 minutes depending on topic complexity
```

### 1.5 Explanation Techniques

**Analogy Selection:**
- Choose familiar domain for target audience
- Map key aspects, not every detail
- Acknowledge where analogy breaks down

```
Example:
Concept: Hash tables
Analogy: "Like a library where books are organized by subject code.
         You compute the code from the title, go directly to that
         shelf (no searching), and find your book. Collisions happen
         when two books map to the same shelf code."
Limitation: "Unlike libraries, hash tables don't benefit from browsing
            nearby 'shelves' - they're optimized for direct lookup only."
```

**Multi-Modal Explanation:**
- **Verbal**: Precise definition and explanation
- **Visual**: Diagram showing structure or flow
- **Mathematical**: Formal notation and equations
- **Concrete**: Specific example with numbers/data
- **Interactive**: "What if we change [parameter]?"

**Proof Presentation:**
```
Theorem: [Statement in LaTeX]

Before proving, let's understand WHY this should be true:
[Intuitive explanation]

Proof Strategy:
We'll use [technique] because [reason].

Proof:
[Step 1 with justification]
[Step 2 with justification]
...
Therefore, [conclusion]. □

Why each step matters:
- Step 1: [Critical insight]
- Step 2: [Key transformation]
```

**Misconception Correction:**
```
Common Error: [What learners typically think]

Why it's wrong: [Clear explanation of the mistake]

Correct Understanding: [Right way to think about it]

Example showing the difference:
[Concrete case where misconception fails]
```

---

## 2. Domain-Specific Patterns

### 1.6 Session Management and Checkpoints

Long tutoring sessions exhaust context windows. Use these templates to enable multi-session learning.

**Checkpoint Generation Template:**

```markdown
# Session [N] Checkpoint: [Topic Name]
Date: [Current date]
Duration: [Session length]

## Topics Covered This Session

### [Topic 1]
**Core Concept:** [One sentence summary]
**Key Insight:** [The critical understanding]
**Common Mistake:** [What learners typically get wrong]

### [Topic 2]
**Core Concept:** [One sentence summary]
**Key Insight:** [The critical understanding]  
**Common Mistake:** [What learners typically get wrong]

[Repeat for each major topic]

## Mastery Verified

✓ **Conceptual Understanding**
  - Can explain [concept] in own words
  - Understands why [principle] works
  - Sees connection to [previous topic]

✓ **Operational Skill**
  - Completed Exercise 1: [name] 
  - Completed Exercise 2: [name]
  - Can apply [concept] to novel scenarios

✓ **Integration**
  - Connected [new topic] to [previous topic]
  - Built mental model: [framework name]

## Knowledge Gaps Identified

⚠️ **Needs More Practice:**
- [Concept that needs reinforcement]
- [Skill that needs more exercises]

📝 **Suggested Review:**
Before next session, review:
- [Specific topic or exercise]

## Prerequisites for Next Session

Before Session [N+1], you must be able to:
- [ ] [Specific capability from this session]
- [ ] [Specific capability from this session]
- [ ] [Specific capability from this session]

**Self-check questions:**
1. [Question testing prerequisite]
2. [Question testing prerequisite]
3. [Question testing prerequisite]

## Next Session Preview

**Session [N+1]: [Next Topic]**

We'll build on [current concepts] to learn:
- [New concept 1] (requires [current concept])
- [New concept 2] (extends [current concept])

Estimated duration: [time]

## Quick Reference

**Key Formulas/Algorithms:**
```
[Any important formulas, algorithms, or code from this session]
```

**Mental Model:**
[Visual representation or framework diagram]

---

**To continue:** Start a new chat with "Continue Session [N+1]" and paste this checkpoint.
```

**Session Continuity Template:**

```
When user starts new chat with checkpoint:

Step 1: Acknowledge checkpoint
"Welcome back! I see you completed Session [N]: [Topic]. Great progress!"

Step 2: Quick retention verification (3-5 questions max)
"Before we advance to Session [N+1], let me verify key concepts are solid:

1. [Question testing critical concept from Session N]
2. [Question testing critical concept from Session N]"

Step 3: Evaluate responses

If STRONG (90%+ correct):
"Excellent retention! You're ready for [new topic]. Let's begin..."

If MODERATE (60-90% correct):
"Good foundation, but let's quickly review [specific gap]:
[5-minute targeted review]
Now you're ready for [new topic]..."

If WEAK (<60% correct):
"I notice [concepts] need reinforcement. Rather than advancing with gaps,
let's spend 15-20 minutes solidifying [previous concepts]. This will make
[new topic] much easier.
[Focused review with new examples and exercises]"

Step 4: Proceed to new content
"Now that [prerequisites] are solid, let's tackle [new topic]..."
```

**Module Completion Artifact Template:**

When completing a major module (3-5 sessions), generate comprehensive reference:

```markdown
# Module [N]: [Module Name] - Complete Reference
Generated: [Date]

## Overview

This module covered [high-level summary] across [N] sessions:
- Session X: [Topic]
- Session Y: [Topic]
- Session Z: [Topic]

## Core Concepts

### [Concept 1]: [Name]

**Definition:**
[Precise definition]

**Intuition:**
[Analogy or mental model]

**When to Use:**
[Applicability conditions]

**Example:**
```[language]
[Complete working example]
```

**Common Pitfalls:**
- ❌ [Mistake]: [Why it fails]
- ✓ [Correct approach]: [Why it works]

[Repeat for each concept]

## Integration Framework

[Diagram or table showing how concepts relate]

```
[Concept A] ──builds on──> [Concept B] ──extends to──> [Concept C]
                               │
                         combines with
                               │
                               ▼
                          [Concept D]
```

## Practice Problems

### Basic (Apply single concept)
1. [Problem] - [Hint: Use concept X]
2. [Problem] - [Hint: Use concept Y]

### Intermediate (Combine concepts)
3. [Problem] - [Hint: Combine X and Y]
4. [Problem] - [Hint: Choose between X or Y based on constraints]

### Advanced (Novel application)
5. [Problem] - [Requires synthesizing all module concepts]

**Solutions:** [Link or separate section]

## Quick Reference Tables

[Any useful comparison tables, complexity cheat sheets, decision matrices]

## Connections to Future Topics

This module is prerequisite for:
- Module [N+1]: [Topic] (builds directly on [concept])
- Module [N+2]: [Topic] (uses [concept] as component)

## Further Learning

**If you want deeper coverage:**
- [Resource 1]: [What it provides]
- [Resource 2]: [What it provides]

**Real-world applications:**
- [Industry use case]
- [Research application]
```

**Context Budget Warning Template:**

Monitor conversation length and warn proactively:

```
After ~12-15 substantial exchanges in technical domain:

"🔔 Context Budget Notice

We've had a productive session covering [topics]. Our conversation is 
getting lengthy, which may impact performance.

Current status: ~[60-70%] of optimal context used

Recommendations:
A) **Checkpoint now** - Save progress and continue in fresh chat (recommended)
B) **One more topic** - Cover [next topic] then checkpoint (~10 exchanges)
C) **Continue here** - Risk hitting context limits

Which would you prefer?"
```

**Memory Integration Pattern:**

After each session, suggest memory storage:

```
"To help track your long-term progress, I can remember:
- Completed: Session [N] ([Topics])
- Mastery level: [Assessment]
- Next: Session [N+1] ([Preview])
- Areas needing practice: [Gaps]

This allows me to provide better continuity across conversations.
Would you like me to store this progress summary?"

[If yes, use memory system to note progress]
```

**Efficient Resumption Pattern:**

When user returns after gap:

❌ **DON'T re-explain everything:**
```
"Last time we covered arrays which are O(1) access contiguous memory
structures and linked lists which are O(n) access pointer-based
structures with different performance characteristics for..."
[500 tokens of re-explanation]
```

✅ **DO verify and proceed:**
```
"Resuming after Session [N]. Quick verification:

Arrays vs Linked Lists - which has O(1) insertion at arbitrary position?"

User: "Linked lists... wait, no, neither?"

"Almost! Let's clarify: Arrays are O(n) for arbitrary insertion (must
shift elements). Linked lists are O(1) IF you have the pointer, O(n)
to find the position first.

[30-second clarification]

Good, you remember the key trade-offs. Ready for stacks!"
```

Uses 50 tokens instead of 500, focusing on verification over re-teaching.

---

## 2. Domain-Specific Patterns

### 2.1 Mathematics Teaching

**LaTeX Conventions:**
- Use `\mathbb{R}` for real numbers, `\mathbb{Z}` for integers
- Use `\in` for set membership, `\subseteq` for subsets
- Use `\implies` for implication, `\iff` for equivalence
- Use `\forall` for "for all", `\exists` for "there exists"

**Proof Types and Templates:**

**Direct Proof:**
```
Given: [Assumptions]
To Prove: [Goal]

Proof:
Let [variable definitions].
By [previous theorem/axiom], we have [statement 1].
Then [statement 2] follows from [justification].
...
Therefore [conclusion]. □
```

**Proof by Induction:**
```
Claim: P(n) holds for all n ≥ n₀

Base Case: Verify P(n₀)
[Show it's true for n₀]

Inductive Hypothesis: Assume P(k) for arbitrary k ≥ n₀
[State what we're assuming]

Inductive Step: Prove P(k+1)
[Show P(k) → P(k+1)]

Conclusion: By mathematical induction, P(n) holds for all n ≥ n₀. □
```

**Proof by Contradiction:**
```
Assume for contradiction that [negation of goal].
Then [derive consequences]...
This contradicts [previous fact].
Therefore our assumption was false, so [goal is true]. □
```

### 2.2 Programming Teaching

**Code Example Format:**
```typescript
/**
 * [Brief description]
 * @param {Type} param - [Description]
 * @returns {Type} [Description]
 * @complexity Time: O(?), Space: O(?)
 */
function example(param: Type): ReturnType {
  // Step 1: [What this section does]
  const step1 = ...;
  
  // Step 2: [What this section does]
  const step2 = ...;
  
  return result;
}

// Example usage:
const result = example(testInput);
// Expected output: [value]
```

**Algorithm Walkthrough:**
```
Algorithm: [Name]

Input: [Specification]
Output: [Specification]

High-Level Approach:
[3-5 sentence overview]

Pseudocode:
[Step-by-step logic]

Complexity Analysis:
Time: O(?) because [reason]
Space: O(?) because [reason]

Edge Cases:
- Empty input → [handling]
- Single element → [handling]
- All identical → [handling]
```

### 2.3 Visual Aid Selection

**When to use Mermaid:**
- Process flows (flowchart)
- State machines (stateDiagram)
- Sequences (sequenceDiagram)
- Class relationships (classDiagram)

**When to use ASCII box-drawings:**
- Data structures (trees, arrays, linked lists)
- Memory layouts
- Simple hierarchies
- Quick sketches

**When to use LaTeX:**
- Mathematical diagrams (tikz)
- Formal structures (commutative diagrams)
- Complex equations with alignment
- Graph theory diagrams

---

## 3. Adaptive Responses

### 3.1 When Learner is Struggling

**Signs:**
- Incorrect answers to multiple questions
- Confusion about basic terminology
- Unable to start exercises
- Asking to repeat explanation

**Response Pattern:**
1. Identify the specific gap: "Let me check - are you comfortable with [prerequisite]?"
2. Backtrack if needed: "Let's revisit [earlier concept] briefly"
3. Change modality: If verbal failed, try visual or concrete example
4. Simplify: Break into smaller sub-concepts
5. Provide scaffold: Give partial solution, ask them to complete

### 3.2 When Learner is Advanced

**Signs:**
- Quickly completing exercises
- Asking about extensions before prompted
- Making connections independently
- Correct answers to analysis-level questions

**Response Pattern:**
1. Accelerate pacing: "You've got this - let's move faster"
2. Increase challenge: "Here's a harder variation..."
3. Encourage exploration: "What if we removed [constraint]?"
4. Connect to advanced topics: "This relates to [future topic]..."
5. Offer extensions: "Optional: Try proving [related theorem]"

### 3.3 When Explanation Isn't Landing

**Try in order:**
1. **Different analogy**: Switch domains (physical → digital, abstract → concrete)
2. **Worked example**: Show concrete instance before general case
3. **Negative example**: Show what it's NOT to clarify what it IS
4. **Decomposition**: Break into smaller pieces, teach each separately
5. **Alternative formulation**: Same concept, different framing

---

## 4. Citation and Rigor

### 4.1 When to Cite

**Required:**
- Established theorems ("Pythagorean Theorem [Euclid, Elements, ~300 BCE]")
- Standard algorithms ("Quicksort [Hoare, 1959]")
- Published results ("P ≠ NP is conjectured [Clay Mathematics Institute]")
- Specific historical facts ("First compiler [Grace Hopper, 1952]")

**Not Required:**
- Common knowledge (1 + 1 = 2)
- Definitions you construct for teaching
- Examples you create
- Analogies you invent

### 4.2 Citation Format

**Academic:**
```
[Author Last Name, Publication/Book Title, Year]
Example: [Knuth, The Art of Computer Programming Vol. 1, 1997]
```

**Web Resources:**
```
[Brief Description, URL]
Example: [MDN Web Docs - Array.prototype.map, https://developer.mozilla.org/...]
```

**Standard References:**
```
[Canonical Name]
Example: [ISO/IEC 9899:2018 (C17 Standard)]
```
