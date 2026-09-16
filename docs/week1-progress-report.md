# Weekly Research Progress Report — Developing a Lecture-Quality Rating Matrix

**Volunteer researcher:** Hamza Mehmood
**Supervising faculty:** Professor Maaz Amjad
**Reporting period:** Week 1 — Wednesday, August 27, 2026
**Status:** On track — rubric designed, pipeline built, pilot walkthrough completed

---

## 1. Task as Assigned

Professor Maaz asked for a matrix to rate the quality of lectures delivered by an instructor. As a starting point, the method is to: (1) pull lectures from YouTube, (2) obtain a transcript of each one, and (3) score the lecture on how thoroughly it covers its stated topic, how many examples it gives, and how much implementation/practical demonstration it includes, on a scale of 1–10.

This report covers Week 1: the rubric design, the transcript-to-score pipeline, and a first walkthrough on one real, published lecture to sanity-check the method before scaling it up.

## 2. Grounding in Professor Maaz's Prior Work

Before designing the matrix, I read two of Professor Maaz's recent papers on LLM-based, rubric-driven evaluation of student work, since the same design pattern applies directly to rating lectures:

- Haseeb, Hmue, Amjad, Amjad & Sheng (2026), *"Toward Cross-Domain Automated Feedback,"* BEA Workshop — evaluates LLM feedback across programming, writing, and math using a 6-criterion binary rubric (Accuracy / Selectivity / Clarity, split across Diagnosis and Guidance), compares a single unified prompt against a multi-agent pipeline, and finds the unified prompt matches or beats multi-agent decomposition on well-defined, single-domain tasks.
- Haseeb, Amjad, Amjad & Sheng (2026), *"From Code to Rubrics,"* ACM WWW Companion — uses the same binary-criteria rubric style (Table A.1: EA/ES/EC/FA/FS/FC) for judging programming feedback, and shows that a "J1-style" judge — one that reasons step-by-step before scoring — agrees with human raters noticeably better than a judge that scores directly.

Two design choices carry over directly into the lecture-rating matrix: (a) break the overall score into a small number of named dimensions, each with 2–4 binary or graded sub-criteria that sum to a point cap, rather than one holistic 1–10 guess; and (b) when an LLM is used to apply the rubric, have it reason through the transcript against each criterion before outputting a score, rather than asking for the number directly.

## 3. Proposed Rating Matrix (v1)

The matrix scores a lecture out of 10 across four weighted dimensions. Each dimension is broken into sub-criteria so the score is auditable — anyone can see exactly why a lecture got the number it got, and disagreements can be resolved criterion-by-criterion instead of re-arguing the whole score.

| Dimension | Code | Sub-criterion | What it measures | Max |
|---|---|---|---|---|
| **1. Topic Coverage** (3.5 pts) | TC1 | Scope match | Lecture addresses the topics scheduled for that session | 1.0 |
| | TC2 | Depth | Sub-concepts are explained, not just named | 1.0 |
| | TC3 | Accuracy | Content presented is technically correct | 1.0 |
| | TC4 | Coherence | Topics build logically on stated prerequisites | 0.5 |
| **2. Examples** (2.0 pts) | EX1 | Presence | At least one worked example per major concept | 1.0 |
| | EX2 | Variety | Examples vary in context/difficulty, not repetitive | 0.5 |
| | EX3 | Clarity | Examples are walked through step-by-step, not just stated | 0.5 |
| **3. Implementation** (3.0 pts) | IM1 | Presence | Live coding, demo, or applied walkthrough is shown | 1.5 |
| | IM2 | Correctness | What is shown/coded actually runs and does what is claimed | 1.0 |
| | IM3 | Connection | Implementation is tied back to the underlying concept | 0.5 |
| **4. Delivery & Structure** (1.5 pts) | DS1 | Framing | Clear intro/roadmap and a closing summary or recap | 0.5 |
| | DS2 | Pacing & clarity | Explanation pace and language are appropriate for the level | 0.5 |
| | DS3 | Engagement | Questions, prompts, or checks for understanding are used | 0.5 |

**Notes on the design:**

- Topic Coverage and Implementation are weighted heaviest (3.5 and 3.0) because they were the two things Professor Maaz specifically named.
- Delivery & Structure is included at a lower weight (1.5) because a lecture that is accurate and hands-on but poorly organized should still lose some points — but it shouldn't dominate the score the way content and implementation do.
- A lecture's expected shape depends on where it sits in a course (e.g., a first, conceptual lecture is not supposed to have much live coding). Section 5 flags this as something the matrix needs to account for before scores are compared across lectures.

## 4. Methodology: Transcript-to-Score Pipeline

