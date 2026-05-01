# CLAUDE.md (수정중)

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --group dev

# Run development server (local)
uv run uvicorn app.main:app --reload

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/path/to/test_file.py

# ---------------------------------------------------------------------------
# Database (Alembic)
# ---------------------------------------------------------------------------

# Local DB 실행 (docker-compose)
docker compose --env-file .env up -d db

# 새 마이그레이션 파일 생성
uv run alembic revision --autogenerate -m "describe your changes"

# 마이그레이션 적용
uv run alembic upgrade head

# 마이그레이션 롤백 (1단계)
uv run alembic downgrade -1

# 현재 마이그레이션 상태 확인
uv run alembic current
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

```
vivac-api/
├── app/
│   ├── main.py              # FastAPI 앱 인스턴스, lifespan
│   ├── core/
│   │   ├── config.py        # pydantic-settings 기반 환경 설정
│   │   ├── database.py      # SQLAlchemy async 엔진, 세션, Base
│   │   └── bastion.py       # SSH 터널 매니저 (dev 환경)
│   ├── models/              # SQLAlchemy ORM 모델
│   ├── schemas/             # Pydantic 요청/응답 모델
│   ├── crud/                # DB 쿼리 함수
│   └── routers/             # FastAPI 라우터
├── alembic/                 # Alembic 마이그레이션
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── alembic.ini
├── docker-compose.yml       # Local PostgreSQL
├── pyproject.toml           # uv 패키지 관리
└── example.env              # 환경 변수 가이드 (실제 값 없음)
```

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
