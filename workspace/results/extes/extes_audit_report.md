# ExtES 自动审计报告

数据源：`binary.json`（来访轮次 + 上下文字符串）、`resist_fine.json`（阻抗细粒度子集）。

## 1. 规模与主键

| 指标 | 数值 |
|------|------|
| binary 行数 | 85601 |
| binary 唯一 sample_id | 85601 |
| binary 重复 sample_id 行数（后者覆盖计数） | 0 |
| resist_fine 行数 | 10091 |

## 2. binary_label 分布

| label | count |
|-------|-------|
| 合作 | 75510 |
| 阻抗 | 10091 |

## 3. metadata.scene（Top 25）

| scene | count |
|-------|-------|
| Communication Challenges | 31075 |
| Conflicts or Communication Problems | 21834 |
| Breakups or Divorce | 6124 |
| Dealing with the Loss of a Pet | 5915 |
| Coping with the illness or death of a loved one | 4938 |
| Academic Stress | 2180 |
| Depression and Low Mood | 2106 |
| Work-related Stress and Burnout | 2051 |
| Unemployment-related stress | 1859 |
| Financial Worries and Uncertainty | 874 |
| Managing Bipolar Disorder | 811 |
| Anxiety and Panic | 579 |
| Adjusting to a New Job or Role | 532 |
| Moving to a New City or Country | 431 |
| Financial Worries and UncertAInty | 407 |
| Parenthood and Parenting Challenges | 240 |
| Career Transitions | 227 |
| Academic Stress or Pressure | 219 |
| Low Self-Esteem or Lack of Confidence | 207 |
| Job Loss or Career Setbacks | 202 |
| Caregiver Support | 189 |
| Cultural Identity and Belonging | 187 |
| Healing from Abuse or Domestic Violence | 186 |
| Finding Meaning and Purpose in Life | 176 |
| Addiction and Recovery | 174 |

- scene 种类数：**64**
- dialog_index（从 sample_id `extes_<d>_<t>` 解析）范围：**0 ~ 11177**
- sample_id 不符合 `extes_<digits>_<digits>`：**0**

## 4. 文本长度（字符）

| 字段 | p50 | p90 | p99 |
|------|-----|-----|-----|
| response | 130 | 201 | 270 |
| context | 988 | 1491 | 1892 |

- 空 response：**0**
- 极短 response（1–9 字符）：**79**

## 5. 规范化 response 重复（粗略）

将 response `strip` + `lower` + 空白折叠后取前 500 字符作为键。

- 重复键组数：**1925**
- 因重复多出来的行数：**5234**（约占 binary 行 6.11%）

## 6. 语言粗测（来访句）

- `response` 中英文字符占比阈值启发式判为「偏英文」：**85600** / 85601（100.00%）

## 7. resist_fine ↔ binary 对齐

- fine 中 sample_id 在 binary 命中：**10091**
- fine 中 sample_id 在 binary 缺失：**0**

### fine_category Top 15

| category | count |
|----------|-------|
| A2 | 6065 |
| B5 | 1298 |
| C2 | 564 |
| D1 | 469 |
| C1 | 431 |
| B1 | 338 |
| B6 | 267 |
| A1 | 256 |
| B4 | 131 |
| B3 | 97 |
| B7 | 96 |
| B2 | 71 |
| D2 | 8 |

### fine_label Top 15

| fine_label | count |
|------------|-------|
| 争辩-贬低 | 6065 |
| 否认-悲观 | 1285 |
| 回避-界限设定 | 564 |
| 忽视-不关注 | 469 |
| 回避-最小的回应 | 431 |
| 否认-责怪 | 337 |
| 否认-犹豫 | 266 |
| 争辩-挑战 | 245 |
| 否认-最小化 | 130 |
| 否认-找借口 | 96 |
| 否认-不愿改变 | 86 |
| 否认-不认同 | 71 |
| A1 | 11 |
| 否认-悲观(B5) | 9 |
| 忽视-岔开话题 | 8 |

---
*脚本：`extes_pipeline/audit_review_packet.py`*
