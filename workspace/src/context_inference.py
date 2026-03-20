"""
大模型上下文推理脚本
用于测试模型扮演心理疾病患者的能力
"""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()


class ContextInference:
    def __init__(self, api_key=None, base_url=None, model="deepseek-v3.2"):
        """
        初始化大模型客户端

        Args:
            api_key: API密钥，默认从环境变量OPENAI_API_KEY读取
            base_url: API基础URL
            model: 使用的模型名称
        """
        # 模型选择：根据传入的 model 名字自动路由不同的 base_url / key
        self.model = model

        # 默认使用 DeepSeek 兼容接口
        default_key = os.getenv("OPENAI_API_KEY")
        default_base = os.getenv("OPENAI_BASE_URL", "https://api.apiplus.org/v1")

        # 如果是 Qwen 系列模型，则优先走 DashScope 兼容端点
        if self.model and self.model.lower().startswith("qwen"):
            qwen_key = os.getenv("QWEN_API_KEY")
            qwen_base = os.getenv(
                "QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            self.api_key = api_key or qwen_key or default_key
            self.base_url = base_url or qwen_base
        else:
            self.api_key = api_key or default_key
            self.base_url = base_url or default_base

        if not self.api_key:
            raise ValueError(
                "API密钥未设置，请设置环境变量 OPENAI_API_KEY / QWEN_API_KEY 或直接传入 api_key 参数"
            )

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def predict_next_response(
        self,
        context: list[dict],
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1500,
    ) -> str:
        """
        根据对话上下文预测下一句话

        Args:
            context: 对话上下文，格式为 [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
            system_prompt: 系统提示词，用于设定角色
            temperature: 温度参数，控制随机性（0-2）
            max_tokens: 生成的最大token数

        Returns:
            预测的下一句话
        """
        # 默认系统提示：扮演心理疾病患者
        if system_prompt is None:
            system_prompt = """你是一名心理咨询中的患者。请根据之前的对话历史，自然地作为患者回应咨询师的问题。
- 保持患者的语气和视角
- 反映患者的情绪状态和心理特点
- 回应要真实、自然，符合心理疾病患者的语言特征
- 不要表现出专业性的分析，而是表达真实的感受和想法"""

        # 构建完整的消息列表
        messages = [{"role": "system", "content": system_prompt}] + context

        # 调用API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content

    def batch_test(
        self,
        test_cases: list[dict],
        output_file: str = None,
        temperature: float = 0.7,
        with_ground_truth: bool = False,
        use_simple_prompt: bool = False,
    ) -> list[dict]:
        """
        批量测试多个对话场景

        Args:
            test_cases: 测试用例列表，每个用例包含 "context" 和可选的 "system_prompt"
            output_file: 结果输出文件路径（可选）
            temperature: 温度参数
            with_ground_truth: 是否包含真实回应（从原始数据中查找）
            use_simple_prompt: 是否使用包含背景信息的简单system prompt

        Returns:
            测试结果列表
        """
        results = []

        for idx, case in enumerate(test_cases):
            print(f"\n{'='*60}")
            print(f"测试用例 {idx + 1}/{len(test_cases)}")
            print(f"{'='*60}")
            print(f"来源: {case.get('source', 'unknown')}")
            print(f"问题类型: {case.get('problem_type', 'unknown')}")
            print(f"情绪类型: {case.get('emotion_type', 'unknown')}")

            context = case["context"]
            system_prompt = case.get("system_prompt")

            # 如果使用简单prompt，生成包含背景信息的system prompt
            if use_simple_prompt and system_prompt is None:
                system_prompt = self._generate_simple_prompt(case)
                print(f"\nSystem Prompt:")
                print(f"{'-'*60}")
                print(system_prompt)

            print(f"\n对话上下文:")
            for i, msg in enumerate(context):
                role = "咨询师" if msg["role"] == "user" else "患者"
                print(f"  [{i+1}] {role}: {msg['content']}")

            print(f"\n正在生成回应...")
            # 预测下一句话（加异常处理：单条失败时自动重试一次，再失败则跳过）
            prediction = ""
            for attempt in range(2):
                try:
                    prediction = self.predict_next_response(
                        context, system_prompt, temperature=temperature
                    )
                    break
                except Exception as e:
                    if attempt == 0:
                        print(f"\n[Warning] API error on attempt 1: {e}. Retrying in 5s...")
                        import time
                        time.sleep(5)
                    else:
                        print(f"\n[Error] API error on attempt 2: {e}. Skipping this case.")

            print(f"\n{'='*60}")
            print(f"预测的下一句话:")
            print(f"{'='*60}")
            print(prediction if prediction else "[SKIPPED - API error]")

            # 获取真实回应（如果提供）
            ground_truth = case.get("ground_truth")

            if with_ground_truth and ground_truth:
                print(f"\n{'='*60}")
                print(f"真实回应:")
                print(f"{'='*60}")
                print(ground_truth)

            results.append(
                {
                    "case_id": idx + 1,
                    "source": case.get("source", "unknown"),
                    "problem_type": case.get("problem_type", "unknown"),
                    "emotion_type": case.get("emotion_type", "unknown"),
                    "situation": case.get("situation", ""),
                    "context": context,
                    "system_prompt": system_prompt,
                    "prediction": prediction,
                    "ground_truth": ground_truth,
                }
            )

        # 输出到文件
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n{'='*60}")
            print(f"所有结果已保存到: {output_file}")
            print(f"{'='*60}")

        return results

    def test_from_file(
        self,
        test_file: str = "test.json",
        output_file: str = "results.json",
        temperature: float = 0.7,
        with_ground_truth: bool = False,
        use_simple_prompt: bool = False,
    ):
        """
        从JSON文件加载测试用例并批量测试

        Args:
            test_file: 测试用例文件路径
            output_file: 结果输出文件路径
            temperature: 温度参数
            with_ground_truth: 是否包含真实回应
            use_simple_prompt: 是否使用包含背景信息的简单system prompt
        """
        with open(test_file, "r", encoding="utf-8") as f:
            test_cases = json.load(f)

        # 如果需要真实回应，从原始数据中查找
        if with_ground_truth:
            # 加载原始数据
            import glob

            esconv_path = "dataset/ESConv.json"
            mesc_path = "dataset/MESC_merged.json"

            source_data = {}
            if os.path.exists(esconv_path):
                with open(esconv_path, "r", encoding="utf-8") as f:
                    source_data["ESConv"] = json.load(f)
            if os.path.exists(mesc_path):
                with open(mesc_path, "r", encoding="utf-8") as f:
                    source_data["MESC"] = json.load(f)

            # 为每个测试用例查找真实回应
            for case in test_cases:
                source = case.get("source", "unknown")
                if source not in source_data:
                    continue

                # 找到匹配的原始对话
                ground_truth = self._find_ground_truth(case, source_data[source])
                if ground_truth:
                    case["ground_truth"] = ground_truth

        print(f"从 {test_file} 加载了 {len(test_cases)} 个测试用例")
        if with_ground_truth:
            gt_count = sum(1 for c in test_cases if "ground_truth" in c)
            print(f"找到 {gt_count}/{len(test_cases)} 个真实回应")
        if use_simple_prompt:
            print("使用包含背景信息的简单system prompt进行测试")

        return self.batch_test(test_cases, output_file=output_file, temperature=temperature, with_ground_truth=with_ground_truth, use_simple_prompt=use_simple_prompt)

    def _extract_background_info(self, case: dict) -> dict:
        """
        从原始对话数据中提取隐性背景信息

        Args:
            case: 测试用例字典

        Returns:
            包含背景信息的字典
        """
        # 加载原始数据
        source = case.get("source", "unknown")
        esconv_path = "dataset/ESConv.json"
        mesc_path = "dataset/MESC_merged.json"

        source_data = None
        if os.path.exists(esconv_path):
            with open(esconv_path, "r", encoding="utf-8") as f:
                esconv_data = json.load(f)
                if source == "ESConv":
                    source_data = esconv_data
        if os.path.exists(mesc_path) and source == "MESC":
            with open(mesc_path, "r", encoding="utf-8") as f:
                source_data = json.load(f)

        if not source_data:
            return {}

        # 找到匹配的完整对话
        for data in source_data:
            if (data.get("problem_type") == case.get("problem_type") and
                data.get("emotion_type") == case.get("emotion_type")):

                # 获取完整对话文本
                full_dialog_text = ""
                if source == "ESConv":
                    for turn in data.get("dialog", []):
                        full_dialog_text += turn["content"] + " "

                # 提取背景信息（简单规则）
                background = {}

                # 家庭相关
                family_keywords = ["wife", "husband", "children", "kids", "son", "daughter", "father", "mother",
                                "parent", "family", "married", "single", "divorced", "separated"]
                for keyword in family_keywords:
                    if keyword.lower() in full_dialog_text.lower():
                        background["has_family_mention"] = True
                        break

                # 地理位置
                location_keywords = ["california", "washington", "new york", "texas", "florida", "chicago",
                                  "boston", "seattle", "los angeles", "new jersey"]
                for keyword in location_keywords:
                    if keyword.lower() in full_dialog_text.lower():
                        background["location"] = keyword
                        break

                # 工作相关
                job_keywords = ["job", "work", "career", "boss", "coworker", "employee", "manager",
                              "company", "office", "business", "corporate", "interview"]
                for keyword in job_keywords:
                    if keyword.lower() in full_dialog_text.lower():
                        background["has_job_mention"] = True
                        break

                # 教育相关
                education_keywords = ["school", "college", "university", "class", "student", "degree",
                                   "study", "learning", "semester", "course"]
                for keyword in education_keywords:
                    if keyword.lower() in full_dialog_text.lower():
                        background["has_education_mention"] = True
                        break

                # 关系状态
                if "girlfriend" in full_dialog_text.lower() or "boyfriend" in full_dialog_text.lower():
                    background["relationship_status"] = "in relationship"
                elif "partner" in full_dialog_text.lower():
                    background["relationship_status"] = "has partner"
                elif "broke up" in full_dialog_text.lower() or "break up" in full_dialog_text.lower():
                    background["relationship_status"] = "recent breakup"

                # 健康状况
                if "covid" in full_dialog_text.lower() or "coronavirus" in full_dialog_text.lower():
                    background["health_context"] = "COVID-19 related"

                # 年龄段（从用词推断）
                if "school" in full_dialog_text.lower() or "college" in full_dialog_text.lower():
                    background["age_group"] = "younger adult (likely student)"
                elif "years" in full_dialog_text.lower() and "work" in full_dialog_text.lower():
                    background["age_group"] = "working age adult"

                return background

        return {}

    def _generate_simple_prompt(self, case: dict) -> str:
        """
        为测试用例生成包含背景信息的简单system prompt

        Args:
            case: 测试用例字典，包含problem_type, emotion_type, situation

        Returns:
            系统提示词字符串
        """
        problem_type = case.get("problem_type", "unknown")
        emotion_type = case.get("emotion_type", "unknown")
        situation = case.get("situation", "")

        # 提取隐性背景信息
        background = self._extract_background_info(case)

        # 构建背景描述
        background_lines = []
        if background.get("location"):
            background_lines.append(f"居住在{background['location']}")
        if background.get("has_family_mention"):
            background_lines.append("有家庭")
        if background.get("relationship_status"):
            if background["relationship_status"] == "in relationship":
                background_lines.append("有恋爱关系")
            elif background["relationship_status"] == "has partner":
                background_lines.append("有伴侣")
            elif background["relationship_status"] == "recent breakup":
                background_lines.append("刚刚经历分手")
        if background.get("has_job_mention"):
            background_lines.append("有工作")
        if background.get("has_education_mention"):
            background_lines.append("涉及学习/教育")
        if background.get("health_context"):
            background_lines.append(f"健康背景: {background['health_context']}")
        if background.get("age_group"):
            background_lines.append(f"年龄段: {background['age_group']}")

        # 组合背景信息
        background_info = "、".join(background_lines) if background_lines else "普通背景"

        prompt = f"""你是一名心理咨询中的患者。

你的情况：
- 问题：{problem_type}
- 情绪：{emotion_type}
- 背景：{background_info}
- 详情：{situation}"""

        return prompt

    def _find_ground_truth(self, case: dict, source_data: list) -> str:
        """
        从原始数据中查找测试用例对应的真实回应

        Args:
            case: 测试用例，包含context
            source_data: 原始数据列表

        Returns:
            真实回应内容，如果未找到则返回None
        """
        context = case["context"]
        source = case.get("source", "unknown")

        # 通过匹配上下文找到原始对话
        for data in source_data:
            # 检查问题类型和情绪类型是否匹配
            if data.get("problem_type") != case.get("problem_type"):
                continue
            if data.get("emotion_type") != case.get("emotion_type"):
                continue

            # 获取对话列表
            if source == "ESConv":
                dialog = data.get("dialog", [])
                # ESConv格式: seeker -> assistant, supporter -> user
                # 转换为标准格式进行匹配
                converted = []
                for turn in dialog:
                    if turn["speaker"] == "seeker":
                        converted.append({"role": "assistant", "content": turn["content"].strip()})
                    else:
                        converted.append({"role": "user", "content": turn["content"].strip()})
            elif source == "MESC":
                dialog = data.get("dialog", [])
                # MESC格式: user -> user, assistant -> assistant
                converted = []
                for turn in dialog:
                    if turn["speaker"] == "user":
                        converted.append({"role": "user", "content": turn["text"].strip()})
                    else:
                        converted.append({"role": "assistant", "content": turn["text"].strip()})
            else:
                continue

            # 检查context是否匹配
            if len(converted) < len(context):
                continue

            # 比较最后几轮对话
            match = True
            for i in range(len(context)):
                if i >= len(converted):
                    match = False
                    break
                if converted[i]["role"] != context[i]["role"]:
                    match = False
                    break
                if converted[i]["content"] != context[i]["content"]:
                    match = False
                    break

            if match:
                # 找到匹配的对话，获取下一句（如果是seeker的话）
                if len(converted) > len(context):
                    next_turn = converted[len(context)]
                    if next_turn["role"] == "assistant":  # 确保下一句是患者的话
                        return next_turn["content"]

        return None


# 示例使用
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="大模型上下文推理测试")
    parser.add_argument("--with-ground-truth", action="store_true", help="是否包含真实回应")
    parser.add_argument("--use-simple-prompt", action="store_true", help="使用包含背景信息的简单system prompt")
    parser.add_argument("--test-file", type=str, default="test.json", help="测试用例文件路径")
    parser.add_argument("--output-file", type=str, default="results.json", help="结果输出文件路径")
    args = parser.parse_args()

    # 创建推理器实例 - 使用deepseek-v3.2
    inference = ContextInference(model="deepseek-v3.2")

    # 从test.json加载测试用例并批量测试
    print(f"从 {args.test_file} 加载测试用例并运行模型推理...")

    # 根据参数选择输出文件
    output_file = args.output_file

    inference.test_from_file(
        test_file=args.test_file, output_file=output_file, temperature=0.7,
        with_ground_truth=args.with_ground_truth, use_simple_prompt=args.use_simple_prompt
    )
