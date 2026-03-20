#!/usr/bin/env python3
"""
从AnnoMI-simple.json中提取高阻抗对话
使用已经从AnnoMI-full.json筛选出的transcript IDs
"""

import json


def extract_simple_transcripts(
    simple_file: str,
    resistance_file: str,
    output_file: str,
    stats_file: str
):
    """从简化版数据中提取高阻抗对话"""
    
    print(f"正在读取简化版数据: {simple_file}")
    with open(simple_file, 'r', encoding='utf-8') as f:
        simple_data = json.load(f)
    
    print(f"正在读取高阻抗对话列表: {resistance_file}")
    with open(resistance_file, 'r', encoding='utf-8') as f:
        resistance_data = json.load(f)
    
    # 获取已筛选的transcript IDs
    selected_ids = list(resistance_data['transcripts'].keys())
    print(f"\n需要提取的对话ID数量: {len(selected_ids)}")
    
    # 从简化版中提取对应的对话
    extracted_transcripts = {}
    statistics = []
    
    for transcript_id in selected_ids:
        if transcript_id in simple_data['transcripts']:
            extracted_transcripts[transcript_id] = simple_data['transcripts'][transcript_id]
            
            # 从resistance_data获取统计信息
            metadata = simple_data['transcripts'][transcript_id]['metadata']
            
            # 计算对话轮次
            dialogue_turns = len(simple_data['transcripts'][transcript_id]['dialogue'])
            client_turns = sum(1 for u in simple_data['transcripts'][transcript_id]['dialogue'] 
                             if u['interlocutor'] == 'client')
            
            statistics.append({
                'transcript_id': transcript_id,
                'topic': metadata.get('topic', 'N/A'),
                'mi_quality': metadata.get('mi_quality', 'N/A'),
                'total_dialogue_turns': dialogue_turns,
                'client_turns': client_turns,
                'video_title': metadata.get('video_title', 'N/A')
            })
        else:
            print(f"警告: Transcript ID {transcript_id} 在简化版中未找到")
    
    # 按ID排序
    statistics.sort(key=lambda x: int(x['transcript_id']))
    
    # 保存提取后的数据
    output_data = {
        'metadata': {
            'description': 'High-resistance client dialogues (simplified version)',
            'source': 'Extracted from AnnoMI-simple.json based on AnnoMI-full.json filtering',
            'filtering_criteria': {
                'mi_quality': 'high',
                'resistance_criteria': 'sustain_ratio >= 0.25 OR sustain_count >= 8 (from full version)'
            },
            'note': 'This simplified version contains only dialogue content without detailed annotations',
            'original_transcript_count': len(simple_data['transcripts']),
            'extracted_transcript_count': len(extracted_transcripts)
        },
        'transcripts': extracted_transcripts
    }
    
    print(f"\n保存提取后的数据: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    # 保存统计信息
    stats_data = {
        'summary': {
            'total_extracted': len(extracted_transcripts),
            'source_full_version': resistance_file,
            'extraction_date': '2026-02-08'
        },
        'transcripts': statistics
    }
    
    print(f"保存统计信息: {stats_file}")
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats_data, f, ensure_ascii=False, indent=2)
    
    # 打印摘要
    print("\n" + "="*80)
    print("提取完成！")
    print("="*80)
    print(f"提取的对话数量: {len(extracted_transcripts)}")
    print(f"平均对话轮次: {sum(s['total_dialogue_turns'] for s in statistics) / len(statistics):.1f}")
    print(f"平均Client发言: {sum(s['client_turns'] for s in statistics) / len(statistics):.1f}")
    
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
    print(f"  - 简化版高阻抗数据集: {output_file}")
    print(f"  - 统计信息: {stats_file}")
    print("="*80)


if __name__ == '__main__':
    simple_file = 'AnnoMI-simple.json'
    resistance_file = 'AnnoMI-high-resistance.json'
    output_file = 'AnnoMI-simple-high-resistance.json'
    stats_file = 'resistance_statistics_simple.json'
    
    extract_simple_transcripts(simple_file, resistance_file, output_file, stats_file)
