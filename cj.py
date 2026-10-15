#!/usr/bin/env python3
# usage: cj.py <url-substring> <js-file-or-'-'>  : run JS in matching Chrome tab, print result
import sys, subprocess, json
sub=sys.argv[1]; js=open(sys.argv[2]).read() if sys.argv[2]!='-' else sys.stdin.read()
script='''on run argv
set sub to item 1 of argv
set js to item 2 of argv
tell application "Google Chrome"
repeat with w in windows
repeat with t in tabs of w
if URL of t contains sub then return execute t javascript js
end repeat
end repeat
end tell
return "NO_TAB"
end run'''
try:
    r=subprocess.run(["osascript","-e",script,sub,js],capture_output=True,text=True,timeout=60)
except subprocess.TimeoutExpired:
    print("TIMEOUT"); sys.exit(2)
print(r.stdout.strip() or r.stderr.strip())
