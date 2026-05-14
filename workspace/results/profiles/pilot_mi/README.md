# MI Profile 试点产出

> 基于 `workspace/results/profile_inputs/*.json` 整段对话，用 LLM 抽取 MI 对齐的最终 Profile，用于验证 Profile 设计效果。

## 文件说明

| 文件 | 内容 |
|------|------|
| `selection_v1.json` | 早期手工挑选的试点候选清单（RECAP 30 + 临床 28） |
| `selection_pilot.json` | 最近一次 pilot 运行实际选中的 RECAP 角色（含 seed、stats） |
| `{数据源}_profiles.json` | Pilot 跑出的 MI Profile（`meta` + `items`），数据源名来自输入 JSON 的文件 stem，如 `recap_profiles.json`、`annomi_profiles.json` |
| `{数据源}_selection.json` | 与上面对应的选样清单（seed、character_ids 等） |

## 运行

```bash
python3 data_scripts/extract_mi_profile_pilot.py --dry-run
python3 data_scripts/extract_mi_profile_pilot.py --max-dialogues 10 --seed 42
python3 data_scripts/extract_mi_profile_pilot.py --dialogues workspace/results/profile_inputs/annomi.json --max-dialogues 10
python3 data_scripts/extract_mi_profile_pilot.py --resume
```

输入默认 `workspace/results/profile_inputs/recap.json`；输出默认写入本目录，文件名为 `recap_profiles.json` / `recap_selection.json`（随 `--dialogues` 的 stem 变化）。可用 `--source-name my_run` 强制覆盖输出前缀。

## 环境变量

脚本启动时从仓库根 `.env` 加载（`override=False`，不覆盖 shell 已导出的变量）。需要配置：

- `DEEPSEEK_API_KEY`（默认模型 `deepseek-v4-flash`）或 `OPENAI_API_KEY`
- 可选 `DEEPSEEK_BASE_URL` / `OPENAI_BASE_URL`
- **DeepSeek 请求扩展**（`LLMClient` 与官方示例同构：`extra_body.thinking` + 可选 `reasoning_effort`）：
  - `DEEPSEEK_THINKING`：`enabled` / `disabled`，默认 `disabled`
  - `DEEPSEEK_REASONING_EFFORT`：如 `high`；留空则不传该字段

## 相关资源

- Schema：[`workspace/schemas/mi_profile.schema.json`](../../../schemas/mi_profile.schema.json)
- 系统提示：[`workspace/prompts/mi_profile_extract_zh_system.md`](../../../prompts/mi_profile_extract_zh_system.md)
- LLM 客户端：[`workspace/src/llm_client.py`](../../../src/llm_client.py)
