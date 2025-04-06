# src/services/conversation_service.py
from datetime import datetime
from typing import List, Optional, Tuple
from uuid import UUID

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from pymongo import MongoClient

from app.DTOs.ConversationDTOs.conversationDTO import (
    AIMessageResponseDTO,
    UserMessageRequestDTO,
)
from app.agents.ChatGoogleGenerativeAI import GoogleGenerativeRealEstateValidator
from app.agents.MessageFormatExtractionAgent import MessageFormatExtractionAgent
from app.agents.ResidentialUnit import ResidentialUnit, ResidentialUnitRecommender
from app.agents.VectorDBWeaviate import VectorDBWeaviate
from app.models.conversation_models.conversation import Conversation, Message, Role, Response
from app.models.property_models.property import Property
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.developer_repository import DeveloperRepository
from app.repositories.location_repository import LocationRepository
from app.repositories.property_repository import PropertyRepository


class ConversationService:
    def __init__(self, repository: ConversationRepository,db: MongoClient):
        self.repository = repository
        self.db = db

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

    async def send_message(self, data: UserMessageRequestDTO) -> AIMessageResponseDTO:
        try:
            # Validate message relevance
            await self._validate_message_relevance(data.content)

            # Extract entities from message
            locations, developers, projects = await self._extract_entities(data.content)

            # Get IDs from vector DB
            location_ids, developer_ids, project_ids = await self._get_vector_db_ids(locations, developers, projects)

            # Query properties
            properties = await self._query_properties(location_ids, developer_ids, project_ids)

            # Convert to ResidentialUnits with proper data resolution
            residential_units = await self._convert_properties_to_units(properties)

            # Get recommendations
            recommendation = await self._get_recommendation(residential_units, data.content)
            best_match, related_properties = await self._process_recommendation(recommendation)

            # Update conversation
            conversation = await self._update_conversation(data, best_match, related_properties, recommendation)

            return self._create_response(conversation, recommendation, related_properties, best_match)

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    # region Helper Methods

    async def _validate_message_relevance(self, content: str):
        """Validate if message is real estate related"""
        try:
            validator = GoogleGenerativeRealEstateValidator()
            ret = validator.execute(content)
            if not ret.get("is_real_estate_related", False):
                raise HTTPException(
                    status_code=400,
                    detail={"message": "This message is not related to real estate content."}
                )
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"Validation service unavailable: {str(e)}"
            )

    async def _extract_entities(self, content: str) -> Tuple[List[str], List[str], List[str]]:
        """Extract location, developer, and project entities from message"""
        try:
            extracted_data = MessageFormatExtractionAgent().execute(content)
            return (
                extracted_data.get("locations", []),
                extracted_data.get("developers", []),
                extracted_data.get("projects", [])
            )
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Failed to extract entities: {str(e)}"
            )

    async def _get_vector_db_ids(self, locations: List[str], developers: List[str], projects: List[str]) -> Tuple[
        List[str], List[str], List[str]]:
        """Convert entity names to database IDs using vector search"""
        try:
            vs = VectorDBWeaviate()
            if not vs.connect():
                raise ConnectionError("Failed to connect to VectorDB")

            return (
                vs.retrieve_location_ids(locations) if locations else [],
                vs.retrieve_developer_ids(developers) if developers else [],
                vs.retrieve_project_ids(projects) if projects else []
            )
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"VectorDB service error: {str(e)}"
            )

    async def _query_properties(self, location_ids: List[str], developer_ids: List[str], project_ids: List[str]) -> \
    List[Property]:
        """Query properties from repository with error handling"""
        try:
            property_repo = PropertyRepository(self.db.properties)
            result = await property_repo.get_properties_by_criteria(
                locations_ids=location_ids,
                developers_ids=developer_ids,
                projects_ids=project_ids,
                page=1,
                page_size=10
            )
            return result.get("properties", [])
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Property query failed: {str(e)}"
            )

    async def _convert_properties_to_units(self, properties: List[Property]) -> List[ResidentialUnit]:
        """Convert Property objects to ResidentialUnit schema with data resolution"""
        units = []
        for prop in properties:
            try:
                current_price = await self._get_current_price(prop)
                location_names = await self._resolve_location_names(
                    prop.detailed_property_details.location_ids
                ) if prop.detailed_property_details else []

                developer_names = await self._resolve_developer_names(
                    prop.basic_property_details.developer_ids
                ) if prop.basic_property_details else []

                units.append(ResidentialUnit(
                    id=str(prop.id),
                    location=", ".join(location_names),
                    developer=", ".join(developer_names),
                    price=current_price,
                    bedrooms=prop.detailed_property_details.bedrooms if prop.detailed_property_details else 0,
                    bathrooms=prop.detailed_property_details.bathrooms if prop.detailed_property_details else 0,
                    amenities=[a.name for a in prop.detailed_property_details.amenities]
                    if prop.detailed_property_details else [],
                    distance_to_city_center=prop.detailed_property_details.distance_to_city_center
                    if prop.detailed_property_details else 0.0
                ))
            except Exception as e:
                # Skip invalid properties but log the error
                print(f"Error converting property {prop.id}: {str(e)}")
                continue
        return units

    async def _get_current_price(self, prop: Property) -> float:
        """Get current price with fallback to latest price"""
        try:
            price_history = prop.background_property_details.price_history
            current_idx = prop.background_property_details.current_price

            if not price_history:
                return 0.0

            if current_idx is None or current_idx >= len(price_history):
                return price_history[-1].amount

            return price_history[current_idx].amount
        except (AttributeError, IndexError):
            return 0.0

    async def _resolve_location_names(self, location_ids: List[str]) -> List[str]:
        """Resolve location IDs to names"""
        try:
            if not location_ids:
                return []

            location_repo = LocationRepository(self.db.locations)
            locations = await location_repo.get_locations_by_ids(location_ids)
            return [loc.name for loc in locations if loc.name]
        except Exception as e:
            print(f"Location resolution error: {str(e)}")
            return []

    async def _resolve_developer_names(self, developer_ids: List[str]) -> List[str]:
        """Resolve developer IDs to names"""
        try:
            if not developer_ids:
                return []

            developer_repo = DeveloperRepository(self.db.developers)
            developers = await developer_repo.get_developers_by_ids(developer_ids)
            return [dev.name for dev in developers if dev.name]
        except Exception as e:
            print(f"Developer resolution error: {str(e)}")
            return []

    async def _get_recommendation(self, units: List[ResidentialUnit], content: str) -> dict:
        """Get recommendation from AI model"""
        try:
            recommender = ResidentialUnitRecommender(residential_units=units)
            return recommender.recommend(content) or {}
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Recommendation failed: {str(e)}"
            )

    async def _process_recommendation(self, recommendation: dict) -> Tuple[Optional[Property], List[Property]]:
        """Process recommendation results"""
        try:
            best_match_id = recommendation.get("best_match_unit_id")
            if not best_match_id:
                return None, []

            property_repo = PropertyRepository(self.db.properties)
            best_match = await property_repo.get_property_by_id(best_match_id)
            if not best_match:
                return None, []

            related_properties = await property_repo.get_related_properties(
                property_id=best_match_id,
                developer_ids=best_match.basic_property_details.developer_ids if best_match.basic_property_details else [],
                location_ids=best_match.detailed_property_details.location_ids if best_match.detailed_property_details else [],
                limit=3
            )
            return best_match, related_properties
        except Exception as e:
            print(f"Recommendation processing error: {str(e)}")
            return None, []

    async def _update_conversation(self, data: UserMessageRequestDTO, best_match: Optional[Property],
                                   related_properties: List[Property], recommendation: dict) -> Conversation:
        """Update conversation history"""
        try:
            conversation = await self._get_conversation(data.conversation_id)

            user_message = Message(
                content=data.content,
                timestamp=datetime.now(),
                role=Role.USER
            )

            ai_response = Response(
                content="\n".join(recommendation.get("match_reasons", ["Best matches based on your criteria"])),
                related_property_ids=[p.id for p in related_properties],
                best_property_id=best_match.id if best_match else None,
                role=Role.ASSISTANT
            )

            conversation.add_message(user_message)
            conversation.add_response(ai_response)

            await self._save_conversation(conversation)
            return conversation
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Conversation update failed: {str(e)}"
            )

    async def _get_conversation(self, conversation_id: str) -> Conversation:
        """Get conversation with proper error handling"""
        try:
            doc = await self.db.conversations.find_one({"_id": ObjectId(conversation_id)})
            if not doc:
                raise HTTPException(status_code=404,
                                    detail="Conversation not found")  # Fixed typo HTTException->HTTPException
            return Conversation(**self._convert_object_ids(doc))  # Fixed model initialization
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid conversation ID format")  # Fixed exception name

    async def _save_conversation(self, conversation: Conversation):
        """Save conversation state"""
        try:
            await self.db.conversations.replace_one(  # Fixed method chain
                {"_id": ObjectId(conversation.id)},
                self._convert_object_ids(conversation.dict(exclude={"id"}))  # Fixed method name and syntax
            )
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid conversation ID format")

    def _convert_object_ids(self, data: dict) -> dict:
        """Recursively convert string IDs to ObjectIds"""
        if isinstance(data, list):
            return [self._convert_object_ids(item) for item in data]
        if isinstance(data, dict):
            for key, value in data.items():
                if key.endswith('_id') or key.endswith('_ids'):
                    if isinstance(value, list):
                        data[key] = [ObjectId(v) if isinstance(v, str) and len(v) == 24 else v for v in value]
                    elif isinstance(value, str) and len(value) == 24:
                        try:
                            data[key] = ObjectId(value)
                        except InvalidId:
                            pass
                else:
                    data[key] = self._convert_object_ids(value)
        return data

    def _convert_object_ids(self, data: dict) -> dict:
        """Recursively convert string IDs to ObjectIds"""
        if isinstance(data, list):
            return [self._convert_object_ids(item) for item in data]
        if isinstance(data, dict):
            for key, value in data.items():
                if key.endswith('_id') or key.endswith('_ids'):
                    if isinstance(value, list):
                        data[key] = [ObjectId(v) if isinstance(v, str) and len(v) == 24 else v for v in value]
                    elif isinstance(value, str) and len(value) == 24:
                        try:
                            data[key] = ObjectId(value)
                        except InvalidId:
                            pass
                else:
                    data[key] = self._convert_object_ids(value)
        return data

    def _create_response(self, conversation: Conversation, recommendation: dict,
                         related_properties: List[Property], best_match: Optional[Property]) -> AIMessageResponseDTO:
        """Create final response DTO"""
        return AIMessageResponseDTO(
            _id=str(conversation.messages[-1].id) if conversation.messages else None,
            content="\n".join(recommendation.get("match_reasons", ["Here are some matching properties"])),
            related_properties=related_properties,
            best_property=best_match,
        )
