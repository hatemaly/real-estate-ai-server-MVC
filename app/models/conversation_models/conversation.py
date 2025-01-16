# src/models/conversation_models/conversation.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum


# Enums
class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


# Value Objects
class Response(BaseModel):
    content: str
    related_property_ids: List[str] = Field(default_factory=list)
    role: Role = Role.ASSISTANT


class Message(BaseModel):
    number: Optional[int] = None
    content: str
    timestamp: datetime
    response: Optional[Response] = None
    role: Role = Role.USER


# Main Entity
class Conversation(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    title: str = Field(default="New Conversation")
    status: ConversationStatus = ConversationStatus.ACTIVE
    messages: List[Message] = Field(default_factory=list)
    message_count: int = 0
    related_property_ids: List[str] = Field(default_factory=list)
    last_message_timestamp: datetime = Field(default_factory=datetime.now)

    def add_message(self, message: Message):
        """Add a message to the conversation."""
        message.number = self.message_count + 1
        self.messages.append(message)
        self.message_count += 1
        self.last_message_timestamp = message.timestamp

    def update_title(self, title: str):
        """Update the conversation's title."""
        self.title = title

    def update_status(self, status: ConversationStatus):
        """Update the conversation's status."""
        self.status = status

    def add_response(self, response: Response):
        """Add a response to the last message in the conversation."""
        if self.messages and self.messages[-1].response is None:
            self.messages[-1].response = response
            for property_id in response.related_property_ids:
                if property_id not in self.related_property_ids:
                    self.related_property_ids.append(property_id)
