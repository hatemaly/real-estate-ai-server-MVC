# @title QuestionSuggestionSchema
# Define the Pydantic model for output validation
import os
from pydantic import Field
from enum import Enum
from typing import List, Dict, Any

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    AI = "ai"


class Message(BaseModel):
    role: Role = Field(
        ...,
        description="The role of the message sender (e.g., 'user' or 'assistant')"
    )
    content: str = Field(
        ...,
        description="The content of the message"
    )



class QuestionSuggestionSchema(BaseModel):
    questions: List[str] = Field(
        ...,
        description="List of relevant questions to suggest to the user based on chat history"
    )

class GoogleGenerativeChatQuestionSuggester:
    def _init_(self):
        # Initialize LLM model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # Using Gemini 1.5 Pro model
            temperature=0,  # Lower temperature for more consistent outputs
            max_output_tokens=300,  # Adjust as needed
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

        # Create output parser
        self.output_parser = PydanticOutputParser(pydantic_object=QuestionSuggestionSchema)


        self.company_context = """
        CBRE Group, Inc. is a global leader in the real estate services and investment industry,
        providing a wide range of services including property sales and leasing, property management,
        valuation, development services, investment management, and consulting.
        """

        # Define the prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["company_context","chat_history", "num_questions"],
            template="""
            Company Context: {company_context}

            Your task is to analyze the following chat history and suggest {num_questions} relevant
            follow-up questions that the user might be interested in asking next.

            The questions should:
            - Be directly related to topics discussed in the chat history
            - Expand on concepts mentioned but not fully explored
            - Help clarify any ambiguous points in the conversation
            - Suggest logical next steps in the conversation flow
            - Avoid redundancy with questions already asked

            Chat History:
            {chat_history}

            Generate exactly {num_questions} questions that would be most relevant and helpful
            based on this conversation history.

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

    def execute(self, chat_history: List[Message], num_questions: int = 3) -> Dict[str, Any]:
        """
        Generate question suggestions based on chat history.

        Args:
            chat_history: List of dictionaries with 'role' and 'content' keys
            num_questions: Number of questions to suggest (default: 3)

        Returns:
            Dictionary containing suggested questions
        """
        # Format chat history for prompt
        formatted_history = ""
        for message in chat_history:
            role = message.role.value.capitalize()
            content = message.content
            formatted_history += f"{role}: {content}\n\n"

        # Run the chain using invoke
        try:
            parsed_output = self.chain.invoke({
                "chat_history": formatted_history,
                "num_questions": num_questions,
                "company_context":self.company_context
            })
            return parsed_output.model_dump()
        except Exception as e:
            return {"questions": [], "error": str(e)}

    def get_suggestions(self, chat_history: List[Message], num_questions: int = 3) -> List[str]:
        """
        Convenience method that returns just the list of questions.
        """
        result = self.execute(chat_history, num_questions)
        return result.get("questions", [])

# example usage
chat_history = [
    Message(role=Role.USER,content="I'm looking to buy a house in downtown Seattle"),
]

questions = GoogleGenerativeChatQuestionSuggester().get_suggestions(chat_history=chat_history,num_questions=1)
print(f"{questions = }")