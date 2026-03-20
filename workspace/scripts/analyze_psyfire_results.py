"""
PsyFIRE 测试结果评估脚本
"""
import json
from collections import defaultdict

def load_results(filepath):
    """加载测试结果"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def evaluate_results(results):
    """评估测试结果"""
    total = len(results)
    
    # 统计各个阻抗类别的表现
    category_stats = defaultdict(lambda: {'total': 0, 'predictions': []})
    
    for case in results:
        category = case.get('resistance_category', 'unknown')
        parent = case.get('resistance_parent', 'unknown')
        prediction = case.get('prediction', '')
        ground_truth = case.get('ground_truth', '')
        
        category_key = f"{parent} - {category}"
        category_stats[category_key]['total'] += 1
        category_stats[category_key]['predictions'].append({
            'case_id': case.get('case_id'),
            'prediction': prediction,
            'ground_truth': ground_truth,
            'prediction_len': len(prediction),
            'ground_truth_len': len(ground_truth)
        })
    
    return {
        'total_cases': total,
        'category_stats': dict(category_stats)
    }

def analyze_quality(results):
    """分析生成质量"""
    quality_metrics = {
        'empty_predictions': 0,
        'very_short_predictions': 0,  # < 20 字符
        'reasonable_predictions': 0,  # 20-200 字符
        'long_predictions': 0,  # > 200 字符
        'avg_prediction_len': 0,
        'avg_ground_truth_len': 0
    }
    
    total_pred_len = 0
    total_gt_len = 0
    
    for case in results:
        pred = case.get('prediction', '')
        gt = case.get('ground_truth', '')
        pred_len = len(pred)
        
        total_pred_len += pred_len
        total_gt_len += len(gt)
        
        if pred_len == 0:
            quality_metrics['empty_predictions'] += 1
        elif pred_len < 20:
            quality_metrics['very_short_predictions'] += 1
        elif pred_len <= 200:
            quality_metrics['reasonable_predictions'] += 1
        else:
            quality_metrics['long_predictions'] += 1
    
    quality_metrics['avg_prediction_len'] = total_pred_len / len(results)
    quality_metrics['avg_ground_truth_len'] = total_gt_len / len(results)
    
    return quality_metrics

def print_detailed_analysis(results):
    """打印详细分析"""
    print("=" * 80)
    print("PsyFIRE 测试结果详细分析")
    print("=" * 80)
    
    eval_results = evaluate_results(results)
    quality = analyze_quality(results)
    
    print(f"\n总测试用例数: {eval_results['total_cases']}")
    print(f"\n质量指标:")
    print(f"  - 空预测: {quality['empty_predictions']}")
    print(f"  - 极短预测 (<20字符): {quality['very_short_predictions']}")
    print(f"  - 合理长度 (20-200字符): {quality['reasonable_predictions']}")
    print(f"  - 过长预测 (>200字符): {quality['long_predictions']}")
    print(f"  - 平均预测长度: {quality['avg_prediction_len']:.1f} 字符")
    print(f"  - 平均真实回应长度: {quality['avg_ground_truth_len']:.1f} 字符")
    
    print(f"\n按阻抗类别统计:")
    for category, stats in sorted(eval_results['category_stats'].items()):
        print(f"\n  {category} ({stats['total']} 个案例)")
        for pred_info in stats['predictions']:
            print(f"    案例 {pred_info['case_id']}:")
            print(f"      预测: {pred_info['prediction'][:80]}...")
            print(f"      真实: {pred_info['ground_truth'][:80]}...")
            print(f"      长度: 预测={pred_info['prediction_len']}, 真实={pred_info['ground_truth_len']}")

if __name__ == "__main__":
    results = load_results("../results/psyfire_results.json")
    print_detailed_analysis(results)
