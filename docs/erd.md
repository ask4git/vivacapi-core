# VIVAC API - Database ERD

> Entity Relationship Diagram (Mermaid)
>
> GitHub, VS Code(Markdown Preview Mermaid 확장) 등에서 시각적으로 렌더링됩니다.

## ERD

```mermaid
erDiagram
    users {
        UUID uid PK
        VARCHAR(320) email UK "unique, indexed"
        VARCHAR(255) google_sub UK "unique, indexed"
        VARCHAR(100) name "nullable"
        VARCHAR(2048) picture "nullable"
        BOOLEAN is_active "default: true"
        TIMESTAMPTZ created_at "server_default: now()"
        TIMESTAMPTZ updated_at "server_default: now(), onupdate"
    }

    spots {
        UUID uid PK
        VARCHAR title "indexed"
        VARCHAR address "nullable"
        VARCHAR address_detail "nullable"
        VARCHAR region_province "nullable, indexed"
        VARCHAR region_city "nullable, indexed"
        VARCHAR postal_code "nullable"
        VARCHAR phone "nullable"
        VARCHAR description "nullable"
        VARCHAR tagline "nullable"
        FLOAT latitude "nullable"
        FLOAT longitude "nullable"
        FLOAT altitude "nullable"
        INTEGER unit_count "nullable"
        BOOLEAN is_fee_required "nullable"
        BOOLEAN is_pet_allowed "nullable"
        VARCHAR pet_policy "nullable"
        VARCHAR[] has_equipment_rental "nullable, ARRAY"
        VARCHAR[] themes "nullable, ARRAY"
        VARCHAR fire_pit_type "nullable"
        VARCHAR[] amenities "nullable, ARRAY"
        VARCHAR[] nearby_facilities "nullable, ARRAY"
        VARCHAR camp_sight_type "nullable"
        FLOAT rating_avg "indexed"
        INTEGER review_count
        VARCHAR website_url "nullable"
        VARCHAR booking_url "nullable"
        VARCHAR features "nullable"
        VARCHAR[] category "nullable, ARRAY"
        FLOAT total_area_m2 "nullable"
        BOOLEAN has_liability_insurance "nullable"
        TIMESTAMPTZ created_at "server_default: now()"
        TIMESTAMPTZ updated_at "server_default: now(), onupdate"
    }

    spot_business_info {
        UUID uid PK
        UUID spot_uid FK "indexed"
        VARCHAR business_reg_no "nullable"
        VARCHAR tourism_business_reg_no "nullable"
        VARCHAR business_type "nullable"
        VARCHAR operation_type "nullable"
        VARCHAR operating_agency "nullable"
        VARCHAR operating_status "nullable, indexed"
        INTEGER national_park_no "nullable"
        VARCHAR national_park_office_code "nullable"
        VARCHAR national_park_serial_no "nullable"
        VARCHAR national_park_category_code "nullable"
        DATE licensed_at "nullable"
        TIMESTAMPTZ created_at "server_default: now()"
        TIMESTAMPTZ updated_at "server_default: now(), onupdate"
    }

    spot_reviews {
        UUID uid PK
        UUID spot_uid FK "indexed"
        UUID user_id FK "indexed"
        FLOAT rating "NOT NULL, CHECK 0-5"
        VARCHAR content "nullable"
        TIMESTAMPTZ created_at "server_default: now()"
        TIMESTAMPTZ updated_at "server_default: now(), onupdate"
    }

    spots ||--o{ spot_business_info : "has business info"
    spots ||--o{ spot_reviews : "has reviews"
    users ||--o{ spot_reviews : "writes reviews"
```

## Relationships

| 관계 | 설명 | FK | 제약 조건 |
|------|------|----|-----------|
| `spots` → `spot_business_info` | 1:N | `spot_business_info.spot_uid` → `spots.uid` | - |
| `spots` → `spot_reviews` | 1:N | `spot_reviews.spot_uid` → `spots.uid` | - |
| `users` → `spot_reviews` | 1:N | `spot_reviews.user_id` → `users.uid` | `UNIQUE(spot_uid, user_id)` - 유저당 스팟별 리뷰 1개 |

## Constraints

| 테이블 | 이름 | 타입 | 설명 |
|--------|------|------|------|
| `spot_reviews` | `uq_spot_user_review` | UNIQUE | `(spot_uid, user_id)` - 동일 유저가 같은 스팟에 중복 리뷰 불가 |
| `spot_reviews` | `check_review_rating_range` | CHECK | `rating >= 0 AND rating <= 5` |

## Indexes

| 테이블 | 컬럼 | 용도 |
|--------|------|------|
| `users` | `email` | 이메일 조회 |
| `users` | `google_sub` | Google 로그인 시 사용자 매칭 |
| `spots` | `title` | 스팟 이름 검색 |
| `spots` | `region_province` | 지역(도/광역시) 필터 |
| `spots` | `region_city` | 지역(시/군/구) 필터 |
| `spots` | `rating_avg` | 평점 정렬 |
| `spot_business_info` | `spot_uid` | 스팟별 사업자 정보 조회 |
| `spot_business_info` | `operating_status` | 운영 상태 필터 |
| `spot_reviews` | `spot_uid` | 스팟별 리뷰 조회 |
| `spot_reviews` | `user_id` | 유저별 리뷰 조회 |
