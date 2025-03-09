# Value Objects
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from app.models.base_model import BaseModelApp
from app.models.conversation_models.conversation import Message
from app.models.property_models.property import Property
from app.schemas.conversation import ConversationStatus, Role


class AIMessageResponseDTO(BaseModelApp):
    content: str
    related_properties: List[Property] = Field(default_factory=list)
    best_property_id: Optional[Property] = None
    role: Role = Role.ASSISTANT


class UserMessageRequestDTO(BaseModel):
    content: str


class ConversationResponse(BaseModelApp):
    user_id: str
    title: str = Field(default="New Conversation")
    status: ConversationStatus = ConversationStatus.ACTIVE
    messages: List[Message] = Field(default_factory=list)
    message_count: int = 0
    related_properties: set[Property] = Field(default_factory=set)
    last_property: set[Property] = Field(default_factory=set)
    last_message_timestamp: datetime = Field(default_factory=datetime.now)
