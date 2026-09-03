#!/usr/bin/env python3
"""Generate raw completions via OpenRouter for each prompt in data/prompts.json.

Defaults to qwen/qwen3.6-27b on Alibaba; override with --model / --provider."""
import argparse
import hashlib
import json
import os
import threading
import time
from datetime import datetime, timezone

import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "qwen/qwen3.6-27b"
DEFAULT_PROVIDER = "Alibaba"
MAX_ATTEMPTS = 3
RETRY_BACKOFF_S = 5


def call(prompt, temperature, max_tokens, model, provider):
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "provider": {
            "order": [provider],
            "allow_fallbacks": False,
        },
        "reasoning": {"effort": "none"},
    }
    r = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
        json=body,
        timeout=180,
    )
    r.raise_for_status()
    return r.json()


def call_with_retries(prompt, temperature, max_tokens, model, provider):
    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return call(prompt, temperature, max_tokens, model, provider), None
        except Exception as e:
            last_error = e
            if attempt < MAX_ATTEMPTS:
                time.sleep(RETRY_BACKOFF_S * attempt)
    return None, last_error


def make_record(prompt_id, prompt_hash, request_index, response_json):
    choice = response_json["choices"][0]
    message = choice["message"]
    usage = response_json.get("usage", {})
    return {
        "prompt_id": prompt_id,
        "prompt_sha256": prompt_hash,
        "request_index": request_index,
        "response_id": response_json.get("id"),
        "response_text": message.get("content"),
        "finish_reason": choice.get("finish_reason"),
        "native_finish_reason": choice.get("native_finish_reason"),
        "provider": response_json.get("provider"),
        "system_fingerprint": response_json.get("system_fingerprint"),
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
        "cost": usage.get("cost"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error": None,
    }


def make_error_record(prompt_id, prompt_hash, request_index, error):
    return {
        "prompt_id": prompt_id,
        "prompt_sha256": prompt_hash,
        "request_index": request_index,
        "response_id": None,
        "response_text": None,
        "finish_reason": None,
        "native_finish_reason": None,
        "provider": None,
        "system_fingerprint": None,
        "prompt_tokens": None,
        "completion_tokens": None,
        "total_tokens": None,
        "cost": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error": str(error),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", default="data/prompts.json")
    parser.add_argument("--out", default="experiments/e01/raw.json")
    parser.add_argument("--n", type=int, default=15, help="requests per prompt")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--provider", default=DEFAULT_PROVIDER, help="OpenRouter provider slug, e.g. Alibaba")
    parser.add_argument("--workers", type=int, default=5, help="concurrent request workers")
    args = parser.parse_args()

    if "OPENROUTER_API_KEY" not in os.environ:
        raise SystemExit("OPENROUTER_API_KEY not set")

    with open(args.prompts) as f:
        prompts = json.load(f)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    if os.path.exists(args.out):
        with open(args.out) as f:
            existing = sum(1 for _ in f)
        print(f"WARNING: {args.out} already has {existing} records; appending.")

    work_items = []
    for p in prompts:
        prompt_id = p["id"]
        text = p["prompt"]
        prompt_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        for i in range(args.n):
            work_items.append((prompt_id, prompt_hash, text, i))

    total = len(work_items)
    done = 0
    failed = 0
    write_lock = threading.Lock()

    def process_one(item):
        prompt_id, prompt_hash, text, i = item
        response, error = call_with_retries(text, args.temperature, args.max_tokens, args.model, args.provider)
        if error is not None:
            record = make_error_record(prompt_id, prompt_hash, i, error)
        else:
            record = make_record(prompt_id, prompt_hash, i, response)
        return record

    from concurrent.futures import ThreadPoolExecutor, as_completed

    with open(args.out, "a") as out_f, ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(process_one, item) for item in work_items]
        for fut in as_completed(futures):
            record = fut.result()
            with write_lock:
                out_f.write(json.dumps(record) + "\n")
                out_f.flush()
            done += 1
            if record.get("error"):
                failed += 1
                print(f"[{done}/{total}] prompt={record['prompt_id']} i={record['request_index']} ERROR: {record['error']}")
            else:
                print(f"[{done}/{total}] prompt={record['prompt_id']} i={record['request_index']} ok")

    print(f"done. {done} requests, {failed} failed. wrote to {args.out}")



if __name__ == "__main__":
    main()
