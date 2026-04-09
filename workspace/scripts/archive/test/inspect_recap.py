# RECAP 数据目标格式草案
# 任务：将 ClientResistance_decrypted.json 解析并规范化

样本来源：
    {
        "text": "咨询师：...\n来访者：...\n咨询师：...\n来访者：...",  # 多轮对话文本
        "label": ["否认-不认同"],
        "binary_label": ["阻抗"]
    }

目标格式：
    {
        "source": "RECAP",
        "dialogue": [
            {"role": "user",      "content": "咨询师的话"},
            {"role": "assistant", "content": "来访者的话"},
            ...
        ],
        "target_utterance": "最后一句来访者的话（标注目标）",
        "resistance_label": {
            "raw": "否认-不认同",          # 原始中文标签
            "parent": "Denying",          # 翻译后父类（英文）
            "category": "Disagreeing",    # 翻译后子类（英文）
            "has_resistance": True
        }
    }

主要处理步骤：
1. 按换行符将 text 分割成若干轮
2. 识别发言者（来访者/咨询师）并分配 role（assistant/user）
3. 提取最后一句 client 发言作 target_utterance
4. 将中文 label 映射为英文（parent + category），参照 数据集总览.md 的映射表
