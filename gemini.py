#!/usr/bin/env python3
"""Ask Gemini in your logged-in Chrome tab and get the answer back as text.

usage:
  gemini.py prompt.txt [answer.md] [--same] [--require-mode TEXT] [--timeout SEC]
  echo "question" | gemini.py - [answer.md]
"""
import argparse, json, os, subprocess, sys, time

CJ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cj.py")
HOST = "gemini.google.com"


def js(code: str) -> str:
    r = subprocess.run([sys.executable, CJ, HOST, "-"], input=code, capture_output=True, text=True)
    return r.stdout.strip()


def nav(url: str) -> None:
    subprocess.run(["osascript", "-e", f'''tell application "Google Chrome"
repeat with w in windows
repeat with t in tabs of w
if URL of t contains "{HOST}" then
set URL of t to "{url}"
return
end if
end repeat
end repeat
end tell'''])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompt", help="prompt file, or - for stdin")
    ap.add_argument("out", nargs="?", help="save the answer to this file")
    ap.add_argument("--same", action="store_true", help="continue in the current chat instead of opening a new one")
    ap.add_argument("--require-mode", metavar="TEXT", help="stop unless the model picker label contains TEXT")
    ap.add_argument("--timeout", type=int, default=900, help="max seconds to wait for the answer (default 900)")
    a = ap.parse_args()

    prompt = sys.stdin.read() if a.prompt == "-" else open(a.prompt, encoding="utf-8").read()
    if not a.same:
        nav(f"https://{HOST}/app")
        time.sleep(4)
    for _ in range(20):
        if js("document.querySelector('.ql-editor')?'ok':'no'") == "ok":
            break
        time.sleep(1)
    else:
        sys.exit("NO GEMINI TAB / EDITOR NOT FOUND")

    if a.require_mode:
        mode = js("""(function(){var b=[...document.querySelectorAll('button')].find(b=>/모드 선택|mode/i.test(b.getAttribute('aria-label')||''));return b?b.getAttribute('aria-label'):'?'})()""")
        if a.require_mode not in mode:
            sys.exit("MODE MISMATCH: " + mode)

    n0 = int(js("String(document.querySelectorAll('model-response').length)") or 0)
    js("(function(){var e=document.querySelector('.ql-editor');e.focus();document.execCommand('insertText',false,%s);return 'ok'})()" % json.dumps(prompt))
    time.sleep(1.5)
    r = js("""(function(){var b=[...document.querySelectorAll('button')].find(b=>/보내기|Send/.test(b.getAttribute('aria-label')||''));if(!b)return 'nobtn';b.click();return 'sent'})()""")
    if r != "sent":
        sys.exit("SEND FAILED: " + r)

    # Poll until the newest response stops changing and Gemini is no longer generating.
    last, stable, t0 = "", 0, time.time()
    while time.time() - t0 < a.timeout:
        time.sleep(5)
        st = js("""(function(){var rs=document.querySelectorAll('model-response');var busy=[...document.querySelectorAll('button')].some(b=>/중지|Stop/.test(b.getAttribute('aria-label')||''));var t=rs.length>%d?(function(m){return m?(m.innerText||m.textContent||''):''})(rs[rs.length-1].querySelector('message-content')):'';return JSON.stringify({busy:busy,t:t})})()""" % n0)
        try:
            d = json.loads(st)
        except Exception:
            continue
        stable = stable + 1 if d["t"] and not d["busy"] and d["t"] == last else 0
        last = d["t"]
        if stable >= 2:
            break
    if a.out:
        open(a.out, "w", encoding="utf-8").write(last)
    print(last)


if __name__ == "__main__":
    main()
