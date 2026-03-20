# AnnoMI-Simple 高阻抗对话提取报告

## 数据来源

本数据集从 `AnnoMI-simple.json` 中提取，基于 `AnnoMI-full.json` 的筛选结果。

- **源文件**: AnnoMI-simple.json
- **筛选依据**: AnnoMI-high-resistance.json（从完整版筛选的32个高阻抗对话ID）
- **数据特点**: 简化版只包含对话内容，无详细标注信息

## 筛选标准（应用于完整版）

**方案F：高质量 + 灵活阻抗标准**

- **MI质量**: high
- **阻抗标准**: sustain talk比例 ≥ 25% 或 sustain次数 ≥ 8

注：简化版不包含 `client_talk_type` 标注，但对话ID与完整版一致。

## 提取结果摘要

- **提取对话数量**: 32 个
- **平均对话轮次**: 224.3
- **平均Client发言**: 111.6

**阻抗特征（来自完整版标注）：**
- 平均sustain比例: 28.5%
- 平均sustain次数: 17.2
- sustain比例范围: 6.8% - 72.2%

## 主题分布

| 主题 | 数量 |
|------|------|
| reducing alcohol consumption | 6 |
| reducing recidivism | 5 |
| smoking cessation | 5 |
| taking medicine / following medical procedure | 3 |
| reducing drug use | 2 |
| diabetes management | 2 |
| reducing self-harm | 2 |
| charging battery | 1 |
| more exercise / increasing activity | 1 |
| increasing activity; taking medicine / following medical procedure | 1 |
| avoiding DOI | 1 |
| reducing drug use; following medical procedure | 1 |
| unidentifiable | 1 |
| birth control | 1 |

## 详细对话列表

| ID | 对话轮次 | Client发言数 | 主题 |
|----|---------|------------|------|
| 1 | 37 | 18 | reducing alcohol consumption |
| 5 | 203 | 101 | reducing recidivism |
| 7 | 660 | 330 | reducing alcohol consumption |
| 11 | 15 | 7 | reducing recidivism |
| 13 | 14 | 7 | taking medicine / following medical procedure |
| 19 | 17 | 8 | reducing recidivism |
| 21 | 248 | 125 | reducing alcohol consumption |
| 24 | 22 | 11 | smoking cessation  |
| 28 | 123 | 61 | smoking cessation  |
| 30 | 29 | 14 | charging battery |
| 34 | 117 | 58 | reducing alcohol consumption |
| 55 | 650 | 320 | reducing drug use |
| 56 | 1750 | 870 | more exercise / increasing activity |
| 61 | 126 | 63 | increasing activity; taking medicine / following m |
| 64 | 262 | 132 | reducing drug use |
| 65 | 35 | 18 | smoking cessation |
| 66 | 310 | 150 | diabetes management |
| 81 | 21 | 9 | taking medicine / following medical procedure |
| 84 | 235 | 117 | reducing recidivism |
| 85 | 131 | 65 | taking medicine / following medical procedure |
| 95 | 36 | 18 | reducing self-harm |
| 96 | 92 | 46 | reducing alcohol consumption |
| 98 | 394 | 197 | avoiding DOI |
| 107 | 18 | 9 | reducing self-harm |
| 109 | 460 | 230 | smoking cessation |
| 111 | 59 | 29 | reducing drug use; following medical procedure |
| 113 | 50 | 25 | smoking cessation |
| 114 | 24 | 12 | reducing alcohol consumption |
| 121 | 598 | 299 | diabetes management |
| 122 | 26 | 13 | unidentifiable |
| 129 | 36 | 18 | birth control |
| 133 | 381 | 190 | reducing recidivism |

## 对话样例

### Transcript 95 - 减少自残

**主题**: reducing self-harm
**视频**: MI 5 30 18
**对话轮次**: 36

**对话片段（前10轮）**:

1. **THERAPIST**: Right. Hi, Ruth, thank you for coming today. How are you?

2. **CLIENT**: Um, okay. Just, I don't even know why I'm doing this anymore. I'm-I'm just so stupid. I'm such an id...

3. **THERAPIST**: Well, Ruth, it sounds like you're very frustrated first of all. And you're saying that you're just t...

4. **CLIENT**: Mm-hmm.

5. **THERAPIST**: You don't want to continue.

6. **CLIENT**: No, it just seems that cutting myself is the only way out. And I just get suicidal thoughts and [for...

7. **THERAPIST**: So you feel really, really like you've had it up to here.

8. **CLIENT**: Yeah.

9. **THERAPIST**: Yeah. You're-you're tired. You're stressed. You feel so sad to the point that you're hurting yoursel...

10. **CLIENT**: Yes. Sometimes a pain in-in the body. It's, uh, to [unintelligible 00:01:27] handle and-and the pain...

## 数据使用说明

### 简化版 vs 完整版

| 特性 | 完整版 (AnnoMI-high-resistance.json) | 简化版 (AnnoMI-simple-high-resistance.json) |
|------|--------------------------------------|---------------------------------------------|
| 对话内容 | ✅ | ✅ |
| client_talk_type标注 | ✅ | ❌ |
| 详细标注信息 | ✅ | ❌ |
| 文件大小 | 较大 (4.1MB) | 较小 (~1MB) |
| 适用场景 | 需要详细分析阻抗类型 | 只需要对话内容 |

### 使用示例

```python
import json

# 加载简化版数据
with open('AnnoMI-simple-high-resistance.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 遍历对话
for transcript_id, transcript in data['transcripts'].items():
    print(f"对话 {transcript_id}: {transcript['metadata']['topic']}")
    
    # 提取对话内容
    for utterance in transcript['dialogue']:
        speaker = utterance['interlocutor']
        text = utterance['utterance_text']
        print(f"{speaker}: {text}")
```

## 相关文件

### 完整版（带标注）
- `AnnoMI-full.json` - 原始完整数据集（133个对话）
- `AnnoMI-high-resistance.json` - 筛选后的高阻抗对话（32个）
- `resistance_statistics.json` - 详细统计信息
- `resistance_filtering_report.md` - 完整版筛选报告

### 简化版（无标注）
- `AnnoMI-simple.json` - 原始简化数据集（133个对话）
- `AnnoMI-simple-high-resistance.json` - 提取的高阻抗对话（32个）
- `resistance_statistics_simple.json` - 简化版统计信息
- `resistance_filtering_report_simple.md` - 本报告

### 脚本文件
- `filter_high_resistance.py` - 从完整版筛选脚本
- `extract_simple_resistance.py` - 从简化版提取脚本
