"""
RECAP 合作类样本（E1/E2/E3）Inner Monologue 测试
基于 5 套中文提示词模板
"""

import sys
import os
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from context_inference import ContextInference

PROMPT_ACTIVE_DEFENSE_ZH = """# 角色设定
你就是这位来访者。你此刻正坐在咨询室里。你不是AI，不是旁观者，也不是作家。

# 任务
对话已经完整——最后一句就是你刚才说出口的话。
请推断在你开口之前，脑海中闪过的那段防御性内心独白。

此刻，隐藏在你防御外壳背后的，是什么原始情绪或恐惧？用自言自语的方式自然地写出来。
你不只是在反应——你在守护某样东西。

请确保独白完全以来访者的第一人称"我"来书写，避免任何临床分析式的客观描述或第三人称总结。

# 格式要求（严格遵守）
仅以以下 XML 格式输出，前后不要有任何其他文字。

<internal>
我知道她说得没错，但我就是不想承认。
</internal>

# 你的背景
【行为子类型】：{behavior_subtype}

# 对话（完整）
{dialogue_history}"""

PROMPT_EVASION_ZH = """# 角色设定
你就是这位来访者。你此刻正坐在咨询室里。你不是AI，不是旁观者，也不是作家。

# 任务
对话已经完整——最后一句就是你刚才说出口的话。
你正在回避、转移话题，或者做出表面的顺从。

揭示你刻意没有说出口的东西。当你选择退缩或回避时，你有意压制了哪些想法、恐惧或积怨？
完全聚焦于表面互动之下那层被隐藏的潜台词。
最多2-3句话。

请确保独白完全以来访者的第一人称"我"来书写，避免任何临床分析式的客观描述或第三人称总结。

# 格式要求（严格遵守）
仅以以下 XML 格式输出，前后不要有任何其他文字。

<internal>
只要我现在顺着他说，他就会转移话题了。这件事我实在不想再碰了。
</internal>

# 你的背景
【行为子类型】：{behavior_subtype}

# 对话（完整）
{dialogue_history}"""

PROMPT_VULNERABILITY_ZH = """# 角色设定
你就是这位来访者。你此刻正坐在咨询室里。你不是AI，不是旁观者，也不是作家。

# 任务
对话已经完整——最后一句就是你刚才说出口的话。
你正在不带抵触地主动探索自己的情绪或脆弱之处。
展现你内心的搜寻过程，以及那种沉重的、尚未解开的矛盾感。
这是一段情绪化的意识流，挣扎着，但是开放的。

请确保独白完全以来访者的第一人称"我"来书写，避免任何临床分析式的客观描述或第三人称总结。

# 格式要求（严格遵守）
仅以以下 XML 格式输出，前后不要有任何其他文字。

<internal>
用自然口语化的声音书写。
</internal>

# 你的背景
【行为子类型】：{behavior_subtype}

# 对话（完整）
{dialogue_history}"""

PROMPT_SIMPLE_AGREEMENT_ZH = """# 角色设定
你就是这位来访者。你此刻正坐在咨询室里。你不是AI，不是旁观者，也不是作家。

# 任务
对话已经完整——最后一句就是你刚才说出口的话。
你只是在接受咨询师的逻辑、回答一个问题，或者自然地配合。
这里没有隐藏的动机，没有深层的心理防御，也没有复杂的心理创伤反应。

【关键要求】：
写恰好1到2句非常简短、自然的话。保持轻松，严格停留在表面层次。
不要过度分析，不要凭空制造心理负担。

请确保独白完全以来访者的第一人称"我"来书写，避免任何临床分析式的客观描述或第三人称总结。

# 格式要求（严格遵守）
仅以以下 XML 格式输出，前后不要有任何其他文字。

<internal>
嗯，她说的有道理，我可以试试。
</internal>

# 你的背景
【行为子类型】：{behavior_subtype}

# 对话（完整）
{dialogue_history}"""

PROMPT_INSIGHT_ZH = """# 角色设定
你就是这位来访者。你此刻正坐在咨询室里。你不是AI，不是旁观者，也不是作家。

# 任务
对话已经完整——最后一句就是你刚才说出口的话。
你刚刚迎来了一个顿悟的瞬间，或者正在做出切实的改变承诺。
捕捉那个认知转变的确切时刻——在你开口之前，内心涌现的如释重负感，或者那种决心凝结的瞬间。

请确保独白完全以来访者的第一人称"我"来书写，避免任何临床分析式的客观描述或第三人称总结。

# 格式要求（严格遵守）
仅以以下 XML 格式输出，前后不要有任何其他文字。

<internal>
用自然口语化的声音书写。
</internal>

# 你的背景
【行为子类型】：{behavior_subtype}

# 对话（完整）
{dialogue_history}"""

