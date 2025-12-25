from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

class RawMember(BaseModel):
    full_name: Optional[str] = Field(alias="Full Name")
    email: Optional[str] = Field(default=None, alias="Email Address")

    date_joined: Optional[str] = Field(default=None, alias="Date Joined")
    bio: Optional[str] = Field(alias="Bio_or_comment")
    last_activity: Optional[str] = Field(alias="Last Activity")

    class Config:
        populate_by_name = True

class ProcessingResult(BaseModel):
    valid_members: list[dict] = []
    errors: list[dict] = []
