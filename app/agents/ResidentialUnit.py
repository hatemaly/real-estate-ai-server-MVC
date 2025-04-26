# @title Reasoner agent.
import os
from pydantic import Field
from typing import List, Dict, Any

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel


class ResidentialUnit(BaseModel):
    id: str
    location: str
    developer: str
    price: float
    bedrooms: int
    bathrooms: int
    amenities: List[str]
    distance_to_city_center: float


class RecommendationOutput(BaseModel):
    best_match_unit_id: str = Field(
        ...,
        description="The ID of the residential unit that best matches the user's context",
    )
    reason: str = Field(
        ..., description="Detailed reasons why this unit is the best match for the user"
    )


class ResidentialUnitRecommender:
    def __init__(self, residential_units: List[ResidentialUnit]):
        # Initialize Anthropic Claude model
        self.llm = self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # Using Gemini 1.5 Pro model
            temperature=0,  # Lower temperature for more consistent outputs
            max_output_tokens=500,  # Adjust as needed
            google_api_key=os.getenv("GEMINI_API_KEY"),
        )

        # Store residential units
        self.residential_units = residential_units

        # Create output parser
        self.output_parser = PydanticOutputParser(pydantic_object=RecommendationOutput)

        # Define the prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["residential_units", "user_context"],
            template="""
            Available Residential Units:
            {residential_units}

            User Context: {user_context}

            Task: Analyze the list of residential units and identify the BEST MATCH for the user based on their specific context.

            Evaluation Criteria:
            1. Relevance to user's needs and preferences
            2. Price compatibility
            3. Location suitability
            4. Amenities
            5. Potential for future value

            Provide:
            - The ID of the best matching unit
            - Detailed reasons for the recommendation

            {format_instructions}
            """,
        )

        # Create the recommendation chain
        self.chain = self.prompt_template | self.llm | self.output_parser

    def recommend(self, user_context: str) -> Dict[str, Any]:
        """
        Recommend the best residential unit based on user context.

        Args:
            user_context (str): Detailed description of user's requirements and preferences

        Returns:
            Dict containing recommended unit ID and match reason
        """
        # Convert residential units to a readable format
        units_str = "\n".join(
            [
                f"ID: {unit.id}, Location: {unit.location}, Developer: {unit.developer}, "
                f"Price: ${unit.price:,.2f}, Bedrooms: {unit.bedrooms}, "
                f"Bathrooms: {unit.bathrooms}, Amenities: {', '.join(unit.amenities)}, "
                f"Distance to City Center: {unit.distance_to_city_center} km"
                for unit in self.residential_units
            ]
        )

        try:
            # Invoke the recommendation chain
            recommendation = self.chain.invoke(
                {
                    "residential_units": units_str,
                    "user_context": user_context,
                    "format_instructions": self.output_parser.get_format_instructions(),
                }
            )
            return recommendation.model_dump()
        except Exception as e:
            return {
                "best_match_unit_id": None,
                "match_reasons": [f"Error in recommendation: {str(e)}"],
            }


# # Example usage
# residential_units = [
#     ResidentialUnit(
#         id="RU001",
#         location="Suburban Oaks, Maple Street",
#         developer="GreenField Homes",
#         price=450000,
#         bedrooms=3,
#         bathrooms=2,
#         amenities=["Gym", "Swimming Pool", "Playground"],
#         distance_to_city_center=15,
#     ),
#     ResidentialUnit(
#         id="RU002",
#         location="Urban Lofts, Downtown",
#         developer="MetroLiving Developers",
#         price=600000,
#         bedrooms=2,
#         bathrooms=2,
#         amenities=["Rooftop Terrace", "Concierge", "Smart Home Features"],
#         distance_to_city_center=2,
#     ),
# ]

# recommender = ResidentialUnitRecommender(residential_units)

# # Example recommendation
# user_context = "I'm a young professional looking for a modern apartment close to the city center with amenities for an active lifestyle"
# recommendation = recommender.recommend(user_context)
# print(f"Best Match Unit ID: {recommendation['best_match_unit_id']}")
# print("Match Reasons:")
# print(f"{recommendation['reason']}")