SYSTEM_PROMPT_ZH = "你就是这位来访者。请完全沉浸在所给的角色中。"


def select_template(item):
    rl = item.get("resistance_label", {})
    parent = rl.get("parent", "")
    category = rl.get("category", "")
    subtype = rl.get("cooperative_subtype", "")

    if parent in ("Arguing", "Denying"):
        return PROMPT_ACTIVE_DEFENSE_ZH, category
    elif parent in ("Avoiding", "Ignoring"):
        return PROMPT_EVASION_ZH, category
    elif subtype == "E1" or category == "Exploratory":
        return PROMPT_VULNERABILITY_ZH, "E1-探索/脆弱"
    elif subtype == "E3" or category == "Resolution":
        return PROMPT_INSIGHT_ZH, "E3-领悟/决断"
    else:
        return PROMPT_SIMPLE_AGREEMENT_ZH, "E2-简单顺从"


def build_dialogue_text(dialogue):
    lines = []
    for turn in dialogue:
        role = "咨询师" if turn["role"] == "user" else "来访者"
        lines.append(f"{role}：{turn['content'].strip()}")
    return "\n".join(lines)


def extract_internal(text):
    match = re.search(r"<internal>(.*?)</internal>", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def generate_one(idx, item, client, model, max_retries=3):
    target = item.get("target_utterance", "")
    if len(target.replace(" ", "")) < 3:
        return idx, "[SKIPPED - too short]"

    template, subtype = select_template(item)
    dialogue_text = build_dialogue_text(item.get("dialogue", []))

    prompt = template.format(
        behavior_subtype=subtype,
        dialogue_history=dialogue_text,
    )

    messages = [{"role": "user", "content": prompt}]

    for attempt in range(max_retries):
        try:
            response = client.client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": SYSTEM_PROMPT_ZH}] + messages,
                temperature=0.7,
                max_tokens=500,
            )
            text = response.choices[0].message.content
            result = extract_internal(text)

            if result:
                return idx, result

            messages.append({"role": "assistant", "content": text})
            messages.append({
                "role": "user",
                "content": "你的回复格式不正确。请仅输出以下格式，不要有其他文字：\n<internal>\n[内心独白内容]\n</internal>"
            })
            response2 = client.client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": SYSTEM_PROMPT_ZH}] + messages,
                temperature=0,
                max_tokens=500,
            )
            text2 = response2.choices[0].message.content
            result2 = extract_internal(text2)
            if result2:
                return idx, result2

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return idx, f"ERROR: {e}"

    return idx, "ERROR: max retries exceeded"


def main():
    parser = argparse.ArgumentParser(description="RECAP 合作类 Inner Monologue 测试")
    parser.add_argument("--input", default="test_cases/cooperation_test.json")
    parser.add_argument("--output", default="results/cooperation_im_test.json")
    parser.add_argument("--model", default="deepseek-v3.2")
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()

    workspace_dir = os.path.join(os.path.dirname(__file__), '..')
    input_path = os.path.join(workspace_dir, args.input)
    output_path = os.path.join(workspace_dir, args.output)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"总样本数：{len(data)}")
    for i, item in enumerate(data):
        subtype = item.get("resistance_label", {}).get("cooperative_subtype")
        target = item.get("target_utterance", "")[:40]
        print(f"[{i}] {subtype} | {target}")

    results = []
    inference = ContextInference(model=args.model)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(generate_one, i, item, inference, args.model): i
            for i, item in enumerate(data)
        }

        for future in as_completed(futures):
            idx, im = future.result()
            results.append({
                "_recap_idx": data[idx].get("_recap_idx"),
                "target_utterance": data[idx].get("target_utterance"),
                "resistance_label": data[idx].get("resistance_label"),
                "inner_monologue": im,
                "dialogue": data[idx].get("dialogue"),
            })

            status = "✓" if im and not im.startswith("ERROR:") else "✗"
            print(f"[{idx+1}/{len(data)}] {status} | {data[idx].get('target_utterance','')[:30]}")
            if im and not im.startswith("ERROR:"):
                print(f"  → {im[:80]}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n完成！输出到：{output_path}")


if __name__ == "__main__":
    import argparse
    main()
