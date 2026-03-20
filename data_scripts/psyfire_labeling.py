import json
import os
import requests
import time
from typing import Dict, List, Any, Optional

# API Configuration
API_BASE_URL = "https://api.apiplus.org/v1"
API_KEY = "sk-g1AVBm70fre57jGr8GQuZyCTOzUPHPuaGHqL7NmcrGQfx3On"
MODEL_NAME = "gpt-4o"  # You can change this to deepseek-chat or other models supported by the provider

PSYFIRE_PROMPT = """
你是一个专业的心理咨询分析师，精通 PsyFIRE 阻抗行为分类框架。
你的任务是阅读一段心理咨询对话，并识别出该对话中最显著的一个阻抗（Resistance）行为。

PsyFIRE 框架分类如下：

1. 争辩 (Arguing) —— 直接挑战咨询师
- 质疑 (Challenging)：直接质疑咨询师的专业能力、经验或所提供信息的准确性。
- 贬低 (Discounting)：通过否定建议的价值或咨询师个人权威来表达轻视。

2. 否认 (Denying) —— 拒绝承认或承担责任
- 责备 (Blaming)：将问题归咎于他人或客观环境。
- 不同意 (Disagreeing)：直接反对咨询师观点，常伴随“但是...”。
- 找借口 (Excusing)：寻找各种理由证明改变是不可能的。
- 轻视 (Minimizing)：淡化问题的严重性或影响。
- 悲观 (Pessimism)：对效果或未来表现出绝望态度。
- 犹豫 (Reluctance)：在表达或尝试改变时显得被动、不确定。
- 不情愿 (Unwillingness)：明确拒绝执行具体任务或建议。

3. 回避 (Avoiding) —— 物理或心理上的撤退
- 极简对话 (Minimum Talk)：提供极其简短、封闭式的回答（如“哦”、“嗯”）。
- 设定限制 (Limit Setting)：明确划定某些话题为禁区，拒绝讨论。

4. 忽略 (Ignoring) —— 关注力转移
- 关注力不足 (Inattention)：走神、没听清或没有回应。
- 偏离主题 (Sidetracking)：故意将话题引向无关方向，规避深刻或痛苦讨论。

如果没有发现任何阻抗行为，请标注为“无”。

请以 JSON 格式输出，包含以下字段：
- "has_resistance": 布尔值，是否有阻抗。
- "category": 如果有，提供最显著的子类别名称（例如：“质疑”）；如果没有，设为 null。
- "parent_category": 如果有，所属的大类名称（例如：“争辩”）；如果没有，设为 null。
- "evidence_utterance": 对应阻抗行为的最具代表性的来访者话语。
- "reasoning": 简要说明为什么它是该类别。
"""

def call_llm(dialogue_text: str) -> Optional[Dict[str, Any]]:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": PSYFIRE_PROMPT},
            {"role": "user", "content": f"请分析以下对话中的阻抗行为：\n\n{dialogue_text}"}
        ],
        "response_format": {"type": "json_object"}
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return json.loads(result['choices'][0]['message']['content'])
        except Exception as e:
            print(f"Error calling LLM (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    return None

def format_dialogue(dialogue: List[Dict[str, str]]) -> str:
    formatted = ""
    for entry in dialogue:
        role = "咨询师" if entry['interlocutor'] == 'therapist' else "来访者"
        formatted += f"{role}: {entry['utterance_text']}\n"
    return formatted

def process_labeling(input_file: str, output_file: str):
    print(f"Reading data from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    transcripts = data.get('transcripts', {})
    labeled_results = {}
    
    total = len(transcripts)
    count = 0
    
    for tid, content in transcripts.items():
        count += 1
        print(f"Processing transcript {tid} ({count}/{total})...")
        
        dialogue_text = format_dialogue(content['dialogue'])
        label_info = call_llm(dialogue_text)
        
        if label_info:
            content['psyfire_label'] = label_info
        else:
            content['psyfire_label'] = {"error": "Failed to label"}
            
        labeled_results[tid] = content
        
        # Save progress every 5 transcripts
        if count % 5 == 0:
            save_data(data, labeled_results, output_file)
            
    save_data(data, labeled_results, output_file)
    print(f"Labeling complete. Results saved to {output_file}")

def save_data(data: Dict, results: Dict, output_file: str):
    data['transcripts'] = results
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_path = "scr data/AnnoMI-simple-high-resistance.json"
    output_path = "scr data/AnnoMI-simple-high-resistance-labeled.json"
    process_labeling(input_path, output_path)
