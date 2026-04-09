import json
import os

def clean_labels(workspace_dir="."):
    dataset_path = os.path.join(workspace_dir, "dataset", "AnnoMI-labeled.json")
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Dictionary for translation
    TRANSLATION_MAP = {
        # Parents
        "否认": "Denying",
        "争辩": "Arguing",
        "回避": "Avoiding",
        "忽视": "Ignoring",
        "不抗拒": "No Resistance",
        
        # Categories (Common ones from PsyFIRE / CBS)
        "指责": "Blaming",
        "责备": "Blaming", # Additional variant
        "不同意": "Disagreeing",
        "找借口": "Excusing",
        "轻视": "Minimizing",
        "悲观": "Pessimism",
        "不情愿": "Reluctance",
        "犹豫": "Reluctance", # Additional variant
        "愿意": "Willingness",
        "不愿意": "Unwillingness",
        "拒绝承认或承担责任": "Denying", # Additional variant
        
        "挑战": "Challenging",
        "打折扣": "Discounting",
        "贬低": "Discounting", # Additional variant
        
        "最少交谈": "Minimum Talk",
        "设定界限": "Limit Setting",
        "设定限制": "Limit Setting", # Additional variant
        "转移话题": "Topic Shift",
        "假配合": "Pseudo-Compliance",
        
        "不专心": "Inattention",
        "偏离主轨道": "Sidetracking",
        
        "探索": "Exploratory",
        "合作": "Cooperative",
        "解决": "Resolution"
    }
    
    transcripts = data.get("transcripts", {})
    changes_made = 0
    
    for tid, tdata in transcripts.items():
        psyfire_label = tdata.get("psyfire_label")
        if not psyfire_label:
            continue
            
        parent = psyfire_label.get("parent_category")
        category = psyfire_label.get("category")
        
        if parent in TRANSLATION_MAP:
            psyfire_label["parent_category"] = TRANSLATION_MAP[parent]
            changes_made += 1
            
        if category in TRANSLATION_MAP:
            psyfire_label["category"] = TRANSLATION_MAP[category]
            changes_made += 1
            
    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Cleaned {changes_made} fields in AnnoMI-labeled.json. Updated to English.")

if __name__ == "__main__":
    # Ensure run relative to workspace
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_labels(workspace)
