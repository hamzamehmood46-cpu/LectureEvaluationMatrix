# Lecture Evaluation Matrix

Volunteer research project with **Dr. Maaz Amjad** (Texas Tech University) — a rubric-based matrix for rating the quality of a lecture from its YouTube transcript, and the pipeline that scores it automatically.

## What this is

The goal is to score a lecture out of 10 on how well it covers its stated topic, how many examples it gives, and how much implementation / hands-on demonstration it includes — starting from a YouTube video's transcript.

The rubric design follows the same pattern used in Dr. Amjad's prior work on LLM-based rubric evaluation ([`Toward Cross-Domain Automated Feedback`](https://aclanthology.org/) and [`From Code to Rubrics`](https://doi.org/10.1145/3774905.3795458)): break the score into a small number of weighted dimensions, each made of binary/graded sub-criteria that sum to a point cap, so every score is auditable rather than a single holistic guess.

## Repository contents

| File | What it is |
|---|---|
| [`docs/week1-progress-report.md`](docs/week1-progress-report.md) | Week 1 progress report (rubric design, methodology, pilot walkthrough) |
| [`Week1_Progress_Report_Maaz.docx`](Week1_Progress_Report_Maaz.docx) | Same report as a Word document |
| [`docs/week2-progress-report.md`](docs/week2-progress-report.md) | Week 2 progress report (rubric tested on 3 real Howard University CSCI 100 lectures) |
| [`Progress_Report_Sept9.docx`](Progress_Report_Sept9.docx) | Same report as a Word document |
| [`docs/literature-review-synthesis.md`](docs/literature-review-synthesis.md) | Early literature review synthesis (5 papers) grounding the rubric and pipeline design |
| [`Literature_Review_SynthesisSept9.docx`](Literature_Review_SynthesisSept9.docx) | Same early synthesis as a Word document |
| [`Comprehensive_Literature_Review.txt`](Comprehensive_Literature_Review.txt) | Expanded literature review synthesis (11 papers), plain text |
| [`Literature_Review_Synthesis_FullSept16.docx`](Literature_Review_Synthesis_FullSept16.docx) | Same expanded synthesis as a Word document |
| [`docs/paper-links.md`](docs/paper-links.md) | Direct links to all 11 cited papers, plus the 4 excluded for requiring paywalled/TTU-library access |
| [`Progress_Report_Sept23.docx`](Progress_Report_Sept23.docx) | Week 4 progress report (first real pipeline run, calibration results) |
| [`Practical_Work_Review_Sept21.docx`](Practical_Work_Review_Sept21.docx) | Review of existing deployed systems and what we can add over them |
| [`results/stage2_results_2026-09-23.json`](results/stage2_results_2026-09-23.json) | Stage 1-2 output on real captions for 3 lectures, with hand-scores alongside |
| [`demo/lecture-matrix-demo.html`](demo/lecture-matrix-demo.html) | Interactive demo: rubric, results, and a live Stage 2 run in the browser |
| [`lecture_rating_pipeline.py`](lecture_rating_pipeline.py) | Transcript acquisition + automated signal-extraction script (Stages 1–2 of the pipeline) |

## The rating matrix (v1)

Score out of 10, across four weighted dimensions:

| Dimension | Weight | What it checks |
|---|---|---|
| Topic Coverage | 3.5 | Scope match, depth, accuracy, coherence with prerequisites |
| Examples | 2.0 | Presence, variety, and clarity of worked examples |
| Implementation | 3.0 | Live coding / demo presence, correctness, tie-back to concept |
| Delivery & Structure | 1.5 | Framing (intro/recap), pacing & clarity, engagement |

Full sub-criteria table is in the [Week 1 report](docs/week1-progress-report.md#3-proposed-rating-matrix-v1).

## Pipeline

1. **Transcript acquisition** — pull YouTube captions (or Whisper fallback if none exist)
2. **Signal extraction** — cheap automated proxies (keyword coverage, example/implementation marker counts)
3. **LLM-as-judge scoring** — reason through each rubric sub-criterion before scoring it, rather than asking for the number directly
4. **Human calibration** — spot-check automated scores against a human rater before trusting the pipeline unsupervised

```bash
pip install youtube-transcript-api
python lecture_rating_pipeline.py <youtube_video_id_or_url> [syllabus_keywords.txt]
```

## Status

Week 4 (2026-09-23): **Stages 1-2 ran against real YouTube captions for the first time.** Two defects had to be fixed to get there: the script called a `youtube-transcript-api` method removed in v1.0, and the `e.g.` example marker never matched in ordinary prose. The resulting calibration is the important finding - the implementation marker count ranks the two content lectures in the *opposite* order to hand-scoring, returning zero markers for a lecture hand-scored 2.5/3.0. The markers detect announcements ("let's write this"), not content. The verification gate, by contrast, behaved correctly: the announcements clip failed at 0% topic coverage and 397 words. See [`Progress_Report_Sept23.docx`](Progress_Report_Sept23.docx) and [`results/`](results/).


Comprehensive literature review (2026-09-16): expanded the synthesis from 5 to 11 papers after an independent search beyond Dr. Amjad's own papers, covering LLM rubric evaluation, transcript topic segmentation, automated teaching-quality assessment, and LLM-judge reliability. Four papers requiring TTU library / paywalled access were identified but left out rather than write around unverified content — see [`docs/paper-links.md`](docs/paper-links.md) for the full source list.

Week 2 (2026-09-09): rubric tested by hand on 3 real Howard University CSCI 100 lectures, chosen to vary in type. Two content lectures scored 9.0/10 each; the third exposed a real pipeline gap — the course schedule linked an announcements clip instead of the actual lecture, and the matrix correctly scored it near zero rather than inventing content. See the [Week 2 report](docs/week2-progress-report.md) for the full breakdown.

Week 1 (2026-08-27): rubric designed, pipeline scaffolded, pilot walkthrough completed on one real lecture (MIT 6.100L, Lecture 1). See the [Week 1 report](docs/week1-progress-report.md) for details and open questions.

## Reports

Progress reports are added weekly under [`docs/`](docs/), one per week, and linked here as they're written.

- [Comprehensive literature review (11 papers) — 2026-09-16](Comprehensive_Literature_Review.txt)
- [Week 2 — 2026-09-09](docs/week2-progress-report.md)
- [Literature review synthesis (early, 5 papers) — 2026-09-02](docs/literature-review-synthesis.md)
- [Week 1 — 2026-08-27](docs/week1-progress-report.md)
