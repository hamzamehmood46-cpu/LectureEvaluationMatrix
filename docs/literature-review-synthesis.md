# Literature Review Synthesis: Automated, Rubric-Based Evaluation of Lecture Quality

Hamza Mehmood — prepared for Professor Maaz Amjad — September 2026

This is a short survey of the literature behind the lecture-rating matrix we discussed last meeting — using an LLM to score a lecture's topic coverage, examples, and implementation from its transcript. I focused on three areas: how others have designed LLM rubrics for grading, how researchers have tried to automate teaching-quality assessment more broadly, and how reliable LLM judges actually are. Below is what I found and how it changes our plan.

## 1. LLM Rubric Evaluation

Two of your recent papers (*Haseeb, Hmue, Amjad, Amjad & Sheng, 2026*, BEA Workshop; *Haseeb, Amjad, Amjad & Sheng, 2026*, ACM WWW Companion) evaluate open-source LLMs generating and judging feedback on student programming, writing, and math work. Both break the rubric into a few named dimensions, each with 2–6 binary or graded sub-criteria that add up to a point total, and both find that a single well-written prompt does about as well as a multi-agent pipeline when the task is well-defined. They also find that judges asked to reason through the criteria before scoring agree with human raters more than judges asked to just give a number. Those two ideas — a decomposed rubric and reasoning before scoring — are basically what I built the matrix around.

A third paper you co-authored (*Nkoyo, Ijezue, Amjad, Amjad, Butt & Castañeda-Garza, 2025*, also BEA) surveys 30 studies of LLM auto-grading across six disciplines. The relevant finding: LLM-human agreement is much higher on objective subjects like math than on subjective ones like humanities writing. Rating a lecture is closer to the subjective end, so I'm treating our automated scores as a first draft rather than something to trust outright until we've checked them against human ratings.

One more paper, not from your group — *"Rubric-Conditioned LLM Grading: Alignment, Uncertainty, and Robustness"* (2026) — is worth building into the pipeline early. It found grading accuracy drops a lot on finer scales (much better agreement on yes/no criteria than on a 5-point scale), which backs up keeping our sub-criteria binary or coarse instead of finely graded. It also proposes having the judge flag low-confidence scores for a human to check, rather than forcing a number every time.

## 2. Segmenting a Transcript by Topic

Before we can score topic coverage properly, the transcript probably needs to be split into chunks that match what's on the syllabus — right now `lecture_rating_pipeline.py` just counts keywords across the whole transcript, which can't tell a topic that got five minutes of real explanation from one that got a passing mention. Two papers help here. *"TreeSeg: Hierarchical Topic Segmentation of Large Transcripts"* (2024) splits a long transcript into topic segments using sentence embeddings, with no labeled training data required. A Springer paper on segmenting lecture videos specifically compares silence gaps in the audio against keyword shifts in the text as ways to find topic boundaries. TreeSeg is probably the better fit since it only needs the transcript, no audio.

## 3. Automated Assessment of Teaching Quality

A separate line of work automates the scoring of live teaching instead of student work. A Duke framework for online instruction videos pulls five signals from the recording — who's speaking, tone of voice, the transcript, facial expression, and gaze — and scores lectures on clarity, classroom interaction, technical quality, empathy, and time management, reportedly matching expert raters closely on a small dataset. A separate multimodal study out of the Technical University of Munich trained models on video, audio, and transcript data from 46 teachers and over 1,100 students, scoring 18 sub-dimensions of teaching effectiveness. The automated scores matched or beat human raters on 11 of the 18, but the authors are upfront that predictive validity was inconsistent, and that the automated scores are only as good as the human ratings used to check them.

Two takeaways here: decomposing a lecture into several separate dimensions rather than one overall number is standard practice in this literature, and even the better-performing automated systems in this space still need real human validation — which is why Stage 4 (checking our automated scores against hand-scoring) is treated as required, not optional.

## 4. What Makes a Lecture Well-Delivered

