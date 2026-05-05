"""
Evaluation Runner
Runs both Model A (advanced prompting) and Model B (baseline prompting)
across all 10 test scenarios and outputs a structured CSV + JSON report.

Usage:
    python src/evaluate.py
    python src/evaluate.py --model qwen3:4b --output reports/results.csv
"""

import sys
import os
import csv
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.email_generator import generate_email, check_ollama_health, MODEL_A
from src.metrics import evaluate_single
from data.test_scenarios import TEST_SCENARIOS


def run_evaluation(
    model: str = MODEL_A,
    use_advanced_prompt: bool = True,
    strategy_name: str = "Advanced (Role-Play + Few-Shot + CoT)",
    output_csv: str = None,
    output_json: str = None,
    verbose: bool = True,
) -> dict:
    """Run evaluation across all 10 scenarios."""

    strategy_label = strategy_name
    results = []

    print(f"\n{'='*70}")
    print(f"  Strategy: {strategy_label}")
    print(f"  Model: {model}")
    print(f"  Scenarios: {len(TEST_SCENARIOS)}")
    print(f"{'='*70}\n")

    for scenario in TEST_SCENARIOS:
        sid = scenario["id"]
        intent = scenario["intent"]
        facts = scenario["facts"]
        tone = scenario["tone"]
        reference = scenario["reference_email"]

        if verbose:
            print(f"[{sid:02d}/10] Generating: {intent[:55]}...")

        # Generate the email
        gen_result = generate_email(
            intent=intent,
            facts=facts,
            tone=tone,
            model=model,
            use_advanced_prompt=use_advanced_prompt,
        )

        if not gen_result["success"]:
            print(f"  ⚠ Generation failed: {gen_result.get('error', 'Unknown error')}")
            results.append({
                "scenario_id": sid,
                "intent": intent,
                "tone": tone,
                "strategy": strategy_label,
                "model": model,
                "generated_email": "[GENERATION FAILED]",
                "fact_recall_score": 0.0,
                "tone_alignment_score": 0.0,
                "professional_quality_score": 0.0,
                "overall_score": 0.0,
                "generation_time_s": 0,
                "error": gen_result.get("error", ""),
            })
            continue

        generated_email = gen_result["content"]

        # Evaluate
        eval_result = evaluate_single(
            generated_email=generated_email,
            facts=facts,
            requested_tone=tone,
            reference_email=reference,
        )

        if verbose:
            print(f"  ✓ FRS: {eval_result['fact_recall_score']:.2%}  "
                  f"TAS: {eval_result['tone_alignment_score']:.2%}  "
                  f"PQS: {eval_result['professional_quality_score']:.2%}  "
                  f"→ Overall: {eval_result['overall_score']:.2%}  "
                  f"({gen_result['elapsed_seconds']}s)")

        results.append({
            "scenario_id": sid,
            "intent": intent,
            "tone": tone,
            "strategy": strategy_label,
            "model": model,
            "generated_email": generated_email,
            "reference_email": reference,
            "fact_recall_score": eval_result["fact_recall_score"],
            "tone_alignment_score": eval_result["tone_alignment_score"],
            "professional_quality_score": eval_result["professional_quality_score"],
            "overall_score": eval_result["overall_score"],
            "frs_found": eval_result["fact_recall_detail"]["found"],
            "frs_total": eval_result["fact_recall_detail"]["total"],
            "tas_raw": eval_result["tone_alignment_detail"]["raw_score"],
            "tas_reasoning": eval_result["tone_alignment_detail"]["reasoning"],
            "pqs_subject": eval_result["professional_quality_detail"]["subject_line"],
            "pqs_structure": eval_result["professional_quality_detail"]["structural_completeness"],
            "pqs_conciseness": eval_result["professional_quality_detail"]["conciseness"],
            "generation_time_s": gen_result["elapsed_seconds"],
            "error": "",
        })

        # Small delay to avoid hammering Ollama
        time.sleep(0.5)

    # Summary stats
    valid = [r for r in results if r["error"] == ""]
    avg_frs = sum(r["fact_recall_score"] for r in valid) / len(valid) if valid else 0
    avg_tas = sum(r["tone_alignment_score"] for r in valid) / len(valid) if valid else 0
    avg_pqs = sum(r["professional_quality_score"] for r in valid) / len(valid) if valid else 0
    avg_overall = sum(r["overall_score"] for r in valid) / len(valid) if valid else 0

    summary = {
        "strategy": strategy_label,
        "model": model,
        "total_scenarios": len(TEST_SCENARIOS),
        "successful": len(valid),
        "avg_fact_recall_score": round(avg_frs, 4),
        "avg_tone_alignment_score": round(avg_tas, 4),
        "avg_professional_quality_score": round(avg_pqs, 4),
        "avg_overall_score": round(avg_overall, 4),
        "timestamp": datetime.now().isoformat(),
    }

    print(f"\n{'─'*70}")
    print(f"  SUMMARY — {strategy_label}")
    print(f"  Fact Recall Score (avg):         {avg_frs:.2%}")
    print(f"  Tone Alignment Score (avg):      {avg_tas:.2%}")
    print(f"  Professional Quality Score (avg):{avg_pqs:.2%}")
    print(f"  ─────────────────────────────────")
    print(f"  OVERALL AVERAGE:                 {avg_overall:.2%}")
    print(f"{'─'*70}\n")

    return {"results": results, "summary": summary}


