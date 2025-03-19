# src/services/conversation_service.py
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from app.DTOs.ConversationDTOs.conversationDTO import (
    AIMessageResponseDTO,
    UserMessageRequestDTO,
)
from app.agents.ChatGoogleGenerativeAI import GoogleGenerativeRealEstateValidator
from app.agents.MessageFormatExtractionAgent import MessageFormatExtractionAgent
from app.agents.ResidentialUnit import ResidentialUnit, ResidentialUnitRecommender
from app.agents.VectorDBWeaviate import VectorDBWeaviate
from app.models.conversation_models.conversation import Conversation
from app.models.property_models.property import Property
from app.repositories.conversation_repository import ConversationRepository


class ConversationService:
    def __init__(self, repository: ConversationRepository):
        self.repository = repository

    async def create_conversation(self, conversation: Conversation) -> Conversation:
        await self.repository.save(conversation)
        return conversation

    async def update_conversation(self, conversation: Conversation) -> Conversation:
        await self.repository.update(conversation)
        return conversation

    async def delete_conversation(self, conversation_id: str) -> None:
        await self.repository.delete(conversation_id)

    async def get_conversation_by_id(
        self, conversation_id: str
    ) -> Optional[Conversation]:
        return await self.repository.get_by_id(conversation_id)

    async def get_conversation_history(
        self, conversation_id: str, limit: int = 10, offset: int = 0
    ) -> Conversation:
        return await self.repository.retrieve_conversation_history_by_id(
            conversation_id, limit, offset
        )

    async def get_conversations_by_user_id(self, user_id: str) -> List[Conversation]:
        return await self.repository.retrieve_conversation_info_by_user_id(user_id)

    async def send_message(self, data: UserMessageRequestDTO):
        validator_agent = GoogleGenerativeRealEstateValidator()
        ret = validator_agent.execute(data.content)
        is_real_estate_related: bool = ret["is_real_estate_related"]

        if not is_real_estate_related:
            raise HTTPException(
                status_code=400,
                detail={"message": "This message does not related to website content."},
            )

        extracted_data = MessageFormatExtractionAgent().execute(data.content)
        locations = extracted_data["locations"]
        developers = extracted_data["developers"]
        projects = extracted_data["projects"]

        vs = VectorDBWeaviate()
        vs.connect()

        locations_ids: list[str] = vs.retrieve_location_ids(locations)
        developers_ids: list[str] = vs.retrieve_developer_ids(developers)
        projects_ids: list[str] = vs.retrieve_project_ids(projects)

        # هنا يرقد الداتا بيز ^_^

        residential_units: List[ResidentialUnit] = (
            []
        )  # this list will come from mongoDB query then convert to 'ResidentialUnit' schema

        recommender = ResidentialUnitRecommender(residential_units=residential_units)
        recommendation = recommender.recommend(data.content)

        best_match_unit_id = recommendation["best_match_unit_id"]

        match_reasons = recommendation["match_reasons"]

        related_properties: list[Property] = []
        best_match_unit: Property | None = (
            None  # update 'None' with best match property by 'best_match_unit_id' but as object 'Property'.
        )

        # هنا يرقد الداتا بيز ^_^
        # TODO: Some queries required.
        # add the new response message into the conversation.
        # add the properties to the conversation.
        # update the last properties in the conversation with 'related_properties'.

        return AIMessageResponseDTO(
            _id=None,  # replace it with the new id coming from mongoDB.
            content="\n".join(match_reasons),
            related_properties=related_properties,
            best_property=best_match_unit,
        )
