"""
Lecture Rating Matrix - transcript pipeline (Week 1 draft)
Professor Maaz volunteer research project - Hamza Mehmood

Two pieces:
  1. fetch_transcript(video_id)  -> pulls YouTube captions (Stage 1)
  2. score_signals(transcript)   -> cheap automated proxies for the rubric (Stage 2)

Run this on a machine with normal internet access (this sandbox's network
does not reach YouTube directly - see Week 1 report, Section 4/6).

Usage:
    pip install youtube-transcript-api
    python lecture_rating_pipeline.py <youtube_video_id_or_url>
"""

import re
import sys
import json
from collections import Counter

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None


# ---------- Stage 1: transcript acquisition ----------

def extract_video_id(url_or_id: str) -> str:
    """Accept a bare video ID or a full YouTube URL."""
    m = re.search(r"(?:v=|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})", url_or_id)
    return m.group(1) if m else url_or_id


def fetch_transcript(video_id: str) -> str:
    """Return the full transcript as one plain-text string."""
    if YouTubeTranscriptApi is None:
        raise RuntimeError("pip install youtube-transcript-api first")
    video_id = extract_video_id(video_id)
    # youtube-transcript-api >= 1.0 replaced the classmethod get_transcript()
    # with an instance method fetch() returning objects, not dicts. Support both
    # so the script works regardless of which version is installed.
    if hasattr(YouTubeTranscriptApi, "get_transcript"):
        segments = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(s["text"].strip() for s in segments if s["text"].strip())
    fetched = YouTubeTranscriptApi().fetch(video_id)
    return " ".join(s.text.strip() for s in fetched.snippets if s.text.strip())


# ---------- Stage 2: cheap automated signal extraction ----------
# These are PROXIES, not the final score. They feed the LLM-as-judge step
# (Stage 3, not implemented here yet) as supporting evidence, and let a
# human sanity-check the rubric before trusting an automated pass.

EXAMPLE_MARKERS = [
    r"\bfor example\b", r"\blet'?s say\b", r"\bsuppose\b", r"\bimagine\b",
    r"\bconsider (?:this|the case)\b", r"\bas an example\b", r"\be\.g\.",
    r"\btake this case\b", r"\bhere'?s an example\b",
]

IMPLEMENTATION_MARKERS = [
    r"\blet'?s (?:write|code|type|run|implement)\b", r"\brun this\b",
    r"\bon (?:the|your) screen\b", r"\bthe output is\b", r"\bthis prints\b",
    r"\blet'?s open\b", r"\bin (?:vs ?code|the terminal|jupyter)\b",
    r"\bdebug(?:ging)?\b", r"\bsyntax error\b", r"\btraceback\b",
]


def _count_markers(text: str, patterns) -> int:
    text_l = text.lower()
    return sum(len(re.findall(p, text_l)) for p in patterns)


def topic_coverage_signal(transcript: str, syllabus_keywords: list) -> dict:
    """Keyword/keyphrase overlap between transcript and the session's
    stated topic list (pass in the professor's syllabus terms)."""
    text_l = transcript.lower()
    found = [kw for kw in syllabus_keywords if kw.lower() in text_l]
    missing = [kw for kw in syllabus_keywords if kw not in found]
    coverage_ratio = len(found) / len(syllabus_keywords) if syllabus_keywords else None
    return {"found": found, "missing": missing, "coverage_ratio": coverage_ratio}


def score_signals(transcript: str, syllabus_keywords=None) -> dict:
    word_count = len(transcript.split())
    examples = _count_markers(transcript, EXAMPLE_MARKERS)
    implementation = _count_markers(transcript, IMPLEMENTATION_MARKERS)
    result = {
        "word_count": word_count,
        "example_marker_count": examples,
        "example_markers_per_1000_words": round(examples / word_count * 1000, 2) if word_count else 0,
        "implementation_marker_count": implementation,
        "implementation_markers_per_1000_words": round(implementation / word_count * 1000, 2) if word_count else 0,
    }
    if syllabus_keywords:
        result["topic_coverage"] = topic_coverage_signal(transcript, syllabus_keywords)
    return result


# ---------- CLI ----------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lecture_rating_pipeline.py <youtube_video_id_or_url> [syllabus_keywords.txt]")
        sys.exit(1)

    vid = sys.argv[1]
    transcript = fetch_transcript(vid)

    keywords = None
    if len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            keywords = [line.strip() for line in f if line.strip()]

    signals = score_signals(transcript, keywords)
    print(json.dumps(signals, indent=2))
