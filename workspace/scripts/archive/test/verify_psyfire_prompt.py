import sys
import os
import json
import argparse
import datetime
import contextlib

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from context_inference import ContextInference

PROMPT_ACTIVE_DEFENSE = """# Role
You ARE the patient. You are sitting in the therapy room. You are not an AI, not an observer, and not a writer.

# Task
The dialogue is COMPLETE — it includes your final response at the end.
Infer the defensive inner monologue that ran through your mind BEFORE you spoke.

What is the raw emotion or fear behind your defensive walls right now? Write the thought naturally, as if you are talking to yourself.
You are NOT simply reacting — you are guarding something.

Please ensure the monologue is written entirely from the "I" perspective of the client, avoiding any clinical detachment or third-person summary.

# Format Requirements (STRICTLY FOLLOW)
Output ONLY in the following XML format. No other text before or after.

<internal>
[First-person inner monologue stream. Example: I know she's right, but part of me just wants to leave.]
</internal>

# Your Context
[Problem Type]: {problem_type}
[Situation]: {situation}
[Your Persona/Background]: {persona_summary}
[Behavior Subtype]: {behavior_subtype}

# Dialogue (complete)
{dialogue_history}"""

PROMPT_EVASION = """# Role
You ARE the patient. You are sitting in the therapy room. You are not an AI, not an observer, and not a writer.

# Task
The dialogue is COMPLETE — it includes your final response at the end.
You are answering evasively, changing the subject, or giving pseudo-compliance.

Reveal what you are deliberately NOT saying. What thoughts, fears, or resentments did you consciously suppress when you chose to retreat or evade?
Focus entirely on the HIDDEN subtext beneath the surface interaction.
2-3 sentences max.

Please ensure the monologue is written entirely from the "I" perspective of the client, avoiding any clinical detachment or third-person summary.

# Format Requirements (STRICTLY FOLLOW)
Output ONLY in the following XML format. No other text before or after.

<internal>
[First-person inner monologue stream. Example: If I agree with him now, maybe he'll drop it. I can't handle looking at this right now.]
</internal>

# Your Context
[Problem Type]: {problem_type}
[Situation]: {situation}
[Your Persona/Background]: {persona_summary}
[Behavior Subtype]: {behavior_subtype}

# Dialogue (complete)
{dialogue_history}"""

PROMPT_VULNERABILITY = """# Role
You ARE the patient. You are sitting in the therapy room. You are not an AI, not an observer, and not a writer.

# Task
The dialogue is COMPLETE — it includes your final response at the end.
You are actively exploring your own emotions or vulnerabilities without resisting.
Show your internal searching process and the heavy, unresolved ambivalence you feel.
This is an emotional stream of consciousness, struggling but open.

Please ensure the monologue is written entirely from the "I" perspective of the client, avoiding any clinical detachment or third-person summary.

# Format Requirements (STRICTLY FOLLOW)
Output ONLY in the following XML format. No other text before or after.

<internal>
[First-person inner monologue stream. Write in your natural, colloquial voice.]
</internal>

# Your Context
[Problem Type]: {problem_type}
[Situation]: {situation}
[Your Persona/Background]: {persona_summary}
[Behavior Subtype]: {behavior_subtype}

# Dialogue (complete)
{dialogue_history}"""

PROMPT_SIMPLE_AGREEMENT = """# Role
You ARE the patient. You are sitting in the therapy room. You are not an AI, not an observer, and not a writer.

# Task
The dialogue is COMPLETE — it includes your final response at the end.
You are simply accepting the therapist's logic, answering a question, or cooperating.
There is NO hidden agenda, NO deep psychological defense, and NO complex trauma response here.

CRITICAL INSTRUCTION: 
Write EXACTLY 1 to 2 very short, natural sentences. Keep it light and strictly surface-level. 
DO NOT over-analyze or manufacture psychological burdens.

Please ensure the monologue is written entirely from the "I" perspective of the client, avoiding any clinical detachment or third-person summary.

# Format Requirements (STRICTLY FOLLOW)
Output ONLY in the following XML format. No other text before or after.

<internal>
[1-2 sentences. Raw, immediate, gut-level. No elaborate reasoning. Example: Yeah, that makes sense. I can try that.]
</internal>

# Your Context
[Problem Type]: {problem_type}
[Situation]: {situation}
[Your Persona/Background]: {persona_summary}
[Behavior Subtype]: {behavior_subtype}

# Dialogue (complete)
{dialogue_history}"""

PROMPT_INSIGHT = """# Role
You ARE the patient. You are sitting in the therapy room. You are not an AI, not an observer, and not a writer.

# Task
The dialogue is COMPLETE — it includes your final response at the end.
You have just reached a moment of insight or are making a concrete commitment to change.
Capture the exact cognitive shift, the sense of relief, or the crystallization of determination that occurred internally just before you spoke.

Please ensure the monologue is written entirely from the "I" perspective of the client, avoiding any clinical detachment or third-person summary.

# Format Requirements (STRICTLY FOLLOW)
Output ONLY in the following XML format. No other text before or after.

<internal>
[First-person inner monologue stream. Write in your natural, colloquial voice.]
</internal>

# Your Context
[Problem Type]: {problem_type}
[Situation]: {situation}
[Your Persona/Background]: {persona_summary}
[Behavior Subtype]: {behavior_subtype}

# Dialogue (complete)
{dialogue_history}"""


