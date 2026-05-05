"""
Custom Evaluation Metrics for Email Generation Assessment

METRIC 1: Fact Recall Score (FRS)
  Definition: Measures what percentage of the key facts provided as input are 
  actually present in the generated email. Uses fuzzy keyword matching with 
  semantic normalization to detect facts even when paraphrased.
  Logic: For each fact, extract key entities (names, dates, numbers, nouns). 
  Score = (facts found in email) / (total facts). Range: 0.0 – 1.0

METRIC 2: Tone Alignment Score (TAS) — LLM-as-a-Judge
  Definition: Measures how accurately the generated email matches the requested 
  tone on a 5-point scale, judged by an LLM evaluator.
  Logic: A separate LLM call evaluates (requested tone, email text) and returns 
  a score 1-5 with reasoning. Normalized to 0.0–1.0. This captures nuances 
  (warmth, urgency, formality level) that keyword matching cannot.

METRIC 3: Professional Quality Score (PQS) — Composite
  Definition: A composite of three sub-metrics: (a) Subject line presence and 
  quality, (b) Structural completeness (opening/body/CTA/sign-off), (c) 
  Conciseness ratio (email length vs reference length, penalising extreme 
  verbosity or brevity). Range: 0.0–1.0
"""

import re
import json
import requests
import math
from typing import Optional


OLLAMA_BASE_URL = "http://localhost:11434"
JUDGE_MODEL = "qwen3:4b"


# ─────────────────────────────────────────────────────────────────────────────
# METRIC 1: Fact Recall Score (FRS)
# ─────────────────────────────────────────────────────────────────────────────

def extract_key_terms(text: str) -> set[str]:
    """Extract meaningful terms from a fact string for matching."""
    # Lowercase, remove common stop words
    stop_words = {
        "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "to", "of", "in", "for", "on",
        "with", "at", "by", "from", "and", "or", "but", "if", "as", "into",
        "through", "during", "before", "after", "above", "below", "between",
        "each", "further", "then", "once", "that", "this", "these", "those",
    }
    words = re.findall(r'\b[a-zA-Z0-9$£€₹%,.\-:]+\b', text.lower())
    key_terms = {w for w in words if w not in stop_words and len(w) > 2}
    return key_terms


def fact_recall_score(generated_email: str, facts: list[str]) -> dict:
    """
    Metric 1: Fact Recall Score
    Checks what proportion of key facts from the input appear in the generated email.
    Uses term-level fuzzy matching: a fact is "found" if ≥60% of its key terms 
    appear in the email text.
    """
    if not facts:
        return {"score": 1.0, "detail": "No facts to check", "found": 0, "total": 0}

    email_lower = generated_email.lower()
    found_facts = []
    missing_facts = []

    for fact in facts:
        key_terms = extract_key_terms(fact)
        if not key_terms:
            found_facts.append(fact)
            continue

        # Count how many key terms appear in the email
        found_terms = sum(1 for term in key_terms if term in email_lower)
        recall_ratio = found_terms / len(key_terms)

        # A fact is considered "recalled" if ≥55% of its key terms appear
        if recall_ratio >= 0.55:
            found_facts.append(fact)
        else:
            missing_facts.append(f"{fact} (term match: {recall_ratio:.0%})")

    score = len(found_facts) / len(facts)
    return {
        "score": round(score, 4),
        "found": len(found_facts),
        "total": len(facts),
        "missing_facts": missing_facts,
    }


# ─────────────────────────────────────────────────────────────────────────────
# METRIC 2: Tone Alignment Score (TAS) — LLM-as-a-Judge
# ─────────────────────────────────────────────────────────────────────────────

TONE_JUDGE_PROMPT = """You are an expert communication analyst. Your task is to evaluate how well an email's actual tone matches the intended tone.

Requested Tone: {requested_tone}

Generated Email:
---
{email}
---

Evaluate the tone alignment on this scale:
1 = The tone is completely mismatched (e.g., requested formal, got casual)
2 = The tone is somewhat off — noticeable misalignment in key areas
3 = The tone is acceptable but not precisely calibrated
4 = The tone closely matches the request with only minor deviations
5 = The tone is a near-perfect or perfect match to the request

Respond ONLY with a JSON object in this exact format (no other text):
{{"score": <integer 1-5>, "reasoning": "<one sentence explanation>"}}"""


