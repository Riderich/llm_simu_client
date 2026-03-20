# 高阻抗对话筛选项目说明

## 项目目标

从AnnoMI-full.json数据集中筛选出**表现明显阻抗现象的client对话**，用于测试模型在阻抗情境下的原生模拟病人能力。

## 筛选标准（方案F）

### 质量控制
- **MI质量**: 仅保留 `high` 质量的对话
- 确保治疗师使用标准的动机访谈技术

### 阻抗定义
满足以下**任一条件**即可：
1. **条件1**: sustain talk比例 ≥ 25%（阻抗比例明显）
2. **条件2**: sustain talk绝对次数 ≥ 8次（阻抗实例充足）

### 设计理念
- 灵活平衡：既包含高阻抗比例的短对话，也包含阻抗次数多的长对话
- 确保数据多样性和实际可用性

## 筛选结果

### 数据统计
- **原始对话数**: 133个
- **筛选后数量**: 32个（符合30-50个目标）
- **平均sustain比例**: 28.5%
- **平均sustain次数**: 17.2次
- **阻抗比例范围**: 6.8% - 72.2%

### 主题分布
覆盖12个不同的咨询主题，包括：
- 减少酒精摄入 (6个)
- 戒烟 (5个)
- 减少再犯 (5个)
- 服药依从性 (3个)
- 其他健康行为改变 (13个)

## 生成文件

### 1. `AnnoMI-high-resistance.json` (4.1MB)
筛选后的数据集，包含32个高阻抗对话。

**结构:**
```json
{
  "metadata": {
    "description": "...",
    "filtering_criteria": {...},
    "original_transcript_count": 133,
    "filtered_transcript_count": 32
  },
  "transcripts": {
    "0": {...},
    "1": {...},
    ...
  }
}
```

**用途**: 用于模型测试的主要数据集

### 2. `resistance_statistics.json` (36KB)
详细的统计信息，包含每个对话的阻抗分析。

**内容:**
- 汇总统计（平均值、范围等）
- 每个对话的详细指标
- Sustain发言样例（前3个）

**用途**: 数据分析、质量检查

### 3. `resistance_filtering_report.md` (3.6KB)
可读性强的Markdown格式报告。

**包含:**
- 筛选标准说明
- 统计摘要
- 主题分布表
- 详细对话列表
- 高阻抗样例展示

**用途**: 快速查看筛选结果、项目文档

### 4. `filter_high_resistance.py`
筛选脚本源代码。

**功能:**
- 读取原始数据集
- 应用筛选条件
- 生成上述三个输出文件
- 打印统计摘要

**可复现**: 可重新运行以验证或调整筛选参数

## 使用方法

### 查看筛选结果
```bash
# 查看统计报告（推荐）
cat resistance_filtering_report.md

# 查看JSON统计（程序化分析）
python3 -m json.tool resistance_statistics.json | less
```

### 重新筛选（如需调整标准）
```bash
# 编辑 filter_high_resistance.py 中的阈值
# 例如修改第52行: return stats['sustain_ratio'] >= 0.30 or stats['sustain_count'] >= 10

python3 filter_high_resistance.py
```

### 使用筛选后的数据
```python
import json

# 加载数据
with open('AnnoMI-high-resistance.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 访问对话
for transcript_id, transcript in data['transcripts'].items():
    print(f"对话 {transcript_id}: {transcript['metadata']['topic']}")
    
    # 提取sustain发言
    for utterance in transcript['dialogue']:
        if utterance['interlocutor'] == 'client' and \
           utterance['client_talk_type'] == 'sustain':
            print(f"  - {utterance['utterance_text']}")
```

## 数据质量保证

### 人工标注质量
- 所有对话均来自高质量MI视频（mi_quality='high'）
- 每个utterance都经过专业标注
- client_talk_type标注包括：sustain, change, neutral

### 筛选逻辑验证
- 使用灵活的组合标准避免偏差
- 平衡短对话和长对话的代表性
- 保持主题多样性

### 可追溯性
- 保留原始transcript ID
- 保留原始metadata（视频链接、标题等）
- 统计文件中包含样例发言

## 下一步工作建议

1. **数据探索**: 深入分析不同主题、不同阻抗比例的对话特点
2. **模型测试**: 使用这32个对话测试LLM的模拟病人能力
3. **评估指标**: 设计评估标准，比较模型生成的阻抗vs真实阻抗
4. **迭代优化**: 根据测试结果调整筛选标准或扩展数据集

## 相关文件

- `AnnoMI-full.json` - 原始完整数据集（133个对话）
- `filter_high_resistance.py` - 筛选脚本
- `AnnoMI-high-resistance.json` - 筛选后数据集（32个对话）
- `resistance_statistics.json` - 统计数据
- `resistance_filtering_report.md` - 可读报告

## 参考信息

### Sustain Talk定义
在动机访谈(MI)中，sustain talk指的是client表达维持现状、不愿改变的言语，通常表现为：
- 否认问题的严重性
- 强调改变的困难
- 表达对改变的抵触
- 为现状辩护

### 项目背景
- **研究目标**: 测试模型在阻抗情境下的原生模拟病人能力
- **数据来源**: AnnoMI数据集（动机访谈标注语料库）
- **筛选日期**: 2026-02-08
