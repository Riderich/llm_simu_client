"""
小批量测试脚本：测试5个阻抗 + 5个非阻抗样本
验证修复后的中文模板效果
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from context_inference import ContextInference
from generate_recap_inner_monologue import generate_one, select_template, save_checkpoint

# 测试样本索引
RESISTANCE_INDICES = [0, 1, 2, 3, 4]  # 5个阻抗样本
NON_RESISTANCE_INDICES = [18, 19, 27, 38, 42]  # 5个非阻抗样本

def main():
    # 加载数据
    with open('dataset/RECAP.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 合并测试索引
    test_indices = RESISTANCE_INDICES + NON_RESISTANCE_INDICES
    
    # 初始化模型
    model = "deepseek-v3.2"
    client = ContextInference(model=model)
    
    results = []
    
    print("=" * 80)
    print("小批量测试：5个阻抗 + 5个非阻抗样本")
    print(f"模型: {model}")
    print("=" * 80)
    
    for idx in test_indices:
        item = data[idx]
        
        # 获取标签信息
        rl = item.get('resistance_label', {})
        has_resistance = rl.get('has_resistance', False)
        parent = rl.get('parent', '')
        category = rl.get('category', '')
        subtype = rl.get('cooperative_subtype', '')
        
        print(f"\n[{idx}] {'🟥 阻抗' if has_resistance else '🟩 非阻抗'} | {parent}/{category}/{subtype or 'N/A'}")
        print(f"目标发言: {item.get('target_utterance', '')[:50]}...")
        
        # 生成 inner monologue
        _, inner = generate_one(idx, item, client, model, max_retries=3)
        
        print(f"内心独白: {inner[:100]}...")
        
        # 检查结果
        has_brackets = '[' in inner and ']' in inner
        is_error = inner.startswith('ERROR:')
        is_skipped = inner == '[SKIPPED - too short]'
        
        status = "✅"
        if is_error:
            status = "❌ ERROR"
        elif is_skipped:
            status = "⏭️ SKIPPED"
        elif has_brackets:
            status = "⚠️ 有方括号"
        
        print(f"状态: {status}")
        
        # 保存结果
        result = {
            "_recap_idx": idx,
            "target_utterance": item.get('target_utterance', ''),
            "resistance_label": rl,
            "inner_monologue": inner,
            "has_brackets": has_brackets,
            "is_error": is_error,
            "is_skipped": is_skipped
        }
        results.append(result)
    
    # 保存结果
    output_path = 'results/small_batch_test.json'
    save_checkpoint(results, output_path)
    
    # 打印统计
    print("\n" + "=" * 80)
    print("测试结果统计")
    print("=" * 80)
    
    resistance_results = [r for r in results if r['resistance_label'].get('has_resistance', False)]
    non_resistance_results = [r for r in results if not r['resistance_label'].get('has_resistance', False)]
    
    print(f"\n阻抗样本 (n={len(resistance_results)}):")
    for r in resistance_results:
        status = "✅" if not r['is_error'] and not r['has_brackets'] else "❌"
        print(f"  [{r['_recap_idx']}] {status} {r['inner_monologue'][:40]}...")
    
    print(f"\n非阻抗样本 (n={len(non_resistance_results)}):")
    for r in non_resistance_results:
        status = "✅" if not r['is_error'] and not r['has_brackets'] else "❌"
        print(f"  [{r['_recap_idx']}] {status} {r['inner_monologue'][:40]}...")
    
    print(f"\n结果已保存到: {output_path}")

if __name__ == "__main__":
    main()
