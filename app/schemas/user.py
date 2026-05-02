from datetime import datetime

from pydantic import BaseModel, ConfigDict, computed_field


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str | None
    picture: str | None
    is_active: bool
    identity_verified_at: datetime | None
    onboarding_survey_completed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_identity_verified(self) -> bool:
        return self.identity_verified_at is not None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def has_completed_onboarding_survey(self) -> bool:
        return self.onboarding_survey_completed_at is not None
