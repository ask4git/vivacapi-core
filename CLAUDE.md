# CLAUDE.md (수정중)

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

<!-- Fill in once project is bootstrapped -->

```bash
# Install dependencies
# TODO

# Run development server
# TODO

# Build
# TODO

# Lint
# TODO

# Run all tests
# TODO

# Run a single test file
# TODO
```

## Architecture

<!-- Fill in once project structure is established -->

- **Framework:** FastAPI
- **Database / ORM:** SQLAlchemy asyncio + PostgreSQL(asyncpg)
- **Auth:** JWT Bearer + Google ID Token verify

## 2) 기본 아키텍처 원칙
- 패키지/의존성 관리는 `uv`를 사용한다.
- 의존 방향:
  - `routers`는 HTTP 입출력과 DI만 담당
  - `crud`는 DB 접근/쿼리 담당
  - `schemas`는 요청/응답 모델 정의
  - `models`는 SQLAlchemy ORM 테이블 정의
  - `core`는 설정/보안/DB 연결
- 비즈니스 로직은 가능하면 `crud` 또는 명시적 서비스 계층으로 이동하고, 라우터는 얇게 유지한다.
- 모든 DB 접근은 `AsyncSession`과 `await` 기반으로 작성한다.

## Project Structure

<!-- Describe the top-level layout and any non-obvious conventions here -->

## Key Conventions
<!-- Document patterns that are not obvious from reading individual files — e.g., how requests flow through layers, naming rules, shared abstractions -->
### 📝 Git Workflow & Branching Strategy

- **Restricted Direct Push:** Direct pushes to the `main` branch are strictly prohibited. All changes must be submitted via Pull Request.

- **Branch Naming Convention:** Use the `type/description` pattern for all new branches.
  - *Example:* `feature/user-authentication`
  - *Example:* `fix/issue-connection-timeout`
  - *Example:* `refactor/clean-up-database-logic`

프로젝트 개요는 @PRODUCT.md를 참조하세요.
<!-- 사용 가능한 npm 명령은 @package.json을 참조하세요. -->

## 추가 지시사항

- API 설계/응답 규약: @.claude/rules/api-conventions.md
- 코드 작성 스타일: @.claude/rules/code-style.md
- 보안/인증 규약: @.claude/rules/security.md
- 테스트 전략/작성 규칙: @.claude/rules/testing.md
