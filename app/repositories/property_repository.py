# src/repositories/property_repository.py
from bson import ObjectId
from pymongo.collection import Collection
from typing import List, Optional, Any

from pymongo.results import UpdateResult
from pyparsing import Dict

from app.models.property_models.payment_plan import PaymentPlan
from app.models.property_models.price import Price
from app.models.property_models.property import Property, BackOfficePropertyDetails, PropertyType
from app.repositories.base_repository import BaseRepository


class PropertyRepository(BaseRepository):
    def __init__(self, collection: Collection):
        super().__init__(collection, Property)

    async def get_all_ids(self) -> List[str]:
        cursor = self.collection.find({}, {"_id": 1})
        return [doc["_id"] for doc in await cursor.to_list(length=None)]

    async def get_active_properties_ids(self) -> List[str]:
        cursor = self.collection.find({"is_active": True}, {"_id": 1})
        return [doc["_id"] for doc in await cursor.to_list(length=None)]




    # Core CRUD Operations

    # Price Management
    async def add_price(self, property_id: str, price: dict) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {
                "$push": {"background_property_details.price_history": price},
                "$inc": {"background_property_details.number_of_prices": 1}
            }
        )

    async def update_price(self, property_id: str, price_index: int, price: dict) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {f"background_property_details.price_history.{price_index}": price}}
        )

    async def activate_price(self, property_id: str, price_index: int) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {f"background_property_details.price_history.{price_index}.is_active": True}}
        )

    async def deactivate_price(self, property_id: str, price_index: int) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {f"background_property_details.price_history.{price_index}.is_active": False}}
        )

    # Payment Plan Management
    async def add_price_payment_plan(self, property_id: str, price_index: int, payment_plan: dict) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {
                "$push": {f"background_property_details.price_history.{price_index}.payment_plans": payment_plan},
                "$inc": {f"background_property_details.price_history.{price_index}.payment_plans_count": 1}
            }
        )

    async def update_price_payment_plan(self, property_id: str, price_index: int, plan_index: int, payment_plan: dict) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {f"background_property_details.price_history.{price_index}.payment_plans.{plan_index}": payment_plan}}
        )

    async def activate_price_payment_plan(self, property_id: str, price_index: int, plan_index: int) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {f"background_property_details.price_history.{price_index}.payment_plans.{plan_index}.is_active": True}}
        )

    async def deactivate_price_payment_plan(self, property_id: str, price_index: int, plan_index: int) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {f"background_property_details.price_history.{price_index}.payment_plans.{plan_index}.is_active": False}}
        )

    # Current Price and Highlighted Payment Plan
    async def set_current_price(self, property_id: str, price_index: int) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {"background_property_details.current_price": price_index}}
        )

    async def set_highlighted_payment_plan(self, property_id: str, price_index: int, plan_index: int) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {f"background_property_details.price_history.{price_index}.highlighted_payment_plan": plan_index}}
        )

    # Broker Management
    async def add_broker(self, property_id: str, broker_id: str) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$addToSet": {"background_property_details.brokers": broker_id}}
        )

    async def remove_broker(self, property_id: str, broker_id: str) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$pull": {"background_property_details.brokers": broker_id}}
        )

    # Property Activation
    async def activate_property(self, property_id: str) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {"background_property_details.is_active": True}}
        )

    async def deactivate_property(self, property_id: str) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {"background_property_details.is_active": False}}
        )

    # Property Information Updates
    async def update_basic_info(self, property_id: str, basic_info: dict) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {"basic_property_details": basic_info}}
        )

    async def update_detailed_info(self, property_id: str, detailed_info: dict) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {"detailed_property_details": detailed_info}}
        )

    async def update_background_info(self, property_id: str, background_info: dict) -> UpdateResult:
        return await self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {"background_property_details": background_info}}
        )

    # Query Methods
    async def get_properties_by_status(self, is_active: bool) -> List[dict]:
        return await self.collection.find({"background_property_details.is_active": is_active}).to_list(None)

    async def get_properties_with_active_prices(self) -> List[dict]:
        return await self.collection.find({
            "background_property_details.price_history.is_active": True
        }).to_list(None)

    async def get_properties_by_broker(self, broker_id: str) -> List[dict]:
        return await self.collection.find({
            "background_property_details.brokers": broker_id
        }).to_list(None)

    async def get_properties_by_price_range(self, min_price: float, max_price: float) -> List[dict]:
        return await self.collection.find({
            "background_property_details.current_price.amount": {
                "$gte": min_price,
                "$lte": max_price
            }
        }).to_list(None)

    async def get_properties_by_criteria(
            self,
            locations_ids: List[str] = None,
            developers_ids: List[str] = None,
            projects_ids: List[str] = None,
            page: int = 1,
            page_size: int = 10
    ) -> dict[str, int | list[Property] | Any]:
        """
        Query properties from MongoDB based on location, developer, and project IDs with pagination.

        Args:
            locations_ids: List of location IDs to filter by
            developers_ids: List of developer IDs to filter by
            projects_ids: List of project IDs to filter by
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            Dictionary with properties, total count, and pagination info
        """
        # Calculate skip value for pagination
        skip = (page - 1) * page_size

        # Build the filter query
        filter_query = {"background_property_details.is_active": True}

        if locations_ids:
            filter_query["detailed_property_details.location_ids"] = {"$in": [ObjectId(lid) for lid in locations_ids]}

        if developers_ids:
            filter_query["basic_property_details.developer_ids"] = {"$in": [ObjectId(did) for did in developers_ids]}

        if projects_ids:
            filter_query["basic_property_details.parent_project_id"] = {"$in": [ObjectId(pid) for pid in projects_ids]}

        # Get total count for pagination
        total_count = await self.collection.count_documents(filter_query)

        # Execute the query with pagination
        cursor = self.collection.find(filter_query).skip(skip).limit(page_size)

        # Convert documents to Property models
        properties = []
        async for doc in cursor:
            # Convert _id to string
            doc["_id"] = str(doc["_id"])
            # Convert other ObjectId fields to strings
            if "basic_property_details" in doc and "developer_ids" in doc["basic_property_details"]:
                doc["basic_property_details"]["developer_ids"] = [
                    str(did) for did in doc["basic_property_details"]["developer_ids"]
                ]
            if "detailed_property_details" in doc and "location_ids" in doc["detailed_property_details"]:
                doc["detailed_property_details"]["location_ids"] = [
                    str(lid) for lid in doc["detailed_property_details"]["location_ids"]
                ]
            # Add to list
            properties.append(Property(**doc))

        return {
            "properties": properties,
            "total": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": (total_count + page_size - 1) // page_size
        }

    async def get_property_by_id(self, property_id: str) -> Optional[Property]:
        """
        Get a property by its ID and convert it to a Property model
        """
        doc = await self.collection.find_one({"_id": ObjectId(property_id)})
        if not doc:
            return None

        # Convert _id to string
        doc["_id"] = str(doc["_id"])
        # Convert other ObjectId fields to strings
        if "basic_property_details" in doc and "developer_ids" in doc["basic_property_details"]:
            doc["basic_property_details"]["developer_ids"] = [
                str(did) for did in doc["basic_property_details"]["developer_ids"]
            ]
        if "detailed_property_details" in doc and "location_ids" in doc["detailed_property_details"]:
            doc["detailed_property_details"]["location_ids"] = [
                str(lid) for lid in doc["detailed_property_details"]["location_ids"]
            ]

        return Property(**doc)

    async def get_related_properties(
            self,
            property_id: str,
            developer_ids: List[str] = None,
            location_ids: List[str] = None,
            limit: int = 3
    ) -> List[Property]:
        """
        Get related properties based on the same developer or location,
        excluding the provided property_id
        """
        filter_query = {
            "_id": {"$ne": ObjectId(property_id)},
            "background_property_details.is_active": True
        }

        # Add developer or location filter if provided
        query_conditions = []
        if developer_ids:
            query_conditions.append({
                "basic_property_details.developer_ids": {
                    "$in": [ObjectId(did) for did in developer_ids]
                }
            })

        if location_ids:
            query_conditions.append({
                "detailed_property_details.location_ids": {
                    "$in": [ObjectId(lid) for lid in location_ids]
                }
            })

        # Combine conditions with $or if both are provided
        if query_conditions:
            filter_query["$or"] = query_conditions

        cursor = self.collection.find(filter_query).limit(limit)

        properties = []
        async for doc in cursor:
            # Convert _id to string
            doc["_id"] = str(doc["_id"])
            # Convert other ObjectId fields to strings
            if "basic_property_details" in doc and "developer_ids" in doc["basic_property_details"]:
                doc["basic_property_details"]["developer_ids"] = [
                    str(did) for did in doc["basic_property_details"]["developer_ids"]
                ]
            if "detailed_property_details" in doc and "location_ids" in doc["detailed_property_details"]:
                doc["detailed_property_details"]["location_ids"] = [
                    str(lid) for lid in doc["detailed_property_details"]["location_ids"]
                ]
            # Add to list
            properties.append(Property(**doc))

        return properties