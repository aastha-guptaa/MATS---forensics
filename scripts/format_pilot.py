#!/usr/bin/env python3
import json
import os

pilot_path = "experiments/e01/pilot.json"
md_path = "experiments/e01/transcripts.md"
labels_path = "experiments/e01/labels.json"

with open(pilot_path) as f:
    records = [json.loads(line) for line in f]

md_lines = [
    "# e01 Pilot Responses for Hand-Labelling",
    "Total records: 30 (29 complete, 1 truncated with finish_reason=length)\n",
    "---\n"
]

template_labels = []

for idx, r in enumerate(records):
    p_id = r.get("prompt_id")
    req_i = r.get("request_index")
    fr = r.get("finish_reason")
    tokens = r.get("completion_tokens")
    text = r.get("response_text") or ""
    
    short_prompt = "graalvm" if "graalvm" in p_id else ("dotnet" if "dotnet" in p_id else p_id)
    
    md_lines.append(f"## Index {idx}: Prompt `{p_id}` (Request {req_i})")
    md_lines.append(f"- **Finish Reason**: `{fr}` | **Tokens**: `{tokens}` | **Provider**: `{r.get('provider')}`")
    if fr == "length":
        md_lines.append("> [!WARNING]")
        md_lines.append("> **TRUNCATED** (finish_reason = length). Excluded from active labelling matching WeirdChat rules.\n")
    
    md_lines.append("\n### Response Text:\n")
    md_lines.append(text)
    md_lines.append("\n\n---\n")
    
    label_entry = {
        "index": idx,
        "prompt_id": short_prompt,
        "full_prompt_id": p_id,
        "request_index": req_i,
        "finish_reason": fr,
        "rungs_present": [],
        "highest_rung": "",
        "disclaim": False,
        "wc_proxy": False,
        "ambiguous": False,
        "evidence": {},
        "notes": ""
    }
    if fr == "length":
        label_entry["notes"] = "EXCLUDED: truncated (finish_reason=length)"
        label_entry["truncated"] = True
    
    template_labels.append(label_entry)

os.makedirs(os.path.dirname(md_path), exist_ok=True)

with open(md_path, "w") as f:
    f.write("\n".join(md_lines))

with open(labels_path, "w") as f:
    json.dump(template_labels, f, indent=2)

print(f"Successfully generated:")
print(f" - Readable Markdown: {md_path}")
print(f" - Starter JSON template: {labels_path}")
