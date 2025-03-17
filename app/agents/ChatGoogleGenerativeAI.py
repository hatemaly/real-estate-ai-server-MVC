# @title ChatGoogleGenerativeAI Filter Agent.
import os
from pydantic import Field
from typing import Dict, Any

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel


class OutputSchema(BaseModel):
    is_real_estate_related: bool = Field(
        ...,
        description="Whether the message is related to real estate"
    )

class GoogleGenerativeRealEstateValidator:
    def _init_(self):
        # Initialize Google Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # Using Gemini 1.5 Pro model
            temperature=0,  # Lower temperature for more consistent outputs
            max_output_tokens=100,  # Adjust as needed
            google_api_key=os.getenv("GEMINI_API_KEY")
            )

        self.company_context = """
        CBRE Group, Inc. is a global leader in the real estate services and investment industry,
        providing a wide range of services including property sales and leasing, property management,
        valuation, development services, investment management, and consulting.
        """

        # Create output parser
        self.output_parser = PydanticOutputParser(pydantic_object=OutputSchema)

        # Define the prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["company_context", "user_message"],
            template="""
            Company Context: {company_context}

            Your task is to analyze if the following message is related to the real estate industry.
            Consider valid topics such as:
            - Property buying, selling, or renting
            - Real estate market analysis
            - Property development and investment
            - Mortgages and real estate financing
            - Property management and maintenance
            - Land development and zoning
            - Real estate agents and services
            - Need to consultation.

            User Message: {user_message}

            Return true only if the message is clearly related to real estate industry.
            Return false for all other topics or ambiguous cases.

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
        Validate if a message is related to real estate.
        """
        # Run the chain using invoke
        try:
            parsed_output = self.chain.invoke({
                "company_context": self.company_context,
                "user_message": user_message
            })
            return parsed_output.model_dump()
        except Exception as e:
            return {"is_real_estate_related": False, "error": str(e)}