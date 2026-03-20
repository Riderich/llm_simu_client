#!/usr/bin/env python3
"""
筛选高阻抗对话脚本
从AnnoMI-full.json中提取表现出明显阻抗现象的对话

筛选标准（方案F）：
- MI质量：high
- 阻抗标准：sustain比例 ≥ 25% 或 sustain绝对次数 ≥ 8次
"""

import json
from typing import Dict, List, Any


def analyze_resistance(dialogue: List[Dict]) -> Dict[str, Any]:
    """分析对话中的阻抗情况"""
    sustain_count = 0
    change_count = 0
    neutral_count = 0
    total_client_utterances = 0
    
    sustain_utterances = []  # 记录所有sustain类型的发言
    
    for utterance in dialogue:
        if utterance['interlocutor'] == 'client':
            total_client_utterances += 1
            talk_type = utterance.get('client_talk_type', 'n/a')
            
            if talk_type == 'sustain':
                sustain_count += 1
                sustain_utterances.append({
                    'utterance_id': utterance['utterance_id'],
                    'text': utterance['utterance_text']
                })
            elif talk_type == 'change':
                change_count += 1
            elif talk_type == 'neutral':
                neutral_count += 1
    
    sustain_ratio = sustain_count / total_client_utterances if total_client_utterances > 0 else 0
    
    return {
        'sustain_count': sustain_count,
        'change_count': change_count,
        'neutral_count': neutral_count,
        'total_client_utterances': total_client_utterances,
        'sustain_ratio': sustain_ratio,
        'sustain_utterances': sustain_utterances
    }


def meets_criteria(stats: Dict[str, Any], mi_quality: str) -> bool:
    """判断是否满足筛选标准（方案F）"""
    if mi_quality != 'high':
        return False
    
    # 条件1: sustain比例 >= 25%
    # 条件2: sustain绝对次数 >= 8
    return stats['sustain_ratio'] >= 0.25 or stats['sustain_count'] >= 8


def filter_transcripts(input_file: str, output_file: str, stats_file: str):
    """筛选符合条件的对话并生成统计报告"""
    
    print(f"正在读取数据: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"原始数据包含 {len(data['transcripts'])} 个对话")
    print("\n开始筛选...")
    
    filtered_transcripts = {}
    statistics = []
    
    for transcript_id, transcript in data['transcripts'].items():
        mi_quality = transcript['metadata'].get('mi_quality', '')
        
        # 分析阻抗情况
        stats = analyze_resistance(transcript['dialogue'])
        
        # 判断是否满足条件
        if meets_criteria(stats, mi_quality):
            filtered_transcripts[transcript_id] = transcript
            
            # 记录统计信息
            statistics.append({
                'transcript_id': transcript_id,
                'mi_quality': mi_quality,
                'topic': transcript['metadata'].get('topic', 'N/A'),
                'video_title': transcript['metadata'].get('video_title', 'N/A'),
                'video_url': transcript['metadata'].get('video_url', 'N/A'),
                'sustain_count': stats['sustain_count'],
                'change_count': stats['change_count'],
                'neutral_count': stats['neutral_count'],
                'total_client_utterances': stats['total_client_utterances'],
                'sustain_ratio': stats['sustain_ratio'],
                'total_dialogue_turns': len(transcript['dialogue']),
                # 记录前3个sustain发言作为样例
                'sample_sustain_utterances': stats['sustain_utterances'][:3]
            })
    
    # 按sustain比例排序
    statistics.sort(key=lambda x: x['sustain_ratio'], reverse=True)
    
    # 保存筛选后的数据
    output_data = {
        'metadata': {
            'description': 'High-resistance client dialogues from AnnoMI dataset',
            'filtering_criteria': {
                'mi_quality': 'high',
                'resistance_criteria': 'sustain_ratio >= 0.25 OR sustain_count >= 8'
            },
            'original_transcript_count': len(data['transcripts']),
            'filtered_transcript_count': len(filtered_transcripts)
        },
        'transcripts': filtered_transcripts
    }
    
    print(f"\n保存筛选后的数据: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    # 保存统计信息
    stats_data = {
        'summary': {
            'total_filtered': len(filtered_transcripts),
            'average_sustain_ratio': sum(s['sustain_ratio'] for s in statistics) / len(statistics),
            'average_sustain_count': sum(s['sustain_count'] for s in statistics) / len(statistics),
            'min_sustain_ratio': min(s['sustain_ratio'] for s in statistics),
            'max_sustain_ratio': max(s['sustain_ratio'] for s in statistics),
        },
        'transcripts': statistics
    }
    
    print(f"保存统计报告: {stats_file}")
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats_data, f, ensure_ascii=False, indent=2)
    
    # 打印摘要
    print("\n" + "="*80)
    print("筛选完成！")
    print("="*80)
    print(f"筛选出的对话数量: {len(filtered_transcripts)}")
    print(f"平均sustain比例: {stats_data['summary']['average_sustain_ratio']:.1%}")
    print(f"平均sustain次数: {stats_data['summary']['average_sustain_count']:.1f}")
    print(f"sustain比例范围: {stats_data['summary']['min_sustain_ratio']:.1%} - {stats_data['summary']['max_sustain_ratio']:.1%}")
    
    # 主题分布
    print("\n主题分布:")
    topic_dist = {}
    for s in statistics:
        topic = s['topic'].strip()
        topic_dist[topic] = topic_dist.get(topic, 0) + 1
    
    for topic, count in sorted(topic_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  {topic}: {count}个")
    
    print("\n" + "="*80)
    print(f"输出文件:")
    print(f"  - 筛选后的数据集: {output_file}")
    print(f"  - 统计报告: {stats_file}")
    print("="*80)


if __name__ == '__main__':
    input_file = 'AnnoMI-full.json'
    output_file = 'AnnoMI-high-resistance.json'
    stats_file = 'resistance_statistics.json'
    
    filter_transcripts(input_file, output_file, stats_file)
