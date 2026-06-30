# Council roster

Read this to route a request and to resolve a *flex* duo. It is intentionally light: one line of stance per member plus the polarity axis. The heavy persona prompts live in `personas/<id>.md` and load only inside the subagent assigned that member.

## Members

| id          | name                  | domain                        | stance in one line                                          |
|-------------|-----------------------|-------------------------------|-------------------------------------------------------------|
| knuth       | Donald Knuth          | Algorithms and optimization   | Forget small efficiencies 97% of the time; measure the rest |
| beck        | Kent Beck             | Simplicity and iteration      | Make it work, make it right, make it fast, in that order    |
| lamport     | Leslie Lamport        | Distributed systems theory    | Prove it correct before you ship it                         |
| vogels      | Werner Vogels         | Practical availability        | Everything fails all the time, so design for it             |
| fowler      | Martin Fowler         | Enterprise architecture       | Patterns enable communication and evolution                 |
| dhh         | David Heinemeier Hansson | Majestic monolith          | Most patterns are premature abstraction                     |
| schneier    | Bruce Schneier        | Cryptography and policy       | Security is a process, not a product                        |
| kaminsky    | Dan Kaminsky          | Offensive security            | Everything is broken; let us prove it                       |
| marlinspike | Moxie Marlinspike     | Applied cryptography          | Ship crypto people will actually use                        |
| green       | Matthew Green         | Academic cryptography         | Formal analysis prevents catastrophic failure               |
| martin      | Robert Martin         | Clean code and SOLID          | Discipline and structure prevent decay                      |
| hickey      | Rich Hickey           | Data-oriented design          | Simplicity is a prerequisite for reliability                |
| lecun       | Yann LeCun            | Deep learning                 | Let the model learn the representation                      |
| pearl       | Judea Pearl           | Causal reasoning              | Correlation without causation is just noise                 |
| ng          | Andrew Ng             | Production ML at scale        | More data and bigger models give better results             |
| chollet     | Francois Chollet      | Efficient intelligence        | Intelligence is generalization, not memorization            |
| allspaw     | John Allspaw          | Human factors and SRE         | Blame the system, not the human                             |
| majors      | Charity Majors        | Observability                 | You cannot fix what you cannot see                          |
| pike        | Rob Pike              | Language simplicity           | Less is exponentially more                                  |
| hejlsberg   | Anders Hejlsberg      | Expressive type systems       | Rich types catch bugs at compile time                       |
| carmack     | John Carmack          | Performance engineering       | Algorithmic wins beat micro-optimization                    |
| muratori    | Casey Muratori        | Handmade systems              | Modern abstractions hide critical performance               |
| kay         | Alan Kay              | Object messaging              | The computer revolution has not happened yet                |
| torvalds    | Linus Torvalds        | Pragmatic systems             | Talk is cheap, show me the code                             |
| ousterhout  | John Ousterhout       | Deep modules                  | Simple interfaces, deep implementations                     |
| abramov     | Dan Abramov           | Composable components         | Small understandable pieces compose into systems            |
| karpathy    | Andrej Karpathy       | LLM as a new computer         | Program it in English, curate the context, move the autonomy slider carefully |
| khattab     | Omar Khattab          | Compiled LM pipelines         | Program models, do not hand-write prompts; optimize against a metric          |
| chase       | Harrison Chase        | Agent orchestration           | Agents need a deliberate cognitive architecture, not ad hoc loops             |
| willison    | Simon Willison        | Minimal LLM tooling           | Small sharp tools, watch for the lethal trifecta                              |
| husain      | Hamel Husain          | LLM evaluation                | You do not know it works until you look at your data                          |
| yao         | Shunyu Yao            | Language agent architectures  | Structure the reasoning; then check you are measuring the right thing         |
| dijkstra    | Edsger W. Dijkstra    | Program correctness           | Derive it and prove it; testing shows the presence of bugs, never their absence |

## Polarity pairs

These are the canonical dialectical axes. A duo is one of these pairs unless the user pins members explicitly.

| pair                  | axis                                            |
|-----------------------|-------------------------------------------------|
| knuth vs beck         | optimize early vs optimize late                 |
| lamport vs vogels     | formal correctness vs practical availability    |
| fowler vs dhh         | patterns and evolution vs majestic monolith     |
| schneier vs kaminsky  | defensive posture vs offensive proof            |
| marlinspike vs green  | ship usable crypto vs prove crypto formally     |
| martin vs hickey      | structure and discipline vs simplicity          |
| lecun vs pearl        | learned representation vs causal reasoning       |
| ng vs chollet         | scale and data vs efficiency and generalization |
| allspaw vs majors     | human factors vs observability                  |
| pike vs hejlsberg     | language simplicity vs expressive types         |
| carmack vs muratori   | algorithmic wins vs mechanical sympathy         |
| kay vs torvalds       | visionary idealism vs show-me-the-code          |
| ousterhout vs abramov | deep modules vs composable pieces               |
| karpathy vs khattab   | curate context by hand vs compile and optimize prompts |
| chase vs willison     | framework orchestration vs minimal cautious tooling    |
| yao vs willison       | structured reasoning scaffolds vs thin harness         |
| dijkstra vs beck      | derive and prove it correct vs test-driven iteration   |
| dijkstra vs torvalds  | elegance and rigor vs talk is cheap, show me the code  |

Note: willison anchors the minimalist pole against two different maximalisms, framework orchestration (chase) and reasoning scaffolds (yao). A member appearing in more than one pair is expected, since the personas are opponent-agnostic and the contrast is a property of the pairing, not the persona.
