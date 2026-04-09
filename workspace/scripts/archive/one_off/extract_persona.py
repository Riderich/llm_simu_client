import sys
import os
import json
import argparse
from tqdm import tqdm

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from context_inference import ContextInference

EXTRACT_PERSONA_SYSTEM = "You are an expert clinical psychologist analyzing a therapy transcript."

EXTRACT_PERSONA_PROMPT = """# Task
Read the following complete therapy transcript and extract a concise "Patient Persona/Background" summary.

Focus ONLY on identifying:
1. The patient's core problem, struggle, or addiction.
2. Their primary emotional state or underlying fear.
3. Their general attitude towards the therapy, therapist, or their own situation (e.g., defensive, cooperative, hopeless).

# Format Requirements
Write a single, highly condensed paragraph (3-4 sentences maximum). DO NOT use bullet points. Write in the third person.

# Example Output
The patient is a 34-year-old male struggling with a long history of drug dealing and recent incarceration. He feels trapped between a mundane, low-paying pro-social life and the easy money of his past, though he is currently deeply fearful of losing his supportive partner, Fiona, if he relapses. While somewhat guarded and unsure of how to change, he shows a lingering desire to find a new path but lacks the confidence and skills to do so.

# Dialogue Transcript
{transcript}

# Persona Summary:"""

def build_transcript_text(dialogue):
    """将 dialogue 列表转化为长文本"""
    text = ""
    for turn in dialogue:
        role = "Therapist" if turn["interlocutor"] == "therapist" else "Patient"
        text += f"{role}: {turn['utterance_text'].strip()}\n"
    return text.strip()

def main():
    parser = argparse.ArgumentParser(description="Extract Patient Persona from transcripts")
    parser.add_argument("--model", type=str, default="deepseek-v3.2", help="Model name for extraction")
    args = parser.parse_args()

    workspace_dir = os.path.join(os.path.dirname(__file__), '..')
    annomi_path = os.path.join(workspace_dir, "dataset", "AnnoMI-labeled.json")
    output_path = os.path.join(workspace_dir, "dataset", "AnnoMI-persona.json")

    print(f"Loading dataset from {annomi_path}...")
    with open(annomi_path, "r", encoding="utf-8") as f:
        annomi_data = json.load(f)

    transcripts = annomi_data.get("transcripts", {})
    test_cases = []

    # 为每个 transcript 构建提取用例
    for tid, tdata in transcripts.items():
        dialogue = tdata.get("dialogue", [])
        transcript_text = build_transcript_text(dialogue)

        prompt = EXTRACT_PERSONA_PROMPT.format(transcript=transcript_text)
        
        case = {
            "transcript_id": tid,
            "system_prompt": EXTRACT_PERSONA_SYSTEM,
            "context": [{"role": "user", "content": prompt}]
        }
        test_cases.append(case)

    print(f"\nExtracting persona for {len(test_cases)} transcripts using {args.model}...")

    inference = ContextInference(model=args.model)
    
    # 使用 batch_test，但这可能很长，由于是 transcript 级别（只有133个），可以一次性跑
    results = inference.batch_test(
        test_cases=test_cases,
        output_file=None,
        temperature=0.3, # 低温度保证事实提取的一致性
        with_ground_truth=False,
        use_simple_prompt=False,
    )

    # 将提取出的 Persona 保存为 mapping: { transcript_id: persona_string }
    persona_mapping = {}
    for r, case in zip(results, test_cases):
        tid = case["transcript_id"]
        persona = r.get("prediction", "").strip()
        persona_mapping[tid] = persona

    print(f"\nExtraction complete. Saving to {output_path}...")
    
    # 存入一个专注保存元数据的 json，供 verify_psyfire_prompt.py 读取
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(persona_mapping, f, ensure_ascii=False, indent=2)
        
    print("Done! Here is a sample persona:")
    sample_tid = next(iter(persona_mapping))
    print(f"[{sample_tid}]:\n{persona_mapping[sample_tid]}")


if __name__ == "__main__":
    main()
