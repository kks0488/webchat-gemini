<p align="center">
  <img src="assets/banner.png" alt="webchat-gemini: 로그인된 크롬의 Gemini 웹을 스크립트로" width="100%">
</p>

<p align="center">
  <a href="README.md"><b>English</b></a> · <b>한국어</b>
</p>

<h2 align="center">이미 쓰고 있는 Gemini를 터미널에서.<br>API 키도, 숨은 브라우저도, 추가 로그인도 없이.</h2>

<p align="center">
  지금 쓰는 크롬 창을 조종하는 작은 파이썬 스크립트 두 개입니다.<br>
  질문 파일을 Gemini에 넘기고, 답이 끝날 때까지 기다렸다가 마크다운으로 저장합니다.
</p>

| 파일 | 하는 일 |
| --- | --- |
| `cj.py` | 주소에 특정 글자가 들어간 크롬 탭을 찾아 자바스크립트를 실행하고 결과를 출력 (어느 사이트든 가능) |
| `gemini.py` | 새 채팅(또는 `--same`으로 이어서)에 질문을 입력·전송하고, 답이 더 바뀌지 않을 때까지 기다려 저장 |

<p align="center">
  <img src="assets/demo.png" alt="터미널: cj.py 결과와 gemini.py 도움말" width="80%">
</p>

## 빠른 시작

1. 크롬 **보기 → 개발자 정보 → Apple Events의 자바스크립트 허용** 켜기(한 번만).
2. `https://gemini.google.com` 탭 하나 열어 두기.
3. 실행:

```bash
git clone https://github.com/kks0488/webchat-gemini.git
cd webchat-gemini
echo "SQLite 장단점 5줄 요약" | ./gemini.py - answer.md
./gemini.py brief.txt draft.md --same
./gemini.py brief.txt --require-mode "Pro"     # 원하는 모델이 아니면 멈춤
```

## 자주 묻는 질문

**API가 필요한가요?** 아니요. 브라우저의 Gemini 웹을 그대로 쓰므로 내 계정 요금제를 따릅니다.

**윈도·리눅스는?** 아직 안 됩니다. AppleScript가 필요합니다.

**Gemini 화면이 바뀌어 안 될 때는?** `gemini.py`의 화면 요소(`.ql-editor`, `model-response`, 보내기 버튼 이름)를 고치면 됩니다.

## 라이선스

MIT © Kyoungsoo Kim — [LICENSE](LICENSE).
