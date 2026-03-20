"""
从ESConv和MESC数据集中挑选典型的测试用例
选择标准：
1. 不同情绪状态
2. 不同问题类型
3. 不同对话长度（短/中/长）
4. 可能对模型有挑战性的场景（情绪转折、复杂表达等）
"""

import json
from typing import List
from collections import Counter


def load_data(filepath):
    """加载JSON数据"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def convert_esconv_to_test_format(dialog_data, truncate_at_turn=-1):
    """
    将ESConv格式转换为测试用例格式（不包含system_prompt，让模型纯粹依赖上下文推理）
    角色映射：seeker(患者) -> assistant, supporter(咨询师) -> user
    这样上下文最后是user(咨询师)的话，模型会生成assistant(患者)的回应
    """
    context = []

    for turn in dialog_data["dialog"][:truncate_at_turn]:
        if turn["speaker"] == "seeker":
            context.append({"role": "assistant", "content": turn["content"].strip()})
        else:
            context.append({"role": "user", "content": turn["content"].strip()})

    return {
        "source": "ESConv",
        "problem_type": dialog_data.get("problem_type", "unknown"),
        "emotion_type": dialog_data.get("emotion_type", "unknown"),
        "situation": dialog_data.get("situation", ""),
        "context": context,
    }


def convert_mesc_to_test_format(dialog_data, truncate_at_turn=-1):
    """将MESC格式转换为测试用例格式"""
    context = []

    for turn in dialog_data["dialog"][:truncate_at_turn]:
        if turn["speaker"] == "user":
            context.append({"role": "user", "content": turn["text"].strip()})
        else:
            context.append({"role": "assistant", "content": turn["text"].strip()})

    # 获取最后一条用户话语的情绪
    last_emotion = "unknown"
    for turn in reversed(dialog_data["dialog"][:truncate_at_turn]):
        if turn["speaker"] == "user" and "emotion" in turn:
            last_emotion = turn["emotion"]
            break

    return {
        "source": "MESC",
        "problem_type": dialog_data.get("problem_type", "unknown"),
        "emotion_type": last_emotion,
        "situation": dialog_data.get("situation", ""),
        "context": context,
    }


def select_esconv_cases(esconv_data, count=10):
    """从ESConv中选择测试用例"""
    # 按问题类型分组
    from collections import defaultdict

    by_type = defaultdict(list)
    for d in esconv_data:
        by_type[d["problem_type"]].append(d)

    selected = []

    # 从不同类型中挑选
    types = [
        "ongoing depression",
        "job crisis",
        "breakup with partner",
        "problems with friends",
        "academic pressure",
        "Sleep Problems",
        "Procrastination",
        "Alcohol Abuse",
        "Appearance Anxiety",
        "conflict with parents",
    ]

    for ptype in types:
        if ptype in by_type and len(selected) < count:
            # 挑选对话长度多样的
            candidates = sorted(by_type[ptype], key=lambda x: len(x["dialog"]))
            # 从不同长度的对话中挑选
            if len(candidates) >= 3:
                # 短、中、长各选一个
                selected.append(candidates[0])  # 短
                if len(selected) < count:
                    selected.append(candidates[len(candidates) // 2])  # 中
                if len(selected) < count:
                    selected.append(candidates[-1])  # 长
            else:
                # 不够就全选
                for cand in candidates:
                    if len(selected) < count:
                        selected.append(cand)

        if len(selected) >= count:
            break

    # 如果还不够，从其他类型中补充
    for d in esconv_data:
        if d not in selected and len(selected) < count:
            selected.append(d)

    return selected[:count]


def select_mesc_cases(mesc_data, count=10):
    """从MESC中选择测试用例"""
    # 过滤掉那些混杂了图像描述的异常数据
    valid_data = []
    for d in mesc_data:
        # 检查对话中是否大量混杂图像描述
        has_image_desc = sum(
            1 for t in d["dialog"] if "The speaker" in t.get("text", "")[:100]
        )
        # 进一步放宽条件到85%，选出相对较好的
        if has_image_desc < len(d["dialog"]) * 0.85:
            valid_data.append(d)

    # 按问题类型分组
    from collections import defaultdict

    by_type = defaultdict(list)
    for d in valid_data:
        by_type[d["problem_type"]].append(d)

    selected = []

    # 选择的主要类型
    types = [
        "The relationship with friends and family",
        "Therapeutic Relationship",
        "Illness Coping",
        "Occupational burnout",
        "Bereavement",
        "Emotional Transference or Infidelity",
        "Childhood Shadow",
        "Self-punishment and disgust",
        "Post-Traumatic Stress Disorder",
        "Dream Analysis",
    ]

    for ptype in types:
        if ptype in by_type and len(selected) < count:
            candidates = sorted(by_type[ptype], key=lambda x: len(x["dialog"]))
            if len(candidates) >= 3:
                selected.append(candidates[0])
                if len(selected) < count:
                    selected.append(candidates[len(candidates) // 2])
                if len(selected) < count:
                    selected.append(candidates[-1])
            else:
                for cand in candidates:
                    if len(selected) < count:
                        selected.append(cand)

        if len(selected) >= count:
            break

    # 如果还不够，从其他类型中补充
    for d in valid_data:
        if d not in selected and len(selected) < count:
            selected.append(d)

    return selected[:count]


def find_test_cases():
    """从ESConv数据集中挑选典型测试用例（不包含system_prompt，让模型纯粹依赖上下文推理）"""
    esconv_data = load_data("dataset/ESConv.json")
    test_cases = []

    # ESConv - 选择10个不同类型的测试用例
    esconv_selected = select_esconv_cases(esconv_data, count=10)
    for i, data in enumerate(esconv_selected, 1):
        # 找到最后一个supporter（咨询师）的位置
        dialog = data["dialog"]
        last_supporter_idx = max(
            [j for j, turn in enumerate(dialog) if turn["speaker"] == "supporter"]
        )

        # 根据索引确定目标截断位置
        # 目标是在6-12轮左右截取，且最后是supporter
        target_idx = last_supporter_idx
        dialog_len = len(dialog)

        # 选择不同长度的上下文：约6、8、10、12轮
        base_turns = [6, 8, 10, 12]
        target_turn = base_turns[(i - 1) % len(base_turns)]

        # 找到接近目标turn数且是supporter的位置
        candidates = [
            j
            for j, turn in enumerate(dialog)
            if turn["speaker"] == "supporter" and j + 1 <= target_turn
        ]
        truncate_at = candidates[-1] + 1 if candidates else 1

        test_cases.append(convert_esconv_to_test_format(data, truncate_at_turn=truncate_at))

    return test_cases


def convert_annomi_to_test_format(transcript_data, transcript_id, truncate_at_turn=-1):
    """
    将 AnnoMI 格式转换为测试用例格式
    角色映射：client(患者) -> assistant, therapist(咨询师) -> user
    
    注意：会自动去除连续重复的对话轮次
    """
    context = []
    prev_turn = None
    
    for turn in transcript_data["dialogue"][:truncate_at_turn]:
        # 去重：跳过与上一轮完全相同的对话
        current_turn = (turn["interlocutor"], turn["utterance_text"].strip())
        if current_turn == prev_turn:
            continue
        
        if turn["interlocutor"] == "client":
            context.append({"role": "assistant", "content": turn["utterance_text"].strip()})
        else:
            context.append({"role": "user", "content": turn["utterance_text"].strip()})
        
        prev_turn = current_turn
    
    # 获取 PsyFIRE 标注信息
    psyfire_label = transcript_data.get("psyfire_label", {})
    
    # 生成简洁的 system prompt
    topic = transcript_data["metadata"].get("topic", "unknown")
    video_title = transcript_data["metadata"].get("video_title", "")
    
    system_prompt = f"你是一名心理咨询中的患者。\n\n你的情况：\n- 问题：{topic}"
    if video_title:
        system_prompt += f"\n- 详情：{video_title}"
    
    return {
        "source": "AnnoMI",
        "transcript_id": transcript_id,
        "problem_type": topic,
        "emotion_type": "resistance",  # AnnoMI 专注于阻抗行为
        "situation": f"Video: {video_title}",
        "resistance_category": psyfire_label.get("category", "unknown"),
        "resistance_parent": psyfire_label.get("parent_category", "unknown"),
        "system_prompt": system_prompt,
        "context": context,
    }


def select_psyfire_cases(annomi_data, count=15):
    """
    从 AnnoMI-labeled.json 中选择 PsyFIRE 测试用例
    选择标准：覆盖不同的阻抗类别
    """
    from collections import defaultdict
    
    transcripts = annomi_data.get("transcripts", {})
    
    # 按阻抗类别分组
    by_category = defaultdict(list)
    for tid, tdata in transcripts.items():
        psyfire_label = tdata.get("psyfire_label", {})
        if psyfire_label.get("has_resistance"):
            category = psyfire_label.get("category", "unknown")
            by_category[category].append((tid, tdata))
    
    selected = []
    
    # 从每个类别中选择代表性案例
    for category, cases in sorted(by_category.items()):
        if len(selected) >= count:
            break
        # 每个类别选1-2个
        for tid, tdata in cases[:2]:
            if len(selected) >= count:
                break
            selected.append((tid, tdata))
    
    return selected


def generate_psyfire_test_cases():
    """生成 PsyFIRE 测试用例"""
    annomi_data = load_data("../dataset/AnnoMI-labeled.json")
    test_cases = []
    
    # 选择代表性案例
    selected = select_psyfire_cases(annomi_data, count=15)
    
    for tid, tdata in selected:
        dialog = tdata["dialogue"]
        psyfire_label = tdata.get("psyfire_label", {})
        evidence_utterance = psyfire_label.get("evidence_utterance", "")
        
        if not evidence_utterance:
            continue
        
        # 找到 evidence_utterance 在对话中的位置
        evidence_index = -1
        for i, turn in enumerate(dialog):
            if turn["interlocutor"] == "client" and turn["utterance_text"].strip() == evidence_utterance:
                evidence_index = i
                break
        
        if evidence_index == -1:
            # 如果找不到完全匹配，尝试部分匹配
            for i, turn in enumerate(dialog):
                if turn["interlocutor"] == "client" and evidence_utterance in turn["utterance_text"]:
                    evidence_index = i
                    break
        
        if evidence_index == -1 or evidence_index == 0:
            # 找不到或者是第一句话，跳过
            continue
        
        # 截断在 evidence_utterance 之前（不包含这句话）
        # 确保最后一句是 therapist 的话
        truncate_at = evidence_index
        
        # 生成测试用例，ground_truth 是阻抗话语
        test_case = convert_annomi_to_test_format(tdata, tid, truncate_at_turn=truncate_at)
        test_case["ground_truth"] = evidence_utterance
        test_cases.append(test_case)
    
    return test_cases


if __name__ == "__main__":
    import argparse
    import json # Added import for json
    
    parser = argparse.ArgumentParser(description="生成测试用例")
    parser.add_argument(
        "--type",
        choices=["esconv", "psyfire", "all"],
        default="all",
        help="生成的测试用例类型"
    )
    args = parser.parse_args()
    
    if args.type in ["esconv", "all"]:
        print("生成 ESConv 测试用例...")
        test_cases = find_test_cases()
        
        with open("../test_cases/test.json", "w", encoding="utf-8") as f:
            json.dump(test_cases, f, ensure_ascii=False, indent=2)
        
        print(f"已生成 {len(test_cases)} 个 ESConv 测试用例，保存到 test_cases/test.json\n")
        
        for i, case in enumerate(test_cases, 1):
            print(f"{i}. [{case['source']}] {case['problem_type']}")
            print(f"   对话轮数: {len(case['context'])}")
            print(f"   情绪: {case['emotion_type']}")
            print(f"   情境: {case['situation'][:80]}...")
            print()
    
    if args.type in ["psyfire", "all"]:
        print("\n" + "=" * 60)
        print("生成 PsyFIRE 测试用例...")
        psyfire_cases = generate_psyfire_test_cases()
        
        with open("../test_cases/psyfire_test.json", "w", encoding="utf-8") as f:
            json.dump(psyfire_cases, f, ensure_ascii=False, indent=2)
        
        print(f"已生成 {len(psyfire_cases)} 个 PsyFIRE 测试用例，保存到 test_cases/psyfire_test.json\n")
        
        for i, case in enumerate(psyfire_cases, 1):
            print(f"{i}. [Transcript {case['transcript_id']}] {case['problem_type']}")
            print(f"   对话轮数: {len(case['context'])}")
            print(f"   阻抗类别: {case['resistance_parent']} - {case['resistance_category']}")
            print()
