---
name: git_commit
description: 현재 변경사항을 분석하여 적절한 커밋 메시지를 작성하고 local git에 커밋합니다.
disable-model-invocation: true
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git add *) Bash(git commit *)
---

# 로컬 Git 커밋

현재 작업 디렉토리의 변경사항을 분석하고, 적절한 커밋 메시지를 작성하여 로컬 git에 커밋합니다.

## 절차

### 1단계: 현재 상태 파악

아래 명령어를 **병렬로** 실행하여 변경 내역을 파악합니다:

```bash
git status
git diff --staged
git diff
git log --oneline -5
```

### 2단계: 커밋 메시지 작성

최근 커밋 히스토리의 스타일을 따르되, 아래 Conventional Commits 규칙을 적용합니다:

- **타입**: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `style`, `perf`, `ci`
- **제목**: 한글로 작성, 70자 이내
- **본문** (선택): 변경 이유나 주요 내용을 간결하게 기술
- **꼬리말**: 항상 `Co-Authored-By: Claude <noreply@anthropic.com>` 포함

### 3단계: 스테이징 및 커밋

- `.env`, `*.pem`, `*.key`, `credentials*.json` 등 민감 파일이 포함되어 있으면 **경고하고 제외**합니다.
- `git add -A` 대신 관련 파일만 개별적으로 `git add` 합니다.
- 커밋 메시지는 HEREDOC 형식으로 전달합니다:

```bash
git commit -m "$(cat <<'EOF'
<type>: <제목>

<본문 (선택)>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 4단계: 결과 확인

커밋 후 `git status`를 실행하여 커밋이 정상적으로 완료되었는지 확인합니다.

## 주의사항

- **push하지 않습니다.** 이 스킬은 로컬 커밋만 수행합니다.
- 변경사항이 없으면 빈 커밋을 생성하지 않고 사용자에게 알립니다.
- 사용자가 `$ARGUMENTS`로 커밋 메시지를 직접 지정하면 해당 메시지를 우선 사용합니다.
