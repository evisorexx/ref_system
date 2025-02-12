from datetime import datetime
from pydantic import BaseModel

class ReferralCodeCreate(BaseModel):
    expiration_date: datetime

class ReferralCodeResponse(BaseModel):
    code: str
    expiration_date: datetime
    is_active: bool