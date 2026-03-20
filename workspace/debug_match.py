import json

with open('dataset/AnnoMI-labeled.json', encoding='utf-8') as f:
    data = json.load(f)

matched = 0
total_res = 0
unmatched_cases = []

for tid, td in data['transcripts'].items():
    label = td.get('psyfire_label', {})
    if label.get('has_resistance'):
        total_res += 1
        ev = label.get('evidence_utterance', '').strip()
        found = False
        
        client_turns = [t['utterance_text'] for t in td['dialogue'] if t['interlocutor'] == 'client']
        
        for text in client_turns:
            if ev and (text.strip() == ev or ev in text.strip() or text.strip() in ev):
                found = True
                break
        
        if found:
            matched += 1
        else:
            unmatched_cases.append((tid, ev, client_turns[:2]))

print(f"Matched {matched} out of {total_res}")
if unmatched_cases:
    print("Example unmatched:")
    for c in unmatched_cases[:3]:
        print(f"Transcript {c[0]} target: {c[1][:50]}...")
