"""
Email Generation Assistant
Advanced Prompting Technique: Role-Playing + Few-Shot Examples + Chain-of-Thought (Combined)

This module implements a professional email generator using Ollama with qwen3:4b.
The prompt architecture uses three advanced techniques layered together:
  1. Role-Playing: The model is assigned an expert persona (Senior Communications Strategist)
  2. Few-Shot Examples: Two high-quality reference emails anchor output quality
  3. Chain-of-Thought: Model is asked to reason through tone/structure before writing
"""

import requests
import json
import time
from typing import Optional


OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_A = "qwen3:4b"         # Primary model
MODEL_B = "qwen3:4b"         # Second strategy: different system prompt (baseline / no few-shot)


# ─────────────────────────────────────────────────────────────
# ADVANCED PROMPT TEMPLATE  (Role-Play + Few-Shot + CoT)
# ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT_ADVANCED = """You are Alexandra Chen, a Senior Communications Strategist with 15 years of experience \
writing high-impact professional emails for Fortune 500 executives, startups, and NGOs. \
Your emails are renowned for being clear, purposeful, and perfectly calibrated to the intended tone.

Your writing philosophy:
- Every email has ONE primary goal — never dilute it.
- Facts are woven naturally into narrative, never listed mechanically.
- Tone is a spectrum; you hit it precisely, not approximately.
- Subject lines are concise and action-oriented.

EXAMPLES OF YOUR WORK:

--- EXAMPLE 1 ---
Intent: Follow up after a product demo meeting
Key Facts: Demo held on June 3rd, prospect is TechCorp, product shown was DataSync Pro, next step is a pilot proposal, contact is Sarah Mitchell
Tone: Professional, warm

Subject: Great Connecting on DataSync Pro — Next Steps for TechCorp

Hi Sarah,

It was a pleasure walking you through DataSync Pro on June 3rd — your questions showed a deep understanding of the integration challenges your team is navigating, and I left the conversation genuinely energised.

Based on our discussion, I'd like to put together a tailored pilot proposal for TechCorp that addresses the specific workflow bottlenecks you mentioned. I'll have a draft ready for your review by end of week.

Would Thursday or Friday work for a quick 20-minute call to align on scope before I finalise it?

Looking forward to continuing the conversation.

Best regards,
[Your Name]

--- EXAMPLE 2 ---
Intent: Request an extension on a project deadline
Key Facts: Original deadline is July 15th, requesting extension to July 30th, reason is unexpected API integration issues, project is the CRM Migration, manager is David Okafor
Tone: Formal, accountable

Subject: Extension Request — CRM Migration Deadline (July 15 → July 30)

Dear David,

I am writing to formally request a two-week extension on the CRM Migration project, moving the delivery date from July 15th to July 30th.

During the past week, our team encountered unexpected API integration issues with the legacy data pipeline that were not apparent during the initial scoping phase. Resolving these correctly requires additional validation cycles to ensure data integrity across all migrated records.

I take full accountability for the timeline impact and want to assure you that this extension is the minimum required to deliver a solution that meets our quality standards. I have already reallocated internal resources to accelerate the remaining workload.

Please let me know if you would like to discuss this further or require additional documentation.

Respectfully,
[Your Name]
---

Now follow this Chain-of-Thought process BEFORE writing each email:
<reasoning>
1. GOAL: What is the single most important outcome of this email?
2. AUDIENCE: Who is reading this — what do they care about?
3. TONE CALIBRATION: What specific language, sentence length, and formality level matches the requested tone?
4. FACT INTEGRATION: How can each fact be woven naturally (not listed) into the email?
5. STRUCTURE: Subject → Opening hook → Core message → Clear CTA → Sign-off
</reasoning>

After your reasoning block, output ONLY the final email (no extra commentary).
Format:
Subject: [subject line]

[email body]
"""

SYSTEM_PROMPT_BASELINE = """You are a helpful assistant that writes professional emails.
When given an intent, key facts, and a tone, write an appropriate email.
Include a subject line. Be concise and professional."""


USER_PROMPT_TEMPLATE = """Please write an email with the following specifications:

Intent: {intent}

Key Facts:
{facts}

Tone: {tone}

Remember to follow the Chain-of-Thought reasoning process and produce a polished, professional email."""


def format_facts(facts: list[str]) -> str:
    return "\n".join(f"- {f}" for f in facts)


def generate_email(
    intent: str,
    facts: list[str],
    tone: str,
    model: str = MODEL_A,
    use_advanced_prompt: bool = True,
    temperature: float = 0.7,
) -> dict:
    """Generate an email using Ollama API."""
    system_prompt = SYSTEM_PROMPT_ADVANCED if use_advanced_prompt else SYSTEM_PROMPT_BASELINE
    user_prompt = USER_PROMPT_TEMPLATE.format(
        intent=intent,
        facts=format_facts(facts),
        tone=tone,
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 800,
        },
    }

    start = time.time()
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        elapsed = time.time() - start

        content = data["message"]["content"]

        # Strip <think>...</think> blocks (qwen3 CoT internal reasoning)
        import re
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        # Strip <reasoning>...</reasoning> if model echoes it
        content = re.sub(r"<reasoning>.*?</reasoning>", "", content, flags=re.DOTALL).strip()

        return {
            "success": True,
            "content": content,
            "model": model,
            "elapsed_seconds": round(elapsed, 2),
            "prompt_tokens": data.get("prompt_eval_count", 0),
            "completion_tokens": data.get("eval_count", 0),
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "content": "",
            "error": "Cannot connect to Ollama. Ensure `ollama serve` is running.",
            "model": model,
            "elapsed_seconds": 0,
        }
    except Exception as e:
        return {
            "success": False,
            "content": "",
            "error": str(e),
            "model": model,
            "elapsed_seconds": 0,
        }


def check_ollama_health() -> bool:
    """Check if Ollama is running and model is available."""
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        return any(MODEL_A.split(":")[0] in m for m in models)
    except Exception:
        return False


if __name__ == "__main__":
    print("Testing email generator...")
    result = generate_email(
        intent="Follow up after a job interview",
        facts=[
            "Interview was on May 2nd with Priya Sharma",
            "Role: Senior Data Engineer at Nexus Analytics",
            "Discussed the real-time pipeline project",
            "Interviewer mentioned decision by May 10th",
        ],
        tone="Professional, enthusiastic",
    )
    if result["success"]:
        print(result["content"])
    else:
        print(f"Error: {result.get('error')}")
