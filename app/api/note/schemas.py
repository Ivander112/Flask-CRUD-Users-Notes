from pydantic import BaseModel, Field, EmailStr
from api.base.base_schemas import BaseResponse, PaginationParams
from utils import REGEX_PASSWORD

# Create note
class CreateNoteRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=6, max_length=100)

class CreateNoteResponse(BaseResponse):
    data: dict | None

# Get note
    
class ReadNoteResponse(BaseResponse):
    data: dict | None

# Get all note

class ReadAllNoteParamRequest(PaginationParams):
    filter_by_user_id: bool = True,

class ReadAllNoteResponse(BaseResponse):
    data: dict | None

# Update note
    
class UpdateNoteRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=6, max_length=100)

class UpdateNoteResponse(BaseResponse):
    data: dict | None

# Deleted Note

class DeleteNoteResponse(BaseResponse):
    data: dict | None