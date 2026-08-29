import os, requests, json

def call(prompt, seed=None, temperature=1.0):
    body = {
        "model": "qwen/qwen3.6-27b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 2048,
        "provider" : {

        "order": ["Alibaba"],
         "allow_fallbacks": False
    }
    }
    if seed is not None:
        body["seed"] = seed
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
        json=body, timeout=180,
    )
    r.raise_for_status()
    return r.json()

a = call("Say a random four-digit number.", seed=42)
b = call("Say a random four-digit number.", seed=42)
print(a["choices"][0]["message"]["content"])
print(b["choices"][0]["message"]["content"])
print("Provider A:", a.get("provider"))
print("Provider B:", b.get("provider"))
print("Full response A keys:", list(a.keys()))
print("SEEDS HONORED:", a["choices"][0]["message"]["content"] ==
                        b["choices"][0]["message"]["content"])