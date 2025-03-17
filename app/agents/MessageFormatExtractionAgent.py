import os
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class CurrencyType(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    EGP = "EGP"

class PropertyType(str, Enum):
    APARTMENT = "apartment"
    VILLA = "villa"
    OFFICE = "office"


class UsageType(str, Enum):
    COMMERCIAL = "commercial"
    RESIDENTIAL = "residential"
    INDUSTRIAL = "industrial"


class FinishingType(str, Enum):
    FINISHED = "finished"
    SEMI_FINISHED = "semi_finished"
    UNFINISHED = "unfinished"

class OperationType(str, Enum):
    SEARCH = "search"               # Looking for property listings
    CONSULTATION = "consultation"   # General advice or market information


class PropertyStats(BaseModel):
    bedrooms: Optional[int] = Field(
        default=None,
        description="Number of bedrooms in the property"
    )
    bathrooms: Optional[int] = Field(
        default=None,
        description="Number of bathrooms in the property"
    )
    square_footage: Optional[int] = Field(
        default=None,
        description="Square footage of the property"
    )
    parking_spaces: Optional[int] = Field(
        default=None,
        description="Number of parking spaces in the property"
    )
    garden: Optional[bool] = Field(
        default=None,
        description="Whether the property has a garden"
    )
    swimming_pool: Optional[bool] = Field(
        default=None,
        description="Whether the property has a swimming pool"
    )



class PriceRange(BaseModel):
    min_price: Optional[float] = Field(
        default=None,
        description="Minimum price mentioned or lower bound of price range"
    )
    max_price: Optional[float] = Field(
        default=None,
        description="Maximum price mentioned or upper bound of price range"
    )
    currency: Optional[CurrencyType] = Field(
        default=CurrencyType.EGP,
        description="Currency of the price (USD, EUR, etc.)"
    )

class RealEstateExtractionsSchema(BaseModel):
    operation_type: OperationType = Field(
        default=OperationType.SEARCH,
        description="Type of operation (search or consultation)"
    )
    locations: List[str] = Field(
        default_factory=list,
        description="List of locations or geographic areas mentioned in the message"
    )
    developers: List[str] = Field(
        default_factory=list,
        description="List of real estate developers or development companies mentioned"
    )
    projects: List[str] = Field(
        default_factory=list,
        description="List of real estate projects, developments, or properties mentioned"
    )
    amenities: List[str] = Field(
        default_factory=list,
        description="List of amenities, facilities, or features of the properties mentioned"
    )
    price: PriceRange = Field(
        default_factory=PriceRange,
        description="Structured price information with min, max, and currency"
    )
    property_types: List[str] = Field(
        default_factory=list,
        description="Types of properties mentioned (apartment, villa, office space, etc.)"
    )
    property_stats: PropertyStats = Field(
        default_factory=PropertyStats,
        description="Property statistics such as square footage, number of bedrooms/bathrooms, etc."
    )
    refactored_message: Optional[str] = Field(
        None,
        description="The refactored version of the user message."
    )
    property_type: Optional[PropertyType] = Field(
        None,  # or provide a default value
        description="Type of property (apartment, villa, office)"
    )
    usage_type: Optional[UsageType] = Field(
        None,  # or provide a default value
        description="Usage classification of the property (commercial, residential, industrial)"
    )
    finishing_type: Optional[FinishingType] = Field(
        default=None,
        description="Level of finishing for the property (finished, semi-finished, unfinished)"
    )
    delivery_date: Optional[datetime] = Field(
        default=None,
        description="Expected or actual date of property delivery/completion"
    )



class MessageFormatExtractionAgent:
    def __init__(self):  # Fixed constructor syntax
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_output_tokens=100,
            google_api_key=os.getenv("GEMINI_API_KEY","AIzaSyBw2Z9hujaI2ay3-mdyQwklUWJ2pt-ho5g")
        )

        print(os.getenv("GEMINI_API_KEY"))

        self.company_context = """
        CBRE Group, Inc. is a global leader in the real estate services and investment industry,
        providing a wide range of services including property sales and leasing, property management,
        valuation, development services, investment management, and consulting.
        """

        # Create output parser
        self.output_parser = PydanticOutputParser(pydantic_object=RealEstateExtractionsSchema)

        # Define the prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["company_context", "user_message"],
            template="""
            Company Context: {company_context}

            Your task is to analyze the following user message in a real estate context and extract comprehensive information.

            User Message: {user_message}

            Extract the following elements:
            1. All locations or geographic areas (cities, neighborhoods, regions, countries, etc.)
            2. All real estate developers or development companies mentioned
            3. All real estate projects, developments, or properties referenced
            4. All amenities and features (pool, gym, parking, security, smart home features, etc.)
            5. All price points, price ranges, or financial terms (including rental rates, purchase prices, etc.)
            6. All property types mentioned (apartment, villa, office space, retail, mixed-use, etc.)
            7. Property statistics as key-value pairs (square footage, number of bedrooms/bathrooms, lot size, year built, etc.)

            Then, provide a refactored version of the message that is concise, clear, and optimized for vector store storage while retaining all essential information.

            For each category, provide an empty list if none are mentioned. Be precise and comprehensive in your extraction.
            For property_stats, return an empty dictionary if no statistics are mentioned.

            {format_instructions}
            """
        )

        # Create the chain using RunnablePassthrough
        self.chain = (
            RunnablePassthrough.assign(format_instructions=lambda _: self.output_parser.get_format_instructions())
            | self.prompt_template
            | self.llm
            | self.output_parser
        )

    def execute(self, user_message: str) -> Dict[str, Any]:
        """
        Refactor a user message into a new format suitable for vector store storage.
        """
        # Run the chain using invoke
        try:
            parsed_output = self.chain.invoke({
                "company_context": self.company_context,
                "user_message": user_message
            })
            return parsed_output.model_dump()
        except Exception as e:
            return {
                "locations": [],
                "developers": [],
                "projects": [],
                "amenities": [],
                "price_points": [],
                "property_types": [],
                "property_stats": {},
                "refactored_message": user_message,
                "error": str(e)
            }

ret = MessageFormatExtractionAgent().execute("I am looking to buy a new house in the suburbs with a budget from $500,000 to $1,000,000 with 200m")
print(ret)