Proposed four-stage pipeline, mirroring the annotation approach in Professor Maaz's papers (defined criteria → automated first pass → human-calibrated ground truth):

**Stage 1 — Transcript acquisition.** Pull the official captions for a lecture (YouTube Data/timedtext API or `yt-dlp`), falling back to Whisper speech-to-text when a video has no captions. Implemented in [`lecture_rating_pipeline.py`](../lecture_rating_pipeline.py).

**Stage 2 — Signal extraction (automated, cheap).**
- Topic coverage proxy: keyword/keyphrase overlap between the transcript and the course syllabus entry for that session.
- Examples proxy: frequency of example-marker phrases ("for example," "let's say," "suppose," "consider this case").
- Implementation proxy: frequency of demo/code markers ("let's write," "run this," "on the screen," "the output is").

**Stage 3 — LLM-as-judge scoring.** An LLM is given the transcript plus the rubric above and asked to reason through each sub-criterion before assigning it a score, the same "reason-then-score" pattern that Professor Maaz's *"From Code to Rubrics"* paper found improves agreement with human raters. Starting with a single unified prompt rather than a multi-agent pipeline, consistent with the *"Cross-Domain Automated Feedback"* paper's finding that unified prompting is at least as good for a well-scoped, single-domain task like this.

**Stage 4 — Human calibration.** Before trusting the automated score at scale, I will hand-score a small batch of lectures myself and check agreement with the automated score (the papers use Cohen's kappa for this). Only once that agreement is acceptable does the pipeline get trusted to run unsupervised.

## 5. Week 1 Pilot Walkthrough

To sanity-check the rubric before writing the full automated pipeline, I hand-applied it to one real, publicly published lecture transcript:

- **Lecture:** MIT 6.100L — Introduction to CS and Programming Using Python, Fall 2022, Lecture 1 ("Introduction to Programming with Python"), Ana Bell
- **Source:** MIT OpenCourseWare official transcript (linked from the lecture's OCW page; the lecture is also published on MIT OCW's YouTube channel)

| Dimension | Sub-scores | Score | Max |
|---|---|---|---|
| Topic Coverage | TC1=1.0, TC2=1.0, TC3=1.0, TC4=0.5 | 3.5 | 3.5 |
| Examples | EX1=0.5, EX2=0.5, EX3=0.0 | 1.0 | 2.0 |
| Implementation | IM1=0.0, IM2=0.0, IM3=0.0 | 0.0 | 3.0 |
| Delivery & Structure | DS1=0.5, DS2=0.5, DS3=0.0 | 1.0 | 1.5 |
| **Total** | | **5.5** | **10.0** |

**Reading of the result:** this is the first lecture of the course, and it reads exactly like one should — strong, accurate coverage of the foundational concepts (imperative vs. declarative knowledge, objects/types, variables, expressions) and a clear intro/roadmap, but almost no live coding or implementation, because that hasn't started yet. The low Implementation score is not a flaw in this lecture; it's the matrix correctly reflecting that this session's job was conceptual, not hands-on.

That is exactly the limitation flagged below: a single 5.5/10 is not meaningful on its own until the matrix knows what kind of lecture it's looking at.

## 6. Limitations to Resolve Next

- **Lecture-type context:** the matrix needs a lightweight tag (e.g., "conceptual" vs. "applied/coding" session) so Implementation and Examples aren't unfairly penalized on lectures that aren't meant to have them, or the weights need to shift depending on the session's stated purpose.
- **Transcript quality:** this week's transcript was pulled from MIT's published PDF transcript via a web fetch that summarizes as it retrieves, not the raw caption file, so the Examples sub-scores above are a lower-bound estimate, not an exact count. The automated pipeline (Stage 1–2) needs to run against the raw caption/transcript text to get real counts.
- **No reference syllabus** was available for this pilot lecture, so Topic Coverage was judged qualitatively rather than by keyword overlap against a stated topic list. Real use needs the professor's syllabus or session outline as an input.
- Only one lecture and one rater (me) so far — no inter-rater or automated-vs-human agreement check yet.

## 7. Plan for Next Week

- Get the transcript-download step running with real network access so raw captions replace the summarized pilot transcript.
- Run the automated pipeline (Stages 1–3) on 3–5 real lectures Professor Maaz selects, ideally a mix of conceptual and applied sessions.
- Hand-score the same lectures myself and compare, to get a first read on how well the automated score tracks a human read (Stage 4).
- Add the lecture-type tag from Section 6 and re-run the pilot lecture through the adjusted matrix.
- Bring both sets of scores to next Wednesday's check-in for Professor Maaz to react to before we lock the rubric weights.
