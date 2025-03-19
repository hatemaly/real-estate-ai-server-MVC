from fastapi import APIRouter, Depends
from typing import List
from app.DTOs.ConversationDTOs.conversationDTO import UserMessageRequestDTO
from app.controllers.conversation_controller import ConversationController
from app.database.collections import get_conversation_collection
from app.repositories.conversation_repository import ConversationRepository
from app.services.conversation_service import ConversationService
from app.models.conversation_models.conversation import Conversation, ConversationStatus

router = APIRouter()


# Dependency to get the ConversationController
async def get_conversation_controller() -> ConversationController:
    conversation_collection = await get_conversation_collection()
    repository = ConversationRepository(conversation_collection)
    service = ConversationService(repository)
    return ConversationController(service)


# Create a new conversation
@router.post("/", response_model=Conversation)
async def create_conversation(
    conversation: Conversation,
    controller: ConversationController = Depends(get_conversation_controller),
):
    return await controller.create_conversation(conversation)


# Get a conversation by ID
@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: str,
    controller: ConversationController = Depends(get_conversation_controller),
):
    print(conversation_id)
    return await controller.get_conversation(conversation_id)


# Get all conversations for a specific user
@router.get("/user/{user_id}", response_model=List[Conversation])
async def get_conversations_by_user(
    user_id: str,
    controller: ConversationController = Depends(get_conversation_controller),
):
    return await controller.get_conversations_by_user(user_id)


# Update a conversation
@router.put("/{conversation_id}", response_model=Conversation)
async def update_conversation(
    conversation_id: str,
    conversation: Conversation,
    controller: ConversationController = Depends(get_conversation_controller),
):
    return await controller.update_conversation(conversation_id, conversation)


# Delete a conversation
@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    controller: ConversationController = Depends(get_conversation_controller),
):
    await controller.delete_conversation(conversation_id)
    return {"message": "Conversation deleted successfully"}


# Get conversations by status
@router.get("/status/{status}", response_model=List[Conversation])
async def get_conversations_by_status(
    status: ConversationStatus,
    controller: ConversationController = Depends(get_conversation_controller),
):
    return await controller.get_conversations_by_status(status)


@router.post("/{conversation_id}")
async def send_message(
    data: UserMessageRequestDTO,
    controller: ConversationController = Depends(get_conversation_controller),
):
    return await controller.send_message(data)
