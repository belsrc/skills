# Content-pattern catalog: CP-1 through CP-15

Full before/after examples for each pattern in the SKILL.md summary table. These apply in every mode. In Pragmatic/Strict mode, the "after" examples below stay inside the structural rules (no contractions, approved modals, active voice) — see the note under each pattern where that matters. In Voice mode, the structural constraint drops away; write the "after" as naturally as the example shows.

---

## CP-1: Inflated significance / legacy language

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** Puffs up importance by claiming an arbitrary fact represents or contributes to a broader trend, without evidence for the trend itself.

**Before:** The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.

**After:** The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

---

## CP-2: Notability / media-coverage puffery

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Problem:** Claims notability by listing sources without giving any specific content from them.

**Before:** Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After:** In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

---

## CP-3: Superficial "-ing" tacked-on analysis

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** A present-participle phrase gets tacked onto a sentence to add the appearance of depth without adding a fact. Related to Rule 3.5, which bans "-ing" as a verb outright in Pragmatic/Strict mode; this pattern also catches grammatical participial clauses that add no information, which Rule 3.5 alone would not flag.

**Before:** The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**After:** The temple uses blue, green, and gold. The architect said these colors reference local bluebonnets and the Gulf coast.

---

## CP-4: Promotional and advertisement-like language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** Keeping a neutral tone is hard for LLMs, especially on "cultural heritage" topics — travel-brochure language creeps into encyclopedic or technical text.

**Before:** Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:** Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

---

## CP-5: Vague attributions and weasel words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few are actually cited)

**Problem:** Opinions get attributed to unnamed authorities instead of a specific, checkable source.

**Before:** Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**After:** The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

---

## CP-6: Formulaic frames — "Challenges and Future Outlook" sections, generic upbeat conclusions

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook, The future looks bright, Exciting times lie ahead, represents a major step forward

**Problem:** Two symptoms of the same cause: LLMs default to a formulaic "problems, then optimism" shape even when the source material does not support either half.

**Before (formulaic challenges section):** Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.

**After:** Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.

**Before (generic conclusion):** The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

**After:** The company plans to open two more locations next year.

---

## CP-7: Copula avoidance

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Problem:** LLMs substitute elaborate constructions for the simple copulas "is" and "are" and for "has".

**Before:** Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After:** Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

---

## CP-8: Negative parallelisms

**Problem:** Constructions like "Not only...but..." or "It's not just about..., it's..." are overused as a substitute for actually stating the point.

**Before:** It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**After:** The heavy beat adds to the aggressive tone.

Pragmatic/Strict note: "it's" is also a contraction (Rule 4.2 violation) independent of this pattern — in that mode expand to "it is" before you even get to the negative-parallelism fix, or just delete the construction as shown.

---

## CP-9: Rule of three overuse

**Problem:** Ideas get forced into groups of three to appear comprehensive, whether or not there are really three distinct things to say.

**Before:** The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:** The event includes talks and panels. There's also time for informal networking between sessions.

Pragmatic/Strict note: "There's" is a contraction — write "There is" instead.

---

## CP-10: Elegant variation (synonym cycling)

**Problem:** Repetition-penalty behavior causes excessive synonym substitution for the same entity across a passage.

**Before:** The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:** The protagonist faces many challenges but eventually triumphs and returns home.

Note: in Pragmatic/Strict mode this is already required by Rule 1.11 (one item, one name) and Rule 9.4 (consistent terminology) — you do not need a separate check, the structural rules already forbid it. This pattern exists in the catalog for Voice mode, where nothing else would catch it.

---

## CP-11: False ranges

**Problem:** "From X to Y" constructions imply X and Y sit on a meaningful scale when they do not.

**Before:** Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After:** The book covers the Big Bang, star formation, and current theories about dark matter.

---

## CP-12: Formatting tells

Six related symptoms, grouped because they are all formatting-level rather than word-level:

**Em dash overuse.** Legal punctuation under Rule 8.1, but LLMs use it far more than humans, mimicking "punchy" sales writing.

**Before:** The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.
**After:** The term is primarily promoted by Dutch institutions, not by the people themselves. You do not say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

**Mechanical boldface.** Phrases get emphasized in boldface by default rather than for actual emphasis.

**Before:** It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.
**After:** It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

**Inline-header vertical lists.** List items start with a bolded header and colon instead of just stating the point.

**Before:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:** The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

**Title Case Headings.** Capitalizing every main word in a heading.

**Before:** `## Strategic Negotiations And Global Partnerships`
**After:** `## Strategic negotiations and global partnerships`

**Emoji decoration.** Emoji used to decorate headings or bullets instead of conveying information.

**Before:**
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting

**After:** The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.

**Curly quotation marks.** Curly quotes ("...") in place of straight quotes ("...").

**Before:** He said "the project is on track" but others disagreed.
**After:** He said "the project is on track" but others disagreed.

This last one is also an Untouchables concern near code: never let a smart-quote autocorrect touch a string that appears in a code block, command, or quoted error, since `'` and `'` are not interchangeable to a parser.

---

## CP-13: Collaborative communication artifacts

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

**Problem:** Text written as chatbot correspondence gets pasted directly into delivered content.

**Before:** Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After:** The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

---

## CP-14: Knowledge-cutoff disclaimers

**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...

**Problem:** Disclaimers about the model's own incomplete information get left in delivered text instead of being resolved or removed.

**Before:** While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**After:** The company was founded in 1994, according to its registration documents.

If the fact genuinely cannot be verified, say so plainly ("The founding date is not documented.") rather than hedging around it.

---

## CP-15: Sycophantic / servile tone

**Problem:** Overly positive, people-pleasing language that praises the reader instead of stating substance.

**Before:** Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**After:** The economic factors you mentioned are relevant here.

---

## Full worked example (Pragmatic mode)

**Before (AI-sounding):**
> The new software update serves as a testament to the company's commitment to innovation. Moreover, it provides a seamless, intuitive, and powerful user experience—ensuring that users can accomplish their goals efficiently. It's not just an update, it's a revolution in how we think about productivity. Industry experts believe this will have a lasting impact on the entire sector, highlighting the company's pivotal role in the evolving technological landscape.

**After (STE + content patterns applied):**
> The software update adds batch processing, keyboard shortcuts, and offline mode. In beta testing, most users completed tasks faster than with the previous version.

**Changes made:** copula avoidance fixed (CP-7); "Moreover" deleted (AI vocabulary, see vocabulary.md); rule-of-three "seamless, intuitive, and powerful" deleted (CP-9) along with the promotional language (CP-4); em dash and "-ing" clause removed (CP-3, and Rule 3.5 in Pragmatic mode); negative parallelism removed (CP-8); vague attribution "industry experts believe" removed (CP-5); "pivotal role" and "evolving landscape" removed (significance inflation, CP-1, and AI-vocabulary, see vocabulary.md); specific features and a concrete result substituted for all of it; contractions expanded per Rule 4.2.

## Reference

CP-1 through CP-9 and CP-12 through CP-15 are adapted from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. The patterns there come from observations of thousands of instances of AI-generated text on Wikipedia. CP-10 and CP-11 are adapted from the same source. Key insight quoted there: LLMs use statistical algorithms to guess what should come next, so the result tends toward the most statistically likely output across the widest variety of cases — which is exactly what produces these patterns.