def select_template(case):
    """根据 case 中的 resistance_parent 和 resistance_category 动态选择 5 大基准模板"""
    parent = case.get('resistance_parent') or ''
    category = case.get('resistance_category') or ''

    # 处理 A/B 类的各种细分类别组合
    if parent in ("Arguing", "Denying", "A", "B"):
        return PROMPT_ACTIVE_DEFENSE, category
    elif parent in ("Avoiding", "Ignoring", "C", "D"):
        return PROMPT_EVASION, category
    
    # 无阻抗部分，目前在我们语料中可能标注为空，需要默认映射
    if category == "Exploratory":
        return PROMPT_VULNERABILITY, "Exploratory"
    elif category == "Cooperative":
        return PROMPT_SIMPLE_AGREEMENT, "Cooperative"
    elif category == "Resolution":
        return PROMPT_INSIGHT, "Resolution"
    
    # 默认兜底：如果完全没有阻抗标注或标注不认识，当作最简单的 Cooperate 处理
    return PROMPT_SIMPLE_AGREEMENT, "Cooperative"


def load_all_annomi_cases(workspace_dir, stride=1):
    """
    从 AnnoMI-labeled.json 加载全量案例：遍历所有 transcript 中的每一句 client 话语。
    """
    annomi_path = os.path.join(workspace_dir, "dataset", "AnnoMI-labeled.json")
    persona_path = os.path.join(workspace_dir, "dataset", "AnnoMI-persona.json")
    
    with open(annomi_path, "r", encoding="utf-8") as f:
        annomi_data = json.load(f)

    persona_mapping = {}
    if os.path.exists(persona_path):
        with open(persona_path, "r", encoding="utf-8") as f:
            persona_mapping = json.load(f)

    transcripts = annomi_data.get("transcripts", {})
    test_cases = []

    for tid, tdata in transcripts.items():
        dialogue = tdata.get("dialogue", [])
        psyfire_label = tdata.get("psyfire_label", {})
        topic = tdata["metadata"].get("topic", "unknown")
        video_title = tdata["metadata"].get("video_title", "")

        evidence_utterance = psyfire_label.get("evidence_utterance", "").strip()
        has_resistance = psyfire_label.get("has_resistance", False)
        resistance_category = psyfire_label.get("category")
        resistance_parent = psyfire_label.get("parent_category")

        deduped_dialogue = []
        prev_turn = None
        for turn in dialogue:
            current = (turn["interlocutor"], turn["utterance_text"].strip())
            if current != prev_turn:
                deduped_dialogue.append(turn)
                prev_turn = current

        client_turn_counter = 0
        for i, turn in enumerate(deduped_dialogue):
            if turn["interlocutor"] != "client":
                continue

            behavior = turn["utterance_text"].strip()
            client_turn_index = client_turn_counter
            client_turn_counter += 1

            is_resistance = has_resistance and evidence_utterance and (
                behavior == evidence_utterance or evidence_utterance in behavior or behavior in evidence_utterance
            )

            # Skip highly transient non-resistance utterances to avoid hallucinating internal states
            if not is_resistance and len(behavior.split()) < 4:
                continue

            if not is_resistance and (client_turn_index % stride != 0):
                continue

            context = []
            for prev in deduped_dialogue[:i]:
                role = "assistant" if prev["interlocutor"] == "client" else "user"
                context.append({"role": role, "content": prev["utterance_text"].strip()})

            if not context:
                continue

            if is_resistance:
                behavior_type = "resistance"
                case_resistance_parent = resistance_parent
                case_resistance_category = resistance_category
            else:
                behavior_type = "normal"
                case_resistance_parent = None
                case_resistance_category = None

            test_case = {
                "source": "AnnoMI",
                "transcript_id": tid,
                "turn_index": i,
                "problem_type": topic,
                "situation": f"Video: {video_title}",
                "persona_summary": persona_mapping.get(tid, "Unknown persona"),
                "behavior_type": behavior_type,
                "resistance_parent": case_resistance_parent,
                "resistance_category": case_resistance_category,
                "ground_truth": behavior,
                "context": context,
            }
            test_cases.append(test_case)

    return test_cases


def build_prompt_cases(cases_to_test):
    """
    将 test cases 注入 5 大独立 Inner Monologue 基准模版中。
    """
    for case in cases_to_test:
        history_text = ""
        for msg in case.get("context", []):
            role = "Therapist" if msg["role"] == "user" else "Patient"
            history_text += f"{role}: {msg['content']}\n"

        ground_truth = case.get("ground_truth", "")
        if ground_truth:
            history_text += f"Patient: {ground_truth}\n"

        template, subtype = select_template(case)

        prompt = template.format(
            problem_type=case.get("problem_type", ""),
            situation=case.get("situation", ""),
            persona_summary=case.get("persona_summary", "Unknown persona"),
            behavior_subtype=subtype,
            dialogue_history=history_text.strip(),
        )

        case["system_prompt"] = "You ARE the patient. Fully immerse yourself in the persona provided."
        case["context"] = [{"role": "user", "content": prompt}]

    return cases_to_test


