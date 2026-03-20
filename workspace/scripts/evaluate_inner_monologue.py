import sys
import os
import json
import argparse
import random
import re

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from context_inference import ContextInference

JUDGE_SYSTEM_PROMPT = "You are an expert clinical psychology supervisor and a strict AI evaluator."

JUDGE_PROMPT_TEMPLATE = """# Task
Evaluate the generated <internal> monologue for an AI-simulated patient based on specific constraints.

# Context
[Problem Type]: {problem_type}
[Situation]: {situation}
[Behavior Type]: {behavior_type}
[Resistance Category]: {resistance_category}

# Expected Constraints for this Category
{criteria}

# Dialogue & Generated Monologue
{dialogue_with_internal}

# Patient's Actual Final Response
Patient: {ground_truth}

# Evaluation Instructions
Assess whether the Generated Monologue strictly followed the Expected Constraints and whether its tone smoothly bridges the Dialogue to the Patient's Actual Final Response.

Score from 1 to 5:
1 = Fails completely (violates constraints, hallucinates horribly)
2 = Poor (misses the core psychological task)
3 = Acceptable (follows basics but lacks depth or slightly violates length constraint)
4 = Good (hits the constraints and tone well)
5 = Excellent (perfectly captures the required psychological layer and constraints)

Output ONLY a JSON object:
{{
  "score": <int>,
  "issues": "<brief summary of what it failed to do, or 'None'>",
  "justification": "<why you gave this score>"
}}"""

# Criteria mappings based on our 5 templates
CRITERIA = {
    "ACTIVE_DEFENSE": "Must capture 4 layers: Perception of therapist, Emotional state + PAST experience, What they are PROTECTING (core desire/belief), and thought process. It must NOT be a simple reaction; they must be guarding something.",
    "EVASION": "Must NOT analyze surface words. Must reveal what they are deliberately NOT saying (suppressed fear/resentment). Max 2-3 sentences.",
    "VULNERABILITY": "Must show internal searching and unresolved ambivalence. Emotional stream of consciousness, struggling but open.",
    "SIMPLE_AGREEMENT": "CRITICAL: MUST be exactly 1-2 very short, natural sentences. Strictly surface-level. Absolutely NO over-analyzing or deep psychological burdens.",
    "INSIGHT": "Must capture a cognitive shift, sense of relief, or crystallization of determination (the 'Aha' moment)."
}

def get_template_class(parent, category):
    if parent in ("A", "B", "Arguing", "Denying"):
        return "ACTIVE_DEFENSE"
    elif parent in ("C", "D", "Avoiding", "Ignoring"):
        return "EVASION"
    elif category == "Exploratory":
        return "VULNERABILITY"
    elif category == "Cooperative":
        return "SIMPLE_AGREEMENT"
    elif category == "Resolution":
        return "INSIGHT"
    return "SIMPLE_AGREEMENT"

def extract_internal_text(prediction):
    m = re.search(r'<internal>(.*?)</internal>', prediction, re.DOTALL)
    return m.group(1).strip() if m else prediction.strip()

def format_dialogue(context):
    history_text = ""
    for msg in context:
        role = "Therapist" if msg["role"] == "user" else "Patient"
        history_text += f"{role}: {msg['content']}\n"
    return history_text.strip()


def main():
    parser = argparse.ArgumentParser(description="Evaluate Inner Monologue generation using LLM-as-a-Judge")
    parser.add_argument("--samples-per-class", type=int, default=3, help="Number of samples to evaluate per template class")
    parser.add_argument("--model", type=str, default="deepseek-v3.2", help="Model name for the judge")
    args = parser.parse_args()

    workspace_dir = os.path.join(os.path.dirname(__file__), '..')
    dataset_file = os.path.join(workspace_dir, "results", "inner_monologue_dataset.json")

    print(f"Loading dataset from {dataset_file}...")
    with open(dataset_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Group data by template class
    grouped_data = {k: [] for k in CRITERIA.keys()}
    
    for item in data:
        t_class = get_template_class(item.get("resistance_parent"), item.get("resistance_category"))
        grouped_data[t_class].append(item)

    # Sample cases
    eval_cases = []
    print("\nSampling for evaluation:")
    for t_class, items in grouped_data.items():
        if not items:
            continue
        k = min(args.samples_per_class, len(items))
        sampled = random.sample(items, k)
        eval_cases.extend(sampled)
        print(f"  {t_class}: sampled {k} / {len(items)} cases")

    if not eval_cases:
        print("No cases to evaluate.")
        return

    # Build prompt for LLM judge
    judge_test_cases = []
    for case in eval_cases:
        t_class = get_template_class(case.get("resistance_parent"), case.get("resistance_category"))
        internal_text = extract_internal_text(case.get("prediction", ""))
        
        # Build dialogue string ending with the internal monologue
        dialogue = format_dialogue(case.get("context", []))
        dialogue_with_internal = f"{dialogue}\n\n<internal>\n{internal_text}\n</internal>"
        
        prompt = JUDGE_PROMPT_TEMPLATE.format(
            problem_type=case.get("problem_type", ""),
            situation=case.get("situation", ""),
            behavior_type=case.get("behavior_type", ""),
            resistance_category=case.get("resistance_category", ""),
            criteria=CRITERIA[t_class],
            dialogue_with_internal=dialogue_with_internal,
            ground_truth=case.get("ground_truth", "")
        )
        
        judge_case = {
            "original_case": case,
            "template_class": t_class,
            "system_prompt": JUDGE_SYSTEM_PROMPT,
            "context": [{"role": "user", "content": prompt}]
        }
        judge_test_cases.append(judge_case)

    print(f"\nEvaluating {len(judge_test_cases)} cases using {args.model}...")
    
    inference = ContextInference(model=args.model)
    results = inference.batch_test(
        test_cases=judge_test_cases,
        output_file=None,
        temperature=0.3, # Low temp for more objective judging
        with_ground_truth=False,
        use_simple_prompt=False,
    )

    # Process and print results
    scores = {k: [] for k in CRITERIA.keys()}
    
    for r, judge_case in zip(results, judge_test_cases):
        t_class = judge_case["template_class"]
        original_case = judge_case["original_case"]
        prediction_json = r.get("prediction", "{}")
        
        # Try to parse the JSON
        # Sometimes LLMs wrap json in markdown block
        json_str = prediction_json
        m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', prediction_json, re.DOTALL)
        if m:
            json_str = m.group(1)
            
        try:
            eval_data = json.loads(json_str)
            score = eval_data.get("score", 0)
            scores[t_class].append(score)
            
            print("\n" + "="*80)
            print(f"Class: {t_class} | Category: {original_case.get('resistance_category')}")
            print(f"Score: {score}/5")
            print(f"Issues: {eval_data.get('issues')}")
            print(f"Justification: {eval_data.get('justification')}")
            print("-" * 40)
            print("Generated Internal:")
            print(extract_internal_text(original_case.get('prediction', '')))
            
        except json.JSONDecodeError:
            print(f"\nFailed to parse JSON for {t_class}: \n{prediction_json}")

    print("\n" + "="*80)
    print("FINAL AVERAGE SCORES BY TEMPLATE:")
    total_score = 0
    total_count = 0
    for t_class, s_list in scores.items():
        if s_list:
            avg = sum(s_list) / len(s_list)
            print(f"  {t_class}: {avg:.1f}/5 (from {len(s_list)} samples)")
            total_score += sum(s_list)
            total_count += len(s_list)
    
    if total_count > 0:
        print(f"\nOVERALL AVERAGE: {total_score/total_count:.2f}/5")

if __name__ == "__main__":
    main()
