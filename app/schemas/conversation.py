from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class MessageSchema(BaseModel):
    content: str
    timestamp: datetime
    role: Role
    related_property_ids: Optional[List[str]] = Field(default_factory=list)


class ConversationCreate(BaseModel):
    user_id: str
    title: Optional[str] = "New Conversation"
    messages: List[MessageSchema] = Field(default_factory=list)
    related_property_ids: Optional[List[str]] = Field(default_factory=list)


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[ConversationStatus] = None


class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    status: ConversationStatus
    messages: List[MessageSchema] = Field(default_factory=list)
    related_property_ids: Optional[List[str]] = Field(default_factory=list)
    last_message_timestamp: datetime
