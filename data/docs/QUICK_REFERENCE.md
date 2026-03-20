# 🎯 高阻抗对话数据集 - 快速参考

## 📦 核心数据文件

### 1️⃣ 完整版（带标注）
```
AnnoMI-high-resistance.json         [4.1MB]
├─ 32个高阻抗对话
├─ 包含 client_talk_type 标注
└─ 适合：阻抗分析、模式识别
```

### 2️⃣ 简化版（仅对话）
```
AnnoMI-simple-high-resistance.json  [1.2MB]
├─ 32个高阻抗对话（同样的ID）
├─ 仅对话内容，无标注
└─ 适合：对话生成、LLM测试
```

## 📊 数据特征一览

| 指标 | 数值 |
|------|------|
| 对话数量 | 32个 |
| MI质量 | 100% high |
| 平均sustain比例 | 28.5% |
| 平均sustain次数 | 17.2次 |
| 阻抗比例范围 | 6.8% - 72.2% |
| 平均对话轮次 | 224.3轮 |
| 主题覆盖 | 12种健康行为 |

## 🎬 快速开始（3步）

### Step 1: 选择版本
```bash
# 如果需要标注信息
FILE="AnnoMI-high-resistance.json"

# 如果只需要对话内容
FILE="AnnoMI-simple-high-resistance.json"
```

### Step 2: 加载数据
```python
import json
with open(FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### Step 3: 使用数据
```python
# 遍历所有对话
for tid, transcript in data['transcripts'].items():
    topic = transcript['metadata']['topic']
    dialogue = transcript['dialogue']
    print(f"对话 {tid}: {topic}, 共{len(dialogue)}轮")
```

## 🔍 常见用法

### 用法1: 提取sustain发言（完整版）
```python
sustain_talks = []
for utterance in transcript['dialogue']:
    if (utterance['interlocutor'] == 'client' and 
        utterance['client_talk_type'] == 'sustain'):
        sustain_talks.append(utterance['utterance_text'])
```

### 用法2: 构建对话历史（简化版）
```python
dialogue_history = []
for utterance in transcript['dialogue']:
    speaker = utterance['interlocutor']
    text = utterance['utterance_text']
    dialogue_history.append(f"{speaker}: {text}")

conversation = "\n".join(dialogue_history)
```

### 用法3: 查看统计信息
```python
# 加载统计文件
with open('resistance_statistics.json', 'r') as f:
    stats = json.load(f)

# 查看某个对话的统计
for t in stats['transcripts']:
    if t['transcript_id'] == '95':  # 最高阻抗的对话
        print(f"Sustain: {t['sustain_count']}/{t['total_client_utterances']}")
        print(f"比例: {t['sustain_ratio']:.1%}")
        print(f"样例: {t['sample_sustain_utterances']}")
```

## 📁 完整文件列表

```
数据集文件 (2个)
├─ AnnoMI-high-resistance.json              完整版数据
└─ AnnoMI-simple-high-resistance.json       简化版数据

统计报告 (4个)
├─ resistance_statistics.json               完整版统计
├─ resistance_statistics_simple.json        简化版统计
├─ resistance_filtering_report.md           完整版报告
└─ resistance_filtering_report_simple.md    简化版报告

脚本工具 (2个)
├─ filter_high_resistance.py                筛选脚本
└─ extract_simple_resistance.py             提取脚本

说明文档 (2个)
├─ README_complete.md                       完整说明（推荐阅读）
└─ README_filtering.md                      筛选详情

快速参考 (1个)
└─ QUICK_REFERENCE.md                       本文档
```

## 🏆 Top 3 高阻抗对话

### 🥇 #1: Transcript 95 - 减少自残
- **阻抗比例**: 72.2%
- **特点**: 表达强烈的无助感和绝望
- **典型语句**: "I don't even know why I'm doing this anymore..."

### 🥈 #2: Transcript 30 - 充电电池  
- **阻抗比例**: 71.4%
- **特点**: 对改变表现出抗拒和辩护

### 🥉 #3: Transcript 24 - 戒烟
- **阻抗比例**: 63.6%
- **特点**: 否认问题严重性

## 💡 推荐阅读顺序

1. **首次使用**: 阅读本文档（QUICK_REFERENCE.md）
2. **深入了解**: 阅读 README_complete.md
3. **查看报告**: resistance_filtering_report.md
4. **开始使用**: 加载数据并运行上述代码示例

## ⚠️ 重要提示

1. **两个版本的对话ID完全一致** - 可以交叉引用
2. **简化版没有sustain标注** - 需要配合统计文件使用
3. **数据包含敏感内容** - 请遵守研究伦理规范

## 🔗 相关链接

- 完整说明: `README_complete.md`
- 筛选详情: `README_filtering.md`
- 完整版报告: `resistance_filtering_report.md`
- 简化版报告: `resistance_filtering_report_simple.md`

## 📮 版本信息

- **创建日期**: 2026-02-08
- **版本**: v1.0
- **数据来源**: AnnoMI数据集
- **筛选标准**: 方案F（high质量 + sustain≥25% 或 次数≥8）

---

**快速测试代码**:
```python
import json

# 快速查看数据
with open('AnnoMI-simple-high-resistance.json', 'r') as f:
    data = json.load(f)

print(f"✅ 成功加载 {len(data['transcripts'])} 个对话")
print(f"✅ 主题示例: {list(data['transcripts'].values())[0]['metadata']['topic']}")
```
