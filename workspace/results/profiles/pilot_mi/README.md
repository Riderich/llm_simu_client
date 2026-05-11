# MI Profile 试点产出

> 基于 RECAP 整段对话，用 LLM 抽取 MI 对齐的最终 Profile，用于验证 Profile 设计效果。

## 文件说明

| 文件 | 内容 |
|------|------|
| `selection_v1.json` | 早期手工挑选的试点候选清单（RECAP 30 + 临床 28） |
| `selection_pilot.json` | 最近一次 pilot 运行实际选中的 RECAP 角色（含 seed、stats） |
| `recap_profiles.json` | Pilot 跑出的 MI Profile 结果（`meta` + `items`） |

## 运行

```bash
python3 data_scripts/extract_mi_profile_pilot.py --dry-run
python3 data_scripts/extract_mi_profile_pilot.py --max-dialogues 10 --seed 42
python3 data_scripts/extract_mi_profile_pilot.py --resume
```

输入默认从 `workspace/results/recap/dialogues.json` 取样；输出默认写入本目录。

## 环境变量

脚本启动时从仓库根 `.env` 加载（`override=False`，不覆盖 shell 已导出的变量）。需要配置：

- `DEEPSEEK_API_KEY`（默认模型 `deepseek-v4-flash`）或 `OPENAI_API_KEY`
- 可选 `DEEPSEEK_BASE_URL` / `OPENAI_BASE_URL`

## 相关资源

- Schema：[`workspace/schemas/mi_profile.schema.json`](../../../schemas/mi_profile.schema.json)
- 系统提示：[`workspace/prompts/mi_profile_extract_zh_system.md`](../../../prompts/mi_profile_extract_zh_system.md)
- LLM 客户端：[`workspace/scripts/profile_pipeline/client.py`](../../../scripts/profile_pipeline/client.py)