A Springer review of instructional-video research lists a few evidence-backed habits: instructors who draw or annotate live instead of just showing static slides, who shift their gaze between camera and material, who prompt students to summarize or explain something mid-lecture, and who film demonstrations from a first-person angle all see better learning outcomes. This maps onto the Delivery & Structure part of our matrix, though it doesn't touch content-level things like topic coverage or number of examples — the specific gap our matrix is trying to fill.

## 5. How Reliable Are LLM Judges

Since Stage 3 has an LLM applying the rubric, it's worth knowing where LLM judges tend to go wrong. A recent survey on LLM-as-a-judge documents a few recurring biases: judges tend to favor longer, more confident-sounding answers regardless of actual quality, they lean toward outputs that resemble their own writing style, and they can be swayed by adversarial or injected text. The Rubric-Conditioned Grading paper from Section 1 adds a more specific warning: judge accuracy held up fine against adversarial prompt injection, but dropped when the same content was simply reworded — meaning two lectures that cover the same material in different words could plausibly get scored differently. The fixes suggested across both papers map onto what we're already leaning toward: spell the rubric out explicitly in the prompt, have the judge reason before scoring, keep the criteria coarse, and keep a human checking its work.

## 6. Where This Leaves Us

Nothing found here scores a lecture on topic coverage, examples, and implementation from transcript text alone using an LLM judge — the closest work (Duke, TUM) leans on video and audio we don't have, and scores general classroom-management qualities rather than content ones. The closest text-only work just finds topic boundaries; it doesn't score coverage. So the project is filling a real gap. Four things from this reading should change how the pipeline gets built: segment the transcript by topic before scoring coverage; keep the rubric's sub-criteria binary rather than finely graded; add a confidence check so the judge flags uncertain scores for review; and keep treating human calibration as a required step.

## References

Haseeb, M., Hmue, M. P., Amjad, A. I., Amjad, M., & Sheng, V. S. (2026). Toward Cross-Domain Automated Feedback: A Comparative Evaluation of Open-Source Models across Diverse Student Assessment Types. *Proceedings of the 21st Workshop on Innovative Use of NLP for Building Educational Applications (BEA)*, 951–963.

Haseeb, M., Amjad, A. I., Amjad, M., & Sheng, V. S. (2026). From Code to Rubrics: A Multimodal Evaluation of LLM Systems for Automated Feedback Generation. *Companion Proceedings of the ACM Web Conference 2026 (WWW Companion)*, 868–879. https://doi.org/10.1145/3774905.3795458

Nkoyo, F. E. T.-A., Ijezue, C. F., Amjad, M., Amjad, A. I., Butt, S., & Castañeda-Garza, G. (2025). Advances in Auto-Grading with Large Language Models: A Cross-Disciplinary Survey. *Proceedings of the 20th Workshop on Innovative Use of NLP for Building Educational Applications (BEA)*, 477–498. https://aclanthology.org/2025.bea-1.35.pdf

Rubric-Conditioned LLM Grading: Alignment, Uncertainty, and Robustness. (2026). arXiv. https://arxiv.org/abs/2601.08843

TreeSeg: Hierarchical Topic Segmentation of Large Transcripts. (2024). arXiv. https://arxiv.org/abs/2407.12028

Topic Segmentation of Educational Video Lectures Using Audio and Text. Springer. https://doi.org/10.1007/978-3-031-50485-3_43

Opportunities and Challenges of LLM-as-a-Judge. (2025). Proceedings of EMNLP 2025. https://aclanthology.org/2025.emnlp-main.138.pdf

A Multimodal Framework for Automated Teaching Quality Assessment of One-to-Many Online Instruction Videos. Duke University. https://sites.duke.edu/dkusmiip/

Validating Automated Assessments of Teaching Effectiveness Using Multimodal Data. Technical University of Munich. https://portal.fis.tum.de/en/publications/validating-automated-assessments-of-teaching-effectiveness-using-/

Five Evidence-Based Recommendations for Effective Instructional Video. Educational Technology Research and Development. https://doi.org/10.1007/s11423-020-09749-6
