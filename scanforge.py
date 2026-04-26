#!/usr/bin/env python3

import argparse
import sys
import urllib.parse
import html as html_lib

import requests

# ===== COLORS =====
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

headers = {"User-Agent": "Mozilla/5.0"}
report_data = []


def log(msg, color=None):
    if color:
        print(color + msg + RESET)
    else:
        print(msg)
    report_data.append(msg)


def build_url(parsed, params, param, payload):
    new_params = params.copy()
    new_params[param] = payload
    encoded = urllib.parse.urlencode(new_params, doseq=True)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{encoded}"


def test_xss(parsed, params):
    log("\n[*] XSS Testing", YELLOW)
    found = False

    payloads = [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
    ]

    for param in params:
        for payload in payloads:
            test_url = build_url(parsed, params, param, payload)

            try:
                res = requests.get(test_url, headers=headers, timeout=5)
                if payload in res.text:
                    log(f"[!] XSS FOUND → {param}", RED)
                    log(f"Payload: {payload}")
                    log(f"URL: {test_url}\n")
                    found = True
            except requests.RequestException:
                log("[-] Request failed")

    if not found:
        log("[+] No XSS detected", GREEN)

    return found


def test_sqli(parsed, params):
    log("\n[*] SQL Injection Testing", YELLOW)
    found = False

    payload = "' OR '1'='1"

    for param in params:
        try:
            normal = requests.get(
                build_url(parsed, params, param, "1"),
                headers=headers,
                timeout=5,
            )

            injected_url = build_url(parsed, params, param, payload)
            injected = requests.get(
                injected_url,
                headers=headers,
                timeout=5,
            )

            if abs(len(normal.text) - len(injected.text)) > 50:
                log(f"[!] SQLi FOUND → {param}", RED)
                log(f"Payload: {payload}")
                log(f"URL: {injected_url}\n")
                found = True

        except requests.RequestException:
            log("[-] Request failed")

    if not found:
        log("[+] No SQL Injection detected", GREEN)

    return found


def save_html(filename):
    html = [
        "<html>",
        "<head>",
        "<meta charset='utf-8'>",
        "<title>ScanForge Report</title>",
        "<style>",
        "body{font-family:Arial,sans-serif;background:#111;color:#eee;padding:20px;}",
        "pre{background:#1b1b1b;padding:16px;border-radius:8px;white-space:pre-wrap;}",
        "</style>",
        "</head>",
        "<body>",
        "<h2>ScanForge Report</h2>",
        "<pre>",
    ]

    for line in report_data:
        html.append(html_lib.escape(line))

    html += [
        "</pre>",
        "</body>",
        "</html>",
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(html))


def main():
    parser = argparse.ArgumentParser(description="ScanForge - Web Scanner")
    parser.add_argument("-u", "--url", help="Target URL")
    parser.add_argument("-f", "--file", help="File with URLs")
    parser.add_argument("-o", "--output", default="report.html", help="Output report file")
    args = parser.parse_args()

    targets = []

    if args.url:
        targets.append(args.url)

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                targets.extend([line.strip() for line in f if line.strip()])
        except OSError:
            print("[-] Could not read file")
            sys.exit(1)

    if not targets:
        print("Provide -u <url> or -f <file>")
        sys.exit(1)

    for target in targets:
        log("=" * 50)
        log(f"Target: {target}")
        log("=" * 50)

        parsed = urllib.parse.urlparse(target)
        query = parsed.query

        if not query:
            log("[-] No parameters found (check URL or use quotes)\n")
            continue

        params = urllib.parse.parse_qs(query)

        x = test_xss(parsed, params)
        s = test_sqli(parsed, params)

        log("\nSUMMARY")
        if not x and not s:
            log("[+] No vulnerabilities detected", GREEN)
        else:
            log("[!] Vulnerabilities detected", RED)

    save_html(args.output)
    print(f"\n[+] HTML report saved as {args.output}")


if __name__ == "__main__":
    main()
