import csv
import time
import requests

INPUT_FILE = 'experiments/e05/c_urls_ranked.txt'
OUTPUT_FILE = 'experiments/e05/url_check_results.csv'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def check_url(url):
    try:
        # Try HEAD request first
        res = requests.head(url, headers=HEADERS, timeout=10, allow_redirects=True)
        # Some servers return 405 Method Not Allowed or 403 for HEAD requests, fall back to GET
        if res.status_code in (405, 403, 400, 501):
            res = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True, stream=True)
        status = res.status_code
    except Exception as e:
        # If HEAD raises an exception, try GET fallback
        try:
            res = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True, stream=True)
            status = res.status_code
        except Exception as e2:
            status = type(e2).__name__

    resolves = (status == 200)
    return status, resolves

def main():
    rows = []
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t', 1)
            if len(parts) == 2:
                count, url = parts
                rows.append((int(count), url))

    print(f"Loaded {len(rows)} URLs to check.")

    results = []
    for idx, (count, url) in enumerate(rows, 1):
        print(f"[{idx}/{len(rows)}] Checking: {url} ...", end=" ", flush=True)
        status, resolves = check_url(url)
        print(f"Status: {status} | Resolves: {resolves}")
        results.append({
            'count': count,
            'url': url,
            'status': status,
            'resolves': str(resolves)
        })
        time.sleep(0.5)

    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['count', 'url', 'status', 'resolves'])
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved results to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
