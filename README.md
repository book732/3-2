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

기본 동작은 diff에서 API 키 형태, `token`/`secret`/`password` 할당값, 이메일을 마스킹하고 최대 10개 파일·200줄까지만 전송합니다. 패턴 기반 마스킹은 모든 민감정보를 찾아내지 못할 수 있으므로, 실행 전에 diff에 비밀정보가 없는지 확인하세요.

```powershell
python main.py commit --unsafe-full-diff
```

`--unsafe-full-diff`는 마스킹 및 파일·줄 제한을 해제합니다. 신뢰할 수 있는 저장소와 API에서만 사용하세요.

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
