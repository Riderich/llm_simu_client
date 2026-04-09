#!/usr/bin/env python3
"""
统一测试脚本 - 用于测试 deepseek-v3.2 模型的角色扮演能力

支持的测试类型：
1. ESConv 基础测试
2. 阻抗行为测试
3. PsyFIRE 框架测试
"""

import sys
import os
import argparse

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from context_inference import ContextInference


def run_esconv_test(args):
    """运行 ESConv 基础测试"""
    print("=" * 60)
    print("ESConv 基础测试")
    print("=" * 60)
    
    inference = ContextInference(model=args.model)
    
    results = inference.test_from_file(
        test_file=os.path.join("..", "test_cases", "test.json"),
        output_file=os.path.join("..", "results", "esconv_results.json"),
        temperature=args.temperature,
        with_ground_truth=args.with_ground_truth,
        use_simple_prompt=args.use_simple_prompt
    )
    
    print(f"\n测试完成！共 {len(results)} 个案例")
    return results


def run_resistance_test(args):
    """运行阻抗行为测试"""
    print("=" * 60)
    print("阻抗行为测试")
    print("=" * 60)
    print("\n测试说明：")
    print("- 从 ESConv 数据集中选取具有真实阻抗行为的对话")
    print("- System prompt 只提供基本信息，不提示'要表现出阻抗'")
    print("- 评估模型能否自然预测出阻抗回应\n")
    
    inference = ContextInference(model=args.model)
    
    results = inference.test_from_file(
        test_file=os.path.join("..", "test_cases", "test_true_resistance.json"),
        output_file=os.path.join("..", "results", "resistance_results.json"),
        temperature=args.temperature,
        with_ground_truth=True,
        use_simple_prompt=False
    )
    
    print(f"\n测试完成！共 {len(results)} 个案例")
    
    # 简单分析阻抗关键词
    resistance_keywords = ['disagree', 'no way', 'won\'t', 'can\'t', 'don\'t want',
                          'not ready', 'not going to', 'refuse', 'but']
    
    for r in results:
        if "error" in r:
            continue
        
        pred = r.get('prediction', '').lower()
        gt = r.get('ground_truth', '').lower()
        
        pred_has_resistance = any(kw in pred for kw in resistance_keywords)
        gt_has_resistance = any(kw in gt for kw in resistance_keywords)
        
        print(f"\nCase {r['case_id']}: {r['problem_type']} ({r['emotion_type']})")
        print(f"  预测包含阻抗关键词: {pred_has_resistance}")
        print(f"  真实包含阻抗关键词: {gt_has_resistance}")
    
    return results


def run_psyfire_test(args):
    """运行 PsyFIRE 框架测试"""
    print("=" * 60)
    print("PsyFIRE 框架测试")
    print("=" * 60)
    print("\n测试说明：")
    print("- 使用 AnnoMI-labeled.json 中标注的阻抗行为对话")
    print("- 测试模型能否预测出 13 种细粒度阻抗类别\n")
    
    inference = ContextInference(model=args.model)
    
    # 检查测试文件是否存在
    test_file = os.path.join("..", "test_cases", "psyfire_test.json")
    if not os.path.exists(test_file):
        print(f"错误：测试文件 {test_file} 不存在")
        print("请先运行 src/test_case_selector.py 生成 PsyFIRE 测试用例")
        return []
    
    results = inference.test_from_file(
        test_file=test_file,
        output_file=os.path.join("..", "results", "psyfire_results.json"),
        temperature=args.temperature,
        with_ground_truth=True,
        use_simple_prompt=False
    )
    
    print(f"\n测试完成！共 {len(results)} 个案例")
    return results


def main():
    parser = argparse.ArgumentParser(description="统一测试脚本")
    parser.add_argument(
        "test_type",
        choices=["esconv", "resistance", "psyfire", "all"],
        help="测试类型"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="deepseek-v3.2",
        help="使用的模型名称"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="温度参数"
    )
    parser.add_argument(
        "--with-ground-truth",
        action="store_true",
        help="是否包含真实回应（仅 ESConv 测试）"
    )
    parser.add_argument(
        "--use-simple-prompt",
        action="store_true",
        help="使用包含背景信息的简单 system prompt（仅 ESConv 测试）"
    )
    
    args = parser.parse_args()
    
    if args.test_type == "esconv":
        run_esconv_test(args)
    elif args.test_type == "resistance":
        run_resistance_test(args)
    elif args.test_type == "psyfire":
        run_psyfire_test(args)
    elif args.test_type == "all":
        print("运行所有测试...\n")
        run_esconv_test(args)
        print("\n" + "=" * 60 + "\n")
        run_resistance_test(args)
        print("\n" + "=" * 60 + "\n")
        run_psyfire_test(args)


if __name__ == "__main__":
    main()
