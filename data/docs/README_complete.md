# 高阻抗对话数据集 - 完整说明文档

## 项目概述

本项目从AnnoMI数据集中筛选出**表现明显阻抗现象**的client对话，用于测试LLM模型在阻抗情境下的原生模拟病人能力。

我们提供了**两个版本**的筛选数据集：
1. **完整版** - 包含详细的行为标注（client_talk_type等）
2. **简化版** - 仅包含对话内容，无标注信息

## 数据集文件结构

```
项目文件/
├── 原始数据集
│   ├── AnnoMI-full.json              (133个对话，带详细标注)
│   └── AnnoMI-simple.json            (133个对话，仅对话内容)
│
├── 筛选后数据集 ⭐
│   ├── AnnoMI-high-resistance.json          (32个高阻抗对话，带标注)
│   └── AnnoMI-simple-high-resistance.json   (32个高阻抗对话，无标注)
│
├── 统计与报告
│   ├── resistance_statistics.json           (完整版详细统计)
│   ├── resistance_statistics_simple.json    (简化版统计)
│   ├── resistance_filtering_report.md       (完整版筛选报告)
│   └── resistance_filtering_report_simple.md (简化版提取报告)
│
├── 脚本工具
│   ├── filter_high_resistance.py            (从完整版筛选)
│   └── extract_simple_resistance.py         (从简化版提取)
│
└── 说明文档
    ├── README_filtering.md                  (完整版详细说明)
    └── README_complete.md                   (本文档 - 总览)
```

## 筛选标准

### 方案F：高质量 + 灵活阻抗标准

**质量要求：**
- MI质量 = `high`（确保治疗师使用标准动机访谈技术）

**阻抗标准（满足任一即可）：**
- 条件1: sustain talk比例 ≥ 25%
- 条件2: sustain talk绝对次数 ≥ 8次

### 设计理念
- **灵活性**：既包含高阻抗比例的短对话，也包含阻抗次数多的长对话
- **代表性**：覆盖多种健康行为改变主题
- **可用性**：数量适中（32个），便于深度分析

## 筛选结果统计

### 整体数据
- **原始对话数**: 133个
- **筛选后数量**: 32个
- **筛选成功率**: 24.1%

### 阻抗特征
- **平均sustain比例**: 28.5%
- **平均sustain次数**: 17.2次
- **阻抗比例范围**: 6.8% - 72.2%

### 对话特征
- **平均对话轮次**: 224.3轮
- **平均Client发言**: 111.6次
- **最长对话**: 1750轮（ID=56, 运动增加主题）
- **最短对话**: 14轮（ID=13, 服药依从性）

### 主题分布（12个主题）
| 主题 | 数量 | 百分比 |
|------|------|--------|
| 减少酒精摄入 | 6个 | 18.8% |
| 减少再犯风险 | 5个 | 15.6% |
| 戒烟 | 5个 | 15.6% |
| 服药依从性 | 3个 | 9.4% |
| 减少药物使用 | 2个 | 6.3% |
| 糖尿病管理 | 2个 | 6.3% |
| 减少自残 | 2个 | 6.3% |
| 其他主题 | 7个 | 21.9% |

## 两个版本对比

### 完整版 (AnnoMI-high-resistance.json)

**特点：**
- ✅ 包含完整的对话内容
- ✅ 包含详细的行为标注（client_talk_type: sustain/change/neutral）
- ✅ 包含治疗师行为标注
- ✅ 包含时间戳、utterance_id等元数据

**文件大小：** 4.1MB

**适用场景：**
- 需要分析阻抗类型和分布
- 需要研究治疗师-来访者互动模式
- 需要训练识别sustain talk的模型
- 需要详细的行为分析

**数据示例：**
```json
{
  "utterance_id": 1,
  "interlocutor": "client",
  "timestamp": "00:00:24",
  "utterance_text": "Sure.",
  "client_talk_type": "neutral",
  "main_therapist_behaviour": "n/a"
}
```

### 简化版 (AnnoMI-simple-high-resistance.json)

