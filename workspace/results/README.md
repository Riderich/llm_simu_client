# workspace/results 目录说明

> 心理咨询模拟患者项目 - 数据结果目录

---

## 目录结构

```
results/
├── README.md                          # 本文件
│
├── 🎯 核心产出文件（直接使用）
│   ├── esconv_resistance_fine_full.json    # ESConv 阻抗细粒度标注 (5,609条)
│   ├── mesc_resistance_fine.json           # MESC 阻抗细粒度标注 (1,608条)
│   ├── esconv_coop_cbs_full.json           # ESConv 合作 CBS 分类 (13,763条)
│   ├── mesc_coop_cbs.json                  # MESC 合作 CBS 分类 (16,828条)
│   └── recap_coop_cbs.json                 # RECAP 合作 CBS 映射 (1,000条)
│
├── 💭 im_related/                         # Inner Monologue 相关文件
│   ├── inner_monologue_dataset.json        # AnnoMI 的 IM 数据集 (153条)
│   ├── cooperation_im_test.json            # 合作样本 IM 测试
│   ├── recap_im_test.json                  # RECAP IM 测试
│   ├── verify_inner_monologue.json         # IM 验证结果
│   └── inner_monologue_run_log.txt         # IM 生成运行日志
│
├── 🔧 archive/                            # 中间过程文件
│   └── ...                                 # 粗分类、utterance级别等中间结果
│
├── 🧪 test_archive/                       # 测试验证文件
│   └── ...                                 # VLLM测试、模型验证等
│
└── 📊 reports_archive/                    # 历史分析报告
    └── ...                                 # 早期测试分析报告
```

---

## 核心产出文件

### 阻抗细粒度标注 (PsyFIRE 13类)

| 文件 | 样本数 | 来源 | 分类体系 | 准确率 |
|------|--------|------|----------|--------|
| `esconv_resistance.json` | 5,609 | ESConv 模拟危机咨询 | PsyFIRE 13类 | 100% |
| `mesc_resistance.json` | 1,608 | MESC 真实电影咨询 | PsyFIRE 13类 | 100% |

### 合作样本分类 (CBS 2-8)

| 文件 | 样本数 | 来源 | 分类体系 | 说明 |
|------|--------|------|----------|------|
| `esconv_coop.json` | 13,763 | ESConv | CBS 2-8 类 | API分类 |
| `mesc_coop.json` | 16,828 | MESC | CBS 2-8 类 | API分类 |
| `recap_coop.json` | 1,000 | RECAP | CBS 2-8 类 | deepseek-v3.2 |

---

## 数据结构

### 阻抗标注文件

```json
{
  "fine_category": "A1",        // 细分类别代码
  "category": "争辩",            // 父类别
  "subcategory": "挑战",         // 子类别
  "text": "...",                 // 原始文本
  "conversation_id": "...",      // 对话ID
  "utterance_idx": 5            // 轮次索引
}
```

### 合作分类文件

```json
{
  "cbs_type": "CBS4-叙述",       // CBS 类型
  "text": "...",                 // 原始文本
  "dialogue_id": "..."          // 对话ID
}
```

---

## 使用建议

1. **模型训练**：直接使用核心产出文件
2. **数据分析**：参考 `notes/数据集细粒度分布统计.md`
3. **问题排查**：如需查看中间过程，检查 `archive/` 目录
4. **IM生成**：相关文件在 `im_related/` 目录

---

## 更新记录

| 日期 | 更新内容 |
|------|---------|
| 2026-04-01 | JSON文件名统一简化，RECAP改用deepseek-v3.2分类 |
| 2026-03-31 | 目录清理，添加 RECAP CBS 映射分类，整理核心产出 |
| 2026-03-26 | 完成 ESConv/MESC 细粒度标注 |
| 2026-03-19 | 完成 RECAP 数据处理 |
