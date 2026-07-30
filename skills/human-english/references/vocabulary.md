# Master vocabulary substitution table

Everything here is merged from two sources: the `simple-english` skill's slop-to-simple table (structural precedence — these are the substitutions to make in Pragmatic/Strict mode) and the `humanizer` skill's AI-vocabulary and promotional-language lists (content-pattern layer — these apply in every mode, including Voice). Overlaps between the two source lists (for example "vibrant" appeared in both) are listed once.

None of this is the official ASD-STE100 dictionary (~900 approved words, ~1,200 banned words), which is copyrighted by ASD and not reproduced here. Its mechanics apply without it: **one word, one meaning, one part of speech.** For full Strict-mode compliance, use the official dictionary at asd-ste100.org.

## Filler and hedging: delete or replace

This table is ours, not the ASD dictionary. It maps words that both AI-generated docs and AI-generated prose overuse to plain replacements. If the word carries no fact, delete it instead of replacing it.

| Slop | Write instead |
|---|---|
| leverage, utilize | use |
| in order to | to |
| prior to | before |
| ensure | make sure that |
| it is worth noting that | (delete) |
| it's important to, crucially | (delete — state the fact) |
| simply, just, easily, seamlessly, effortlessly | (delete) |
| robust, powerful, comprehensive, performant | (delete, or give the measurable property) |
| functionality | function, feature |
| enables you to, allows you to | you can |
| is designed to, aims to | (delete — say what it does) |
| facilitate | help, make possible |
| dive into, delve into | read, examine |
| when it comes to | for |
| in the event that | if |
| due to the fact that | because |
| as needed, as necessary | (state the condition) |
| and/or | Pick one, or write "X, or Y, or both" |
| e.g. / i.e. / etc. | for example / that is / (name the items) |
| gracefully handles | (say what it does: "retries three times, then stops") |
| out of the box | by default |
| under the hood | internally |
| blazingly fast, state-of-the-art | fast (give the number) / (delete) |
| streamline | make simpler, make faster |
| plethora, myriad | many |
| addresses the issue, tackles | corrects the fault, removes the error |
| could potentially possibly, might arguably | (delete the hedge stack — state the claim or drop it) |

## AI-vocabulary words

These words appear far more frequently in post-2023 text than in human baselines and often co-occur in clusters. None of them are banned outright — the fix is to ask whether the sentence still means something after you delete the word. Usually it does.

Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun, as in "the evolving landscape"), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant

**Before:** Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After (Voice mode):** Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

## Promotional and inflated-significance language

**Promotional/advertisement words** (CP-4): boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Significance-inflation phrases** (CP-1): stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Notability puffery** (CP-2): independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Vague-attribution openers** (CP-5): Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few are actually cited)

## Copula avoidance (CP-7)

LLMs substitute elaborate constructions for the simple verbs "is", "are", and "has".

| Instead of | Write |
|---|---|
| serves as, stands as, marks, represents [a] | is |
| boasts, features, offers [a] | has |

**Before:** Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.
**After:** Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

## The modal ladder (Pragmatic / Strict — see also SKILL.md Section 3)

| You wrote | STE writes |
|---|---|
| should (requirement) | must |
| should (recommendation) | Delete it, or state it as fact: "X is better because Y." |
| may / might / could (possibility) | can |
| may (permission) | can |
| would (hypothetical) | Restructure: "If X occurs, Y occurs." |

## Consistency pass (Rules 1.11, 9.4 — also applies in Voice mode via CP-10)

Collapse these common rotations to one term each:

- check / verify / confirm / validate / ensure → pick one
- config / configuration / settings / options → pick one
- delete / remove / drop / destroy → one per meaning, kept consistent
- error / issue / problem / failure → "error" for errors, "failure" for failed operations
- run / execute / invoke / launch → pick one
- show / display / render / present → pick one

## Known part-of-speech rulings (Strict mode, useful as patterns)

| Word | Ruling |
|---|---|
| test, check, work | Noun only. "Do a test", not "test the pump". "Check that X" becomes "make sure that X". |
| oil | Noun only as used in STE examples. For the verb, the dictionary gives "lubricate". |
| help | Verb only. For the noun, the dictionary gives "aid": "with the aid of". |
| fall | "To move down by gravity" only, never "decrease". |
| follow | "To come after" only, never "obey". Write "obey the instructions". |
| above, below | Physical positions only. For limits write "more than", "less than". |
