# VIVAC API - Architecture Overview

> 캠퍼를 위한 장소 큐레이션 서비스 백엔드 아키텍처

## Tech Stack

| 구분 | 기술 |
|------|------|
| Framework | FastAPI |
| Language | Python 3.x |
| ORM | SQLAlchemy 2.x (async) |
| Database | PostgreSQL 16 (asyncpg 드라이버) |
| Migration | Alembic |
| Auth | Google OAuth 2.0 + JWT (access/refresh) |
| Package Manager | uv |
| Local Infra | Docker Compose |

---

## Project Structure

```
vivacapi-core/
├── app/
│   ├── main.py                  # FastAPI 앱 인스턴스, 라우터 등록
│   ├── core/                    # 핵심 인프라 계층
│   │   ├── config.py            # pydantic-settings 기반 환경 설정
│   │   ├── database.py          # SQLAlchemy async 엔진, 세션, Base
│   │   ├── security.py          # Google ID Token 검증, JWT 생성/디코딩
│   │   └── deps.py              # FastAPI 의존성 (get_current_user 등)
│   ├── models/                  # SQLAlchemy ORM 모델
│   │   ├── user.py              # 사용자
│   │   ├── spot.py              # 캠핑 스팟
│   │   ├── spot_business_info.py # 스팟 사업자 정보
│   │   └── spot_review.py       # 스팟 리뷰
│   ├── schemas/                 # Pydantic 요청/응답 모델
│   │   ├── auth.py              # 로그인, 토큰 스키마
│   │   └── user.py              # 사용자 응답 스키마
│   ├── crud/                    # DB 쿼리 함수
│   │   └── user.py              # 사용자 CRUD
│   └── routers/                 # API 라우터
│       └── auth.py              # 인증 관련 엔드포인트
├── alembic/                     # DB 마이그레이션
│   ├── env.py
│   └── versions/
├── docker-compose.yml           # Local PostgreSQL
├── pyproject.toml               # 의존성 관리
└── .env                         # 환경 변수 (git 미추적)
```

---

## Layered Architecture

```
┌─────────────────────────────────────────────────────┐
│                     Client (App)                    │
└────────────────────────┬────────────────────────────┘
                         │ HTTP Request
                         ▼
┌─────────────────────────────────────────────────────┐
│                   Routers Layer                     │
│  - HTTP 입출력, 요청 검증, 의존성 주입              │
│  - auth.py: /auth/google, /auth/refresh, /auth/me   │
│  - GET /health                                       │
└────────────────────────┬────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Schemas    │ │    Deps      │ │   Security   │
│  (Pydantic)  │ │ (get_current │ │ (JWT, Google │
│  요청/응답    │ │  _user)      │ │  ID Token)   │
└──────────────┘ └──────┬───────┘ └──────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                    CRUD Layer                       │
│  - DB 쿼리/조작 담당                                 │
│  - AsyncSession 기반 비동기 처리                      │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                   Models Layer                      │
│  - SQLAlchemy ORM 테이블 정의                        │
│  - User, Spot, SpotBusinessInfo, SpotReview          │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                  PostgreSQL 16                      │
│  - asyncpg 드라이버 (비동기 연결)                    │
│  - Local: Docker Compose                             │
│  - Dev/Prod: AWS RDS (VPC 직접 접속)                 │
└─────────────────────────────────────────────────────┘
```

### 의존 방향 원칙

```
Routers → CRUD → Models
   ↓        ↓
Schemas    Core (config, database, security, deps)
```

- **Routers**: HTTP 입출력과 DI만 담당, 비즈니스 로직 최소화
- **CRUD**: DB 접근/쿼리 담당, 비즈니스 로직 포함 가능
- **Schemas**: Pydantic 기반 요청/응답 모델 정의
- **Models**: SQLAlchemy ORM 테이블 정의
- **Core**: 설정, 보안, DB 연결 등 횡단 관심사

---

## Authentication Flow

```
┌────────┐          ┌──────────┐          ┌────────────┐
│ Client │          │ VIVAC API│          │  Google    │
└───┬────┘          └────┬─────┘          └─────┬──────┘
    │                    │                      │
    │  1. Google 로그인   │                      │
    │ ──────────────────>│                      │
    │    (id_token)      │                      │
    │                    │  2. ID Token 검증     │
    │                    │ ────────────────────>│
    │                    │     (공개키 서명 검증) │
    │                    │ <────────────────────│
    │                    │     (sub, email, ...) │
    │                    │                      │
    │                    │  3. DB 조회/생성       │
    │                    │  (google_sub 기준)    │
    │                    │                      │
    │  4. JWT 토큰 쌍     │                      │
    │ <──────────────────│                      │
    │  (access + refresh)│                      │
    │                    │                      │
    │  5. API 요청        │                      │
    │ ──────────────────>│                      │
    │  Authorization:    │                      │
    │  Bearer {access}   │                      │
    │                    │                      │
    │  6. 응답            │                      │
    │ <──────────────────│                      │
```

- **Access Token**: HS256 JWT, 기본 30분 만료
- **Refresh Token**: HS256 JWT, 기본 7일 만료
- JWT payload에 `sub` (user uid), `type` (access/refresh), `iat`, `exp` 포함

---

## API Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/health` | 헬스체크 | - |
| `POST` | `/auth/google` | Google ID Token 로그인 | - |
| `POST` | `/auth/refresh` | 토큰 갱신 | - |
| `GET` | `/auth/me` | 현재 사용자 정보 조회 | Bearer JWT |

---

## Database

- **Engine**: SQLAlchemy `create_async_engine` (asyncpg)
- **Connection Pool**: `pool_size=5`, `max_overflow=10`, `pool_pre_ping=True`
- **Session**: `async_sessionmaker`, `expire_on_commit=False`
- **Migration**: Alembic (autogenerate 지원)
- **Local**: Docker Compose로 PostgreSQL 16 Alpine 실행
- **Environment**: `local` 환경에서 SQL echo 활성화

---

## Configuration

`pydantic-settings` 기반으로 `.env` 파일에서 환경 변수를 로드합니다.

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `ENVIRONMENT` | 실행 환경 (local/dev/prod) | `local` |
| `DB_HOST` | DB 호스트 | `localhost` |
| `DB_PORT` | DB 포트 | `5432` |
| `DB_NAME` | DB 이름 | (필수) |
| `DB_USER` | DB 사용자 | (필수) |
| `DB_PASSWORD` | DB 비밀번호 | (필수) |
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID | (필수) |
| `JWT_SECRET_KEY` | JWT 서명 키 | (필수) |
| `JWT_ALGORITHM` | JWT 알고리즘 | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Access Token 만료(분) | `30` |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | Refresh Token 만료(일) | `7` |