**特点：**
- ✅ 包含完整的对话内容
- ❌ 无行为标注
- ❌ 无时间戳等详细元数据
- ✅ 保留基础metadata（主题、视频链接等）

**文件大小：** 1.2MB

**适用场景：**
- 只需要对话内容进行测试
- 训练对话生成模型
- 减少数据加载时间
- 简化数据预处理流程

**数据示例：**
```json
{
  "interlocutor": "client",
  "utterance_text": "Sure."
}
```

## 快速开始

### 1. 查看筛选报告

```bash
# 查看完整版报告
cat resistance_filtering_report.md

# 查看简化版报告
cat resistance_filtering_report_simple.md
```

### 2. 加载数据（Python）

**完整版：**
```python
import json

# 加载完整版数据
with open('AnnoMI-high-resistance.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 访问对话
for transcript_id, transcript in data['transcripts'].items():
    print(f"对话 {transcript_id}: {transcript['metadata']['topic']}")
    
    # 提取sustain类型的发言
    for utterance in transcript['dialogue']:
        if utterance['interlocutor'] == 'client' and \
           utterance['client_talk_type'] == 'sustain':
            print(f"  阻抗: {utterance['utterance_text']}")
```

**简化版：**
```python
import json

# 加载简化版数据
with open('AnnoMI-simple-high-resistance.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 访问对话
for transcript_id, transcript in data['transcripts'].items():
    print(f"对话 {transcript_id}: {transcript['metadata']['topic']}")
    
    # 提取所有对话内容
    dialogue_text = []
    for utterance in transcript['dialogue']:
        speaker = utterance['interlocutor']
        text = utterance['utterance_text']
        dialogue_text.append(f"{speaker}: {text}")
    
    print("\n".join(dialogue_text))
```

### 3. 统计分析

```python
import json

# 加载统计数据
with open('resistance_statistics.json', 'r', encoding='utf-8') as f:
    stats = json.load(f)

# 查看汇总统计
summary = stats['summary']
print(f"总数: {summary['total_filtered']}")
print(f"平均sustain比例: {summary['average_sustain_ratio']:.1%}")
print(f"平均sustain次数: {summary['average_sustain_count']:.1f}")

# 遍历每个对话的统计
for t in stats['transcripts']:
    print(f"ID {t['transcript_id']}: {t['topic']}")
    print(f"  Sustain: {t['sustain_count']}/{t['total_client_utterances']} ({t['sustain_ratio']:.1%})")
    print(f"  样例: {t['sample_sustain_utterances'][0]['text'][:50]}...")
```

## 高阻抗样例

### 样例1: Transcript 95 - 减少自残（72.2% sustain）

**阻抗特征：**
- 最高阻抗比例（72.2%）
- 13次sustain发言 / 18次总发言
- 表现出强烈的无助感和绝望

**典型sustain发言：**
> "Um, okay. Just, I don't even know why I'm doing this anymore. I'm-I'm just so stupid. I'm such an idiot. I didn't know what the point of-of this is."

> "No, it just seems that cutting myself is the only way out. And I just get suicidal thoughts..."

### 样例2: Transcript 30 - 充电电池（71.4% sustain）

**阻抗特征：**
- 次高阻抗比例（71.4%）
- 10次sustain发言 / 14次总发言
- 对改变表现出抗拒和辩护

### 样例3: Transcript 56 - 增加运动（12.8% sustain, 但111次）

**阻抗特征：**
- 阻抗比例较低，但绝对次数最多（111次）
- 对话轮次最长（1750轮）
- 长期、反复的阻抗表现

## 数据质量保证

### 标注质量
- ✅ 所有对话来自专业标注的AnnoMI数据集
- ✅ MI质量均为`high`，确保治疗师技术标准
- ✅ 每个utterance都经过专业人员标注
- ✅ client_talk_type包括：sustain, change, neutral三类

### 筛选逻辑
- ✅ 使用灵活的组合标准避免单一维度偏差
- ✅ 平衡短对话和长对话的代表性
- ✅ 保持主题多样性（12个不同主题）
- ✅ 完整保留原始数据和元数据