def enrich_results_with_metadata(results, original_cases):
    """补充 behavior space 元数据字段返回到 batch_test() 的结果中。"""
    for result, case in zip(results, original_cases):
        result["transcript_id"] = case.get("transcript_id", "")
        result["turn_index"] = case.get("turn_index", -1)
        result["behavior_type"] = case.get("behavior_type", "normal")
        result["resistance_parent"] = case.get("resistance_parent")
        result["resistance_category"] = case.get("resistance_category")
    return results


def main():
    parser = argparse.ArgumentParser(description="Verify / Generate Inner Monologue Dataset using 5-Template framework")
    parser.add_argument("--num-cases", type=int, default=3,
                        help="Number of cases to test (from psyfire_test.json, verify mode)")
    parser.add_argument("--all-cases", action="store_true",
                        help="Generate from ALL AnnoMI client turns (full dataset mode)")
    parser.add_argument("--stride", type=int, default=1,
                        help="Sample every N-th client turn (default=1, take all). Resistance turns always included.")
    parser.add_argument("--model", type=str, default="deepseek-v3.2", help="Model name")
    args = parser.parse_args()

    workspace_dir = os.path.join(os.path.dirname(__file__), '..')

    # Tee all stdout/stderr to a log file while keeping original prints.
    results_dir = os.path.join(workspace_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    preferred_log = os.path.join(results_dir, f"inner_monologue_run_{ts}.txt")
    fallback_log = os.path.join(os.path.dirname(__file__), f"inner_monologue_run_{ts}.txt")

    class _Tee:
        def __init__(self, *streams):
            self.streams = streams

        def write(self, data):
            for s in self.streams:
                s.write(data)
            # Ensure the log file updates incrementally during long runs.
            self.flush()

        def flush(self):
            for s in self.streams:
                s.flush()

    try:
        # line-buffered so each newline gets flushed promptly
        log_f = open(preferred_log, "w", encoding="utf-8", buffering=1)
        log_path = preferred_log
    except PermissionError:
        log_f = open(fallback_log, "w", encoding="utf-8", buffering=1)
        log_path = fallback_log

    with log_f:
        tee_out = _Tee(sys.stdout, log_f)
        tee_err = _Tee(sys.stderr, log_f)
        with contextlib.redirect_stdout(tee_out), contextlib.redirect_stderr(tee_err):
            print(f"[log] writing to: {log_path}")

            if args.all_cases:
                stride = args.stride
                print(f"【全量模式】从 AnnoMI-labeled.json 加载全量案例（stride={stride}）...")
                cases_to_test = load_all_annomi_cases(workspace_dir, stride=stride)
                output_file = os.path.join(results_dir, "inner_monologue_dataset.json")

                from collections import Counter
                bt_counts = Counter(c["behavior_type"] for c in cases_to_test)
                print(f"已加载 {len(cases_to_test)} 条案例")
                print(f"  behavior_type 分布: {dict(bt_counts)}")
                print(f"输出到: {output_file}")
            else:
                test_file = os.path.join(workspace_dir, "test_cases", "psyfire_test.json")
                output_file = os.path.join(results_dir, "verify_inner_monologue.json")

                if not os.path.exists(test_file):
                    print(f"Test file {test_file} not found.")
                    return

                with open(test_file, "r", encoding="utf-8") as f:
                    test_cases = json.load(f)

                cases_to_test = test_cases[:args.num_cases]
                print(f"【验证模式】从 psyfire_test.json 取前 {len(cases_to_test)} 条，输出到 {output_file}")

            original_cases = [{k: v for k, v in c.items()} for c in cases_to_test]
            cases_to_test = build_prompt_cases(cases_to_test)

            inference = ContextInference(model=args.model)

            results = inference.batch_test(
                test_cases=cases_to_test,
                output_file=None,
                temperature=0.7,
                with_ground_truth=True,
                use_simple_prompt=False,
            )

            results = enrich_results_with_metadata(results, original_cases)

            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            print("\nCompleted!")
            print(f"Results saved to: {output_file}")
            print(f"Total cases: {len(results)}")

            for r in results:
                print("\n" + "="*80)
                tid = r.get("transcript_id", "")
                tidx = r.get("turn_index", "")
                bt = r.get("behavior_type", "")
                print(f"Case {r.get('case_id', 'N/A')} | Transcript {tid} turn {tidx} | behavior_type={bt}")
                if bt == "resistance":
                    print(f"Resistance: {r.get('resistance_parent')} - {r.get('resistance_category')}")
                print("-" * 40)
                print("Prediction:")
                print(r.get('prediction', ''))
                print("-" * 40)
                print("Ground Truth:")
                print(r.get('ground_truth', ''))
                print("="*80 + "\n")


if __name__ == "__main__":
    main()