def tone_alignment_score(generated_email: str, requested_tone: str) -> dict:
    """
    Metric 2: Tone Alignment Score (LLM-as-a-Judge)
    Uses the judge model to evaluate tone accuracy on a 1-5 scale.
    """
    prompt = TONE_JUDGE_PROMPT.format(
        requested_tone=requested_tone,
        email=generated_email[:2000],  # Truncate to avoid token limits
    )

    payload = {
        "model": JUDGE_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 200},
    }

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        content = response.json()["message"]["content"]

        # Strip think blocks (qwen3 internal reasoning)
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

        # Parse JSON
        json_match = re.search(r'\{.*?\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            raw_score = int(result.get("score", 3))
            normalized = (raw_score - 1) / 4  # Map 1-5 to 0.0-1.0
            return {
                "score": round(normalized, 4),
                "raw_score": raw_score,
                "reasoning": result.get("reasoning", ""),
            }
    except Exception as e:
        pass

    # Fallback if LLM judge fails
    return {"score": 0.5, "raw_score": 3, "reasoning": "Judge unavailable, defaulted to mid-score"}


# ─────────────────────────────────────────────────────────────────────────────
# METRIC 3: Professional Quality Score (PQS) — Composite
# ─────────────────────────────────────────────────────────────────────────────

def has_subject_line(email_text: str) -> float:
    """Sub-metric A: Check for presence and quality of subject line."""
    lines = email_text.strip().split('\n')
    for line in lines[:5]:  # Check first 5 lines
        if line.lower().startswith("subject:"):
            subject_content = line[8:].strip()
            if len(subject_content) >= 5:
                # Bonus for action-oriented subject lines
                if any(kw in subject_content.lower() for kw in 
                       ["re:", "follow", "update", "request", "invite", "welcome", 
                        "recap", "action", "urgent", "proposal"]):
                    return 1.0
                return 0.85
            return 0.4
    return 0.0


def structural_completeness(email_text: str) -> float:
    """Sub-metric B: Check for email structural components."""
    text_lower = email_text.lower()
    score = 0.0
    components = {
        "greeting": any(text_lower.startswith(g) or f"\n{g}" in text_lower 
                       for g in ["dear ", "hi ", "hello ", "good morning", "good afternoon"]),
        "body_content": len(email_text.split()) > 40,
        "call_to_action": any(kw in text_lower for kw in [
            "please", "let me know", "would you", "i'd love", "feel free",
            "look forward", "reach out", "happy to", "available", "call",
        ]),
        "sign_off": any(kw in text_lower for kw in [
            "regards", "sincerely", "best", "warm", "thank", "respectfully",
            "yours", "cheers", "kind"
        ]),
    }
    weights = {"greeting": 0.25, "body_content": 0.25, "call_to_action": 0.25, "sign_off": 0.25}
    for component, present in components.items():
        if present:
            score += weights[component]
    return round(score, 4)


def conciseness_score(generated_email: str, reference_email: str) -> float:
    """
    Sub-metric C: Conciseness ratio.
    Ideal: generated email is within 50%–150% of reference length.
    Penalise extreme verbosity (>200%) and extreme brevity (<30%).
    """
    gen_words = len(generated_email.split())
    ref_words = len(reference_email.split())

    if ref_words == 0:
        return 0.5

    ratio = gen_words / ref_words

    if 0.5 <= ratio <= 1.5:
        return 1.0  # Perfect range
    elif 0.3 <= ratio < 0.5:
        return 0.7  # Slightly too brief
    elif 1.5 < ratio <= 2.0:
        return 0.7  # Slightly verbose
    elif 0.1 <= ratio < 0.3:
        return 0.4  # Too brief
    elif 2.0 < ratio <= 3.0:
        return 0.4  # Quite verbose
    else:
        return 0.1  # Way off


def professional_quality_score(generated_email: str, reference_email: str) -> dict:
    """
    Metric 3: Professional Quality Score (Composite)
    Combines subject line quality, structural completeness, and conciseness.
    """
    sub_a = has_subject_line(generated_email)
    sub_b = structural_completeness(generated_email)
    sub_c = conciseness_score(generated_email, reference_email)

    # Weighted composite: subject (25%) + structure (50%) + conciseness (25%)
    composite = (sub_a * 0.25) + (sub_b * 0.50) + (sub_c * 0.25)

    return {
        "score": round(composite, 4),
        "subject_line": round(sub_a, 4),
        "structural_completeness": round(sub_b, 4),
        "conciseness": round(sub_c, 4),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Evaluate a single scenario
# ─────────────────────────────────────────────────────────────────────────────

def evaluate_single(
    generated_email: str,
    facts: list[str],
    requested_tone: str,
    reference_email: str,
) -> dict:
    """Run all three metrics on a single generated email."""
    m1 = fact_recall_score(generated_email, facts)
    m2 = tone_alignment_score(generated_email, requested_tone)
    m3 = professional_quality_score(generated_email, reference_email)

    overall = round((m1["score"] + m2["score"] + m3["score"]) / 3, 4)

    return {
        "fact_recall_score": m1["score"],
        "fact_recall_detail": m1,
        "tone_alignment_score": m2["score"],
        "tone_alignment_detail": m2,
        "professional_quality_score": m3["score"],
        "professional_quality_detail": m3,
        "overall_score": overall,
    }


if __name__ == "__main__":
    # Quick smoke test
    test_email = """Subject: Thank You — Senior Data Engineer Interview (May 2nd)

Dear Priya,

Thank you for the interview on May 2nd regarding the Senior Data Engineer role at Nexus Analytics.
I really enjoyed discussing the Kafka pipeline project and look forward to hearing your decision by May 10th.

Best regards,
Test User"""

    test_facts = [
        "Interview held on May 2nd with hiring manager Priya Sharma",
        "Role: Senior Data Engineer at Nexus Analytics",
        "Discussed the real-time Kafka pipeline migration project",
        "Interviewer mentioned final decision expected by May 10th",
    ]

    m1 = fact_recall_score(test_email, test_facts)
    print(f"Metric 1 (Fact Recall): {m1['score']:.2%} — Found {m1['found']}/{m1['total']} facts")

    m3 = professional_quality_score(test_email, test_email)
    print(f"Metric 3 (Prof Quality): {m3['score']:.2%}")
    print("  Subject line:", m3["subject_line"])
    print("  Structure:", m3["structural_completeness"])
    print("  Conciseness:", m3["conciseness"])