### 可追溯性
- ✅ 保留原始transcript ID
- ✅ 保留原始metadata（视频链接、标题等）
- ✅ 提供完整的统计文件和筛选脚本
- ✅ 可复现的筛选流程

## 使用场景建议

### 场景1: 测试LLM模拟病人能力
**推荐：** 简化版
**理由：** 只需要对话内容，无需标注信息

```python
# 将对话作为prompt测试LLM
prompt = f"""
你是一个来访者，正在接受动机访谈。
以下是对话历史：
{dialogue_history}

请继续扮演这个来访者回应。
"""
```

### 场景2: 分析阻抗模式
**推荐：** 完整版
**理由：** 需要sustain标注来识别阻抗

```python
# 统计不同阻抗模式
sustain_patterns = []
for utterance in dialogue:
    if utterance['client_talk_type'] == 'sustain':
        sustain_patterns.append(utterance['utterance_text'])
```

### 场景3: 训练阻抗识别模型
**推荐：** 完整版
**理由：** 需要标注作为训练标签

```python
# 构建训练数据
X = [u['utterance_text'] for u in dialogue if u['interlocutor'] == 'client']
y = [u['client_talk_type'] for u in dialogue if u['interlocutor'] == 'client']
```

### 场景4: 快速原型开发
**推荐：** 简化版
**理由：** 文件更小，加载更快

## 重要注意事项

### 1. 阻抗的定义
在动机访谈中，**sustain talk**指的是：
- 否认问题的严重性
- 强调改变的困难
- 表达对改变的抵触
- 为现状辩护
- 表现出无助或绝望

### 2. 简化版的局限
简化版**不包含**client_talk_type标注，因此：
- 无法直接识别哪些发言是sustain
- 需要依赖完整版的统计信息了解阻抗分布
- 适合用于生成任务，不适合用于分类任务

### 3. 数据使用伦理
- ⚠️ 本数据集包含真实的心理健康对话内容
- ⚠️ 请确保数据使用符合研究伦理规范
- ⚠️ 不要泄露个人隐私信息

## 重新筛选（调整标准）

如果需要调整筛选标准，可以修改脚本并重新运行：

```bash
# 1. 编辑筛选脚本
nano filter_high_resistance.py

# 修改第52行的阈值，例如：
# return stats['sustain_ratio'] >= 0.30 or stats['sustain_count'] >= 10

# 2. 重新运行筛选
python3 filter_high_resistance.py

# 3. 重新提取简化版
python3 extract_simple_resistance.py
```

## 相关资源

### 论文与文档
- AnnoMI论文：[链接待补充]
- 动机访谈理论：Miller & Rollnick (2012)

### 代码仓库
- 本项目脚本：见当前目录
- AnnoMI原始数据：[链接待补充]

## 更新日志

**2026-02-08 - v1.0**
- ✅ 完成从AnnoMI-full.json的筛选（32个对话）
- ✅ 完成从AnnoMI-simple.json的提取（32个对话）
- ✅ 生成完整的统计报告和说明文档
- ✅ 提供可复现的筛选脚本

## 下一步工作建议

1. **数据探索**
   - 深入分析不同主题的阻抗特点
   - 比较高阻抗和低阻抗对话的差异
   - 研究治疗师应对阻抗的策略

2. **模型测试**
   - 使用简化版测试LLM的模拟病人能力
   - 评估模型生成的阻抗vs真实阻抗
   - 比较不同模型的表现

3. **评估指标开发**
   - 设计阻抗相似度评估标准
   - 开发自动化评估工具
   - 建立基准测试集

4. **数据扩展**
   - 考虑是否需要更多样本
   - 是否需要包含中等阻抗的对话
   - 是否需要特定主题的专门数据集

## 联系与反馈

如有问题或建议，请联系项目维护者。

---

**最后更新**: 2026-02-08  
**版本**: 1.0  
**数据集大小**: 完整版 4.1MB, 简化版 1.2MB  
**对话数量**: 32个高阻抗对话
