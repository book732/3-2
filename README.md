# Git 커밋 및 PR 초안 생성기

Git 변경 사항을 AI API에 전달해 커밋 메시지 또는 Pull Request 초안을 만드는 Python CLI입니다. 결과는 터미널에만 출력하며 자동 커밋, push, PR 생성은 하지 않습니다.

## 요구 사항

- Python 3.10 이상
- Git
- OpenAI 호환 Chat Completions API와 API 키

## 설치

외부 Python 패키지는 필요하지 않습니다. 저장소를 받은 뒤 프로젝트 폴더로 이동해 바로 실행합니다.

```powershell
git clone <저장소 주소>
cd 3-2
python --version
```

## 설정

PowerShell:

```powershell
$env:AI_API_KEY = "발급받은_API_키"
$env:AI_MODEL = "사용할_모델명"
```

API 기본 주소는 `https://api.openai.com/v1`입니다. 호환 API를 쓰는 경우 주소를 바꿀 수 있습니다.

```powershell
$env:AI_API_BASE_URL = "https://api.example.com/v1"
```

Codyssey 가상 키를 사용하는 경우에는 다음 값을 사용합니다.

```powershell
$env:AI_MODEL = "gpt-5.5"
$env:AI_API_BASE_URL = "https://copa.codyssey.kr/v1"
```

`gpt-5.5` 요청에는 `max_completion_tokens`를 사용하며, 지원되지 않는 `temperature` 값은 보내지 않습니다.

## 실행

저장소 안에서 실행합니다.

```powershell
python main.py commit
python main.py pr
```

모델과 생성 파라미터는 옵션으로도 지정할 수 있습니다.

```powershell
python main.py commit --model "사용할_모델명" --temperature 0.2 --max-tokens 1200
```

## 안전 모드

기본 동작은 diff에서 API 키 형태, `token`/`secret`/`password` 할당값, 이메일을 마스킹하고 diff 내용을 최대 10개 파일·200줄로 제한합니다. Git status의 파일명 목록은 제한 대상이 아닙니다. 패턴 기반 마스킹은 모든 민감정보를 찾아내지 못할 수 있으므로, 실행 전에 diff에 비밀정보가 없는지 확인하세요.

```powershell
python main.py commit --safe-files 5 --safe-lines 100
python main.py commit --unsafe-full-diff
```

`--safe-files`와 `--safe-lines`는 각각 diff 파일 수와 줄 수 제한을 조정합니다. 1 이상의 정수를 입력해야 합니다. `--unsafe-full-diff`는 마스킹 및 두 제한을 해제합니다. 신뢰할 수 있는 저장소와 API에서만 사용하세요.

테스트용 가짜 키 `sk-example-token-1234567890`과 두 텍스트 파일을 사용해 API 전송 전 컨텍스트를 비교했습니다.

| 설정 | 키 값 | 두 번째 파일 내용 |
| --- | --- | --- |
| 안전 모드 ON (`--safe-files 1 --safe-lines 20`) | `api_key=[REDACTED]` | `[safe-mode: 나머지 파일 diff 생략]` |
| 안전 모드 OFF (`--unsafe-full-diff`) | 가짜 키 원문 포함 | 포함 |

`python -m unittest discover -s tests -v`로 마스킹, 파일·줄 제한, ON/OFF 동작을 확인할 수 있습니다.

## 생성 결과 규칙

- 커밋 제목은 50자 이내를 권장하며 최대 72자입니다.
- PR 제목은 최대 80자입니다.
- PR 본문에는 `Why`, `What`, `How to Test` 섹션과 각 섹션의 불릿이 필요합니다.
- 생성 결과를 검토한 뒤 직접 적용합니다. 도구는 `git commit`, `git push`, GitHub PR 생성을 실행하지 않습니다.

## 출력 예시

커밋 메시지:

```text
--- Commit Message ---
feat(cli): generate commit drafts from Git changes

- Summarize changed files and key behavior
```

PR 초안:

```text
--- PR Title ---
feat: generate commit and PR drafts

--- PR Body ---
## Why
- Keep change summaries consistent.

## What
- Generate drafts from local Git changes.

## How to Test
- Run the CLI against a repository with changes.
```

## 요청 수와 비용

정상 결과는 실행 1회당 API 요청 1회입니다. 첫 응답의 형식 검증에 실패하면 한 번 재생성하여 최대 2회 요청합니다. `commit`과 `pr`를 각각 실행하면 각각 별도 요청을 보냅니다. 토큰 사용량과 비용은 모델 및 diff 크기에 따라 달라집니다.

## 제한 사항

- 추적되지 않은 텍스트 파일도 diff 입력에 포함합니다. 바이너리 파일은 내용 대신 생략 표시를 전달합니다.
- GitHub 저장소 업로드 및 실제 PR 제출은 별도 작업입니다.

## 보너스: 저장소별 양식

이전 미션 저장소 [2-1](https://github.com/book732/2-1)의 기존 커밋은 `feat :`, `fix:`, `chore:` 접두사를 사용했지만 콜론 앞 공백이 일정하지 않았습니다. 기존 PR은 없었습니다. 이 저장소에 적용할 양식은 `feat:`, `fix:`, `chore:` 뒤에 공백 한 칸과 간결한 한국어 제목을 쓰고, PR은 `Why`/`What`/`How to Test` 헤더 아래 한국어 불릿을 쓰는 것입니다.

```powershell
python main.py commit --convention "For repo 2-1, use feat:, fix:, or chore: with no space before colon. Write the title and body bullets in Korean. Keep required format and length rules."
python main.py pr --convention "For repo 2-1, use feat:, fix:, or chore: with no space before colon. Write Korean bullets. Keep Why, What, and How to Test headings and the required format and length rules."
```

같은 CSV 가져오기 수정 diff로 실제 생성한 커밋 메시지 비교입니다.

| 설정 | 생성된 제목 | 본문 예시 |
| --- | --- | --- |
| 적용 전 | `fix(import): handle short CSV rows` | `Treat missing memo or tags cells as empty during CSV import` |
| 적용 후 | `fix: CSV 가져오기 누락 셀 처리` | `필수 값이 빠진 행은 건너뛰고 선택 값 누락은 빈 값으로 처리` |

적용 후 실행은 첫 응답의 형식 검증 실패로 API를 2회 호출했고, 최종 초안은 규칙을 통과했습니다.

## 보너스: 실제 PR 적용

[2-1 PR #1](https://github.com/book732/2-1/pull/1)에 이 도구로 만든 커밋 메시지와 PR 초안을 적용했습니다. AI 초안에서 최종 PR까지 다음을 다듬었습니다.

- PR 제목 `fix:CSV`의 콜론 뒤에 공백을 넣어 `fix: CSV`로 고쳤습니다.
- 실패 가능성으로 표현된 배경을 재현된 CSV 셀 누락 오류로 명확히 했습니다.
- 필수 셀 누락 시 건너뛰기와 선택 셀 누락 시 빈 값 처리 범위를 분명히 했습니다.
- AI가 제안한 `pytest` 명령을 실제 실행한 `python -m unittest discover -s tests -p test_cli.py`로 바꿨습니다.
- 통과한 테스트 수 5개와 `imported=1, skipped=1` 확인 결과를 PR에 적었습니다.
