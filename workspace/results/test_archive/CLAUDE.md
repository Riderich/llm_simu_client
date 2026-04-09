# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project for evaluating LLM capabilities in psychological counseling scenarios, specifically testing how well models can simulate patient resistance behaviors. The codebase uses Python to run LLM inference tests against datasets of real counseling conversations.

## Running Tests

```bash
# Install dependencies
pip install openai python-dotenv

# Run basic resistance tests
python run_resistance_test.py

# Run real resistance case tests (with ground truth comparison)
python run_test_true_resistance.py

# Process dataset and select test cases
python select_test_cases.py

# Run inference tests with options
python context_inference.py --test-file test.json --output-file results.json --with-ground-truth --use-simple-prompt
```

## Architecture

### Core Components

**ContextInference Class** (`context_inference.py`)
- Main abstraction for LLM API interactions
- Uses OpenAI-compatible API (can be configured via `OPENAI_BASE_URL`)
- Default model: `deepseek-v3` (configurable)
- Key methods:
  - `predict_next_response()`: Generate next patient response given conversation context
  - `batch_test()`: Run inference on multiple test cases
  - `test_from_file()`: Load test cases from JSON and run batch tests

### Data Flow

1. **Test Case Format** (JSON):
   ```json
   {
     "source": "ESConv" | "MESC",
     "problem_type": "relationship issues",
     "emotion_type": "anxiety",
     "situation": "description of patient situation",
     "context": [
       {"role": "user", "content": "counselor message"},
       {"role": "assistant", "content": "patient message"}
     ],
     "system_prompt": "optional custom patient role prompt",
     "ground_truth": "optional actual patient response"
   }
   ```

2. **Conversation Context**:
   - Role mapping: `user` = counselor, `assistant` = patient
   - System prompt sets the patient role for inference

3. **Dataset Sources**:
   - `dataset/ESConv.json`: Emotional support conversations (~9MB)
   - `dataset/MESC_merged.json`: Merged dataset (~13MB)
   - Test files: `test.json`, `test_resistance.json`, `test_true_resistance.json`

### System Prompt Strategy

The project uses two approaches for system prompts:

1. **Default Prompt** (context_inference.py:58-63): Generic patient role instruction
2. **Enhanced Prompt** (`use_simple_prompt=True`): Includes extracted background information:
   - Problem type, emotion type, situation
   - Implicit background extracted from full dialog text (family, location, job, education, relationship status, health context, age group)

### Ground Truth Matching

The `_find_ground_truth()` method matches test case context to original dataset conversations:
- Matches by `problem_type` and `emotion_type`
- Compares conversation history exactly
- Returns the next patient response from the original dialog
- Handles different dataset formats (ESConv uses "seeker"/"supporter", MESC uses "user"/"assistant")

## Configuration

Required environment variables in `.env`:
```
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.apiplus.org/v1  # optional, default provided
```

## Claude Code Permissions

The `.claude/settings.local.json` allows executing Python commands:
```json
{
  "permissions": {
    "allow": ["Bash(python:*)"]
  }
}
```

## Resistance Types Studied

The project evaluates these specific patient resistance behaviors:
- Direct contradiction (反驳)
- Suggestion refusal (拒绝建议)
- Stubbornness (固执己见)
- Fear of change (恐惧改变)
- Self-limitation (自我设限)
- Resistance to change (不愿改变)
- Marriage refusal (固执不离婚)
- Self-negation (自我否定)
- Avoidance (回避讨论)
- Attribution of partner's unwillingness (坚持认为对方不愿沟通)
