# Weekly Research Progress Report — Lecture Rating Matrix

Hamza Mehmood — prepared for Professor Maaz Amjad — September 9, 2026

## 1. Purpose of This Week's Test

Week 1 tested the rubric on a single lecture — MIT's 6.100L, Lecture 1 — which is useful as a sanity check but doesn't say much about whether the matrix generalizes. This week I ran the same rubric on three lectures from a different course entirely: Howard University's CSCI 100, an intro computer science course that posts every lecture on YouTube with a public schedule on its own course site. I picked lectures on purpose to vary in type: one clearly implementation-heavy topic, one mixed conceptual/implementation topic, and one that the course schedule labeled as a soft, non-technical topic (ethics). That third pick turned out to matter more than expected.

## 2. Method

All three come from the CSCI100 Fall '21 YouTube channel, chosen from the lecture-by-lecture schedule posted on the course's own site:

1. *2-Dimensional Lists, Nested For Loops, Images* — youtube.com/watch?v=hEh_6otWzNs
2. *Classes, Attributes, Object-Oriented Programming* — youtube.com/watch?v=l_n_7mOqqjs
3. *Computer Science Ethics* (as labeled on the course schedule) — youtube.com/watch?v=U8M4DlCE2ms

Same limitation as Week 1: this environment can't reach YouTube's caption endpoints directly, so transcripts came from a third-party transcript tool rather than `lecture_rating_pipeline.py` itself — the scores below are hand-applied rubric scoring, not the automated Stage 3 judge. Each lecture was scored against the same four-dimension matrix from the Week 1 report (Topic Coverage, Examples, Implementation, Delivery & Structure), scoring conservatively — anything not clearly shown in the transcript was scored low rather than assumed.

## 3. Results at a Glance

| Lecture | Coverage | Examples | Implementation | Total |
|---|---|---|---|---|
| 2D Lists / Nested Loops | 3.5 / 3.5 | 2.0 / 2.0 | 2.0 / 3.0 | 9.0 / 10 |
| Classes / OOP | 3.5 / 3.5 | 2.0 / 2.0 | 2.5 / 3.0 | 9.0 / 10 |
| "CS Ethics" (announcements clip) | 0.0 / 3.5 | 0.0 / 2.0 | 0.0 / 3.0 | 1.0 / 10 |

## 4. Lecture-by-Lecture Detail

**2D Lists, Nested For Loops, Images.** Topic Coverage scored a full 3.5 because the lecture explicitly ties back to earlier material (lists, loops) before introducing the new idea. Examples scored close to full marks: a single running example — a classroom seating chart — is walked through step by step rather than just stated. Implementation lost the most ground: real Python syntax is shown (indexing an entry like `seating[0][1]`), but nothing in the transcript shows the code actually being executed with visible output, so correctness couldn't be confirmed. Delivery & Structure scored full marks, including credit for practice problems that ask students to identify specific indices — a concrete form of engagement.

**Classes, Attributes, OOP.** This lecture handled coherence especially well: it opens by reviewing data types students already know before making the case that none of them cleanly represent something with several bundled properties. The example — a role-playing-game character — is carried through the whole lecture: creating an instance, reading attributes, calling a method. Implementation scored slightly higher than Lecture 1 (2.5 vs. 2.0) because more syntax gets shown across the lecture. Delivery & Structure is weaker here — nothing in the transcript points to a question posed to the class, so the engagement sub-criterion scored zero.

**"Computer Science Ethics" (as scheduled).** This is the one that actually taught something. The video the course schedule links for "Computer Science Ethics" is not the ethics lecture — it's a short administrative segment covering project deadlines, a guest-speaker announcement, and a recruiting event. Howard splits each class period into multiple numbered video segments on YouTube (an announcements clip, then the lecture content), and the public schedule links the first segment rather than the one that covers the stated topic. The rubric doesn't know that context — it just read a transcript with no ethics content and scored accordingly: zero across Topic Coverage, Examples, and Implementation. This 1.0/10 is not the matrix being unfair to a real lecture; it's the matrix correctly refusing to invent content that isn't there.

## 5. What This Changes About the Pipeline

Lecture 3 exposed a gap the MIT pilot never surfaced: nothing in the pipeline currently checks whether a given video actually contains lecture content before scoring it. A course's public schedule can point to the wrong clip, and without a check, the pipeline could produce a very low score for a lecture that might actually be fine — with no way for someone reading the output to tell "badly taught" apart from "wrong video." A reasonably cheap fix is a content-check step between Stage 1 (transcript acquisition) and Stage 2 (signal extraction): compare transcript length against the course's typical lecture length, and run a quick keyword check against the syllabus topic before running the full rubric.

Outside of that, the two real content lectures held up well — both scored 9.0/10, for reasons that trace back to specific, checkable things in the transcript rather than a vague overall impression.

## 6. Limitations Still Open

Transcripts here are summarized by a third-party tool, not raw captions, so Examples and Implementation sub-scores are lower-bound estimates. No syllabus text for CSCI 100 was available, so Topic Coverage was judged against the schedule's one-line topic description rather than a real keyword-overlap check. Lecture 3 adds the content-verification gap described above, which wasn't a known issue before this week.

## 7. Next Steps

Get raw captions flowing into `lecture_rating_pipeline.py` directly instead of hand-copying transcript summaries — blocked on network access from the current environment, likely needs to happen from a personal machine. Add the content-check step described above before Stage 2. Once both are in place, run these same three Howard lectures through the automated Stage 3 LLM judge and compare its scores against the hand-scores here — the first real test of Stage 4 (human calibration).
