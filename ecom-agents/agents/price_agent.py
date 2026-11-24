from typing import Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from repository.queries import get_product, get_competitor_prices

load_dotenv()

class PriceRecommendationOutput(BaseModel):
    action: Literal["lower", "raise", "hold"]
    suggested_price: float = Field(description="New price in INR")
    reason: str = Field(description="One or two sentences explaining the decision")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
structured_llm = llm.with_structured_output(PriceRecommendationOutput)

def run_price_agent(product_id: int) -> dict:
    # 1. CODE: gather and calculate (no LLM needed for math)
    product = get_product(product_id)
    prices = [c["price"] for c in get_competitor_prices(product_id)]
    avg = round(sum(prices) / len(prices), 2)
    current = product["base_price"]
    

    # 2. LLM: judgment only
    prompt = f"""You are a pricing analyst for an e-commerce store.
                Product: {product['name']}
                Our price: {current}
                Competitor prices: {prices}
                Competitor average: {avg}
                Lowest competitor: {min(prices)}, highest: {max(prices)}

                Decide whether to lower, raise, or hold our price. Be conservative.
                Explain briefly."""
    result = structured_llm.invoke(prompt)

    # 3. CODE: guardrail. Never trust the LLM blindly with money
    low, high = current * 0.8, current * 1.2
    suggested = min(max(result.suggested_price, low), high)

    return {
        "product_id": product_id, "current": current, "avg": avg,
        "suggested": round(suggested, 2),
        "action": result.action, "reason": result.reason,
    }