def save_csv(all_results: list[dict], filepath: str):
    """Save results to CSV."""
    if not all_results:
        return
    fieldnames = [
        "scenario_id", "intent", "tone", "strategy", "model",
        "fact_recall_score", "tone_alignment_score", "professional_quality_score", "overall_score",
        "frs_found", "frs_total", "tas_raw", "tas_reasoning",
        "pqs_subject", "pqs_structure", "pqs_conciseness",
        "generation_time_s", "generated_email", "reference_email", "error",
    ]
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_results)
    print(f"✓ CSV saved: {filepath}")


def save_json(data: dict, filepath: str):
    """Save full results to JSON."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ JSON saved: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Email Generation Evaluation Runner")
    parser.add_argument("--model", default=MODEL_A, help="Ollama model name")
    parser.add_argument("--output-dir", default="reports", help="Output directory")
    parser.add_argument("--quiet", action="store_true", help="Suppress verbose output")
    args = parser.parse_args()

    print("\n" + "="*70)
    print("  EMAIL GENERATION ASSISTANT — EVALUATION SUITE")
    print("="*70)

    # Check Ollama connectivity
    print("\nChecking Ollama connection...")
    if not check_ollama_health():
        print("⚠ Warning: Cannot verify Ollama is running or model is available.")
        print("  Ensure `ollama serve` is running and `ollama pull qwen3:4b` is done.")
        print("  Continuing anyway (may fail on generation)...\n")
    else:
        print(f"✓ Ollama is running. Using model: {args.model}\n")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_results = []
    all_summaries = []

    # ── Strategy A: Advanced Prompt (Role-Play + Few-Shot + CoT) ──
    result_a = run_evaluation(
        model=args.model,
        use_advanced_prompt=True,
        strategy_name="Strategy_A_Advanced (Role-Play+Few-Shot+CoT)",
        verbose=not args.quiet,
    )
    all_results.extend(result_a["results"])
    all_summaries.append(result_a["summary"])

    # ── Strategy B: Baseline Prompt (Simple instruction) ──
    result_b = run_evaluation(
        model=args.model,
        use_advanced_prompt=False,
        strategy_name="Strategy_B_Baseline (Simple instruction)",
        verbose=not args.quiet,
    )
    all_results.extend(result_b["results"])
    all_summaries.append(result_b["summary"])

    # Save outputs
    csv_path = output_dir / f"evaluation_results_{timestamp}.csv"
    json_path = output_dir / f"evaluation_results_{timestamp}.json"
    summary_path = output_dir / f"evaluation_summary_{timestamp}.json"

    save_csv(all_results, str(csv_path))
    save_json({"results": all_results, "summaries": all_summaries}, str(json_path))
    save_json(all_summaries, str(summary_path))

    # ── Comparative Analysis ──
    print("\n" + "="*70)
    print("  COMPARATIVE ANALYSIS")
    print("="*70)

    sa = result_a["summary"]
    sb = result_b["summary"]

    winner_frs = "Strategy A" if sa["avg_fact_recall_score"] >= sb["avg_fact_recall_score"] else "Strategy B"
    winner_tas = "Strategy A" if sa["avg_tone_alignment_score"] >= sb["avg_tone_alignment_score"] else "Strategy B"
    winner_pqs = "Strategy A" if sa["avg_professional_quality_score"] >= sb["avg_professional_quality_score"] else "Strategy B"
    winner_overall = "Strategy A" if sa["avg_overall_score"] >= sb["avg_overall_score"] else "Strategy B"

    print(f"\n  {'Metric':<35} {'Strategy A':>12} {'Strategy B':>12} {'Winner':>12}")
    print(f"  {'─'*73}")
    print(f"  {'Fact Recall Score (FRS)':<35} {sa['avg_fact_recall_score']:>11.2%} {sb['avg_fact_recall_score']:>11.2%} {winner_frs:>12}")
    print(f"  {'Tone Alignment Score (TAS)':<35} {sa['avg_tone_alignment_score']:>11.2%} {sb['avg_tone_alignment_score']:>11.2%} {winner_tas:>12}")
    print(f"  {'Professional Quality Score (PQS)':<35} {sa['avg_professional_quality_score']:>11.2%} {sb['avg_professional_quality_score']:>11.2%} {winner_pqs:>12}")
    print(f"  {'─'*73}")
    print(f"  {'OVERALL AVERAGE':<35} {sa['avg_overall_score']:>11.2%} {sb['avg_overall_score']:>11.2%} {winner_overall:>12}")
    print()
    print(f"\n  Recommended for Production: {winner_overall}")
    print(f"\n  Output files:")
    print(f"    CSV:     {csv_path}")
    print(f"    JSON:    {json_path}")
    print(f"    Summary: {summary_path}")
    print()


if __name__ == "__main__":
    main()
