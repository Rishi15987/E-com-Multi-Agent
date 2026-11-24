from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from repository.queries import get_reviews

load_dotenv()

# What the agent must return (like a DTO)
class ReviewInsightOutput(BaseModel):
    sentiment_score: float = Field(description="0.0 = very negative, 1.0 = very positive")
    top_praises: list[str] = Field(description="Top 3 things customers like")
    top_complaints: list[str] = Field(description="Top 3 things customers complain about")

# The bridge: LLM can call this
@tool
def fetch_reviews(product_id: int) -> list[dict]:
    """Fetch customer reviews (rating and text) for a product by its id."""
    return get_reviews(product_id)

agent = create_agent(
    model=ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0),
    tools=[fetch_reviews],
    system_prompt=(
        "You are a review analyst for an e-commerce store. "
        "Always fetch the reviews first, then analyze them. "
        "Identify the top 3 praises and top 3 complaints and give a sentiment score."
    ),
    response_format=ReviewInsightOutput,
)

def run_review_agent(product_id: int) -> ReviewInsightOutput:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"Analyze the reviews for product {product_id}."}]}
    )
    return result["structured_response"]