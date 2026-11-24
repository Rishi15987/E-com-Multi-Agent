from dotenv import load_dotenv
from typing import Literal
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from repository.queries import get_product, get_review_insight, get_product_description, get_price_recommendation

load_dotenv()

class ProductCampaignOutput(BaseModel):
    channel: Literal["email", "instagram", "google_ads"]
    audience: str = Field(description="Target audience for the campaign")
    headline: str = Field(description="Catchy headline for the campaign")
    body: str = Field(description="Body text for the campaign")
    call_to_action: str = Field(description="Call to action for the campaign")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
structured_llm = llm.with_structured_output(ProductCampaignOutput)

def run_marketing_agent(product_id: int) -> dict:
    product = get_product(product_id)
    review_insight = get_review_insight(product_id)
    product_description = get_product_description(product_id)
    price_recommendation = get_price_recommendation(product_id)

    if review_insight is None:
        raise ValueError(f"No review insight for product {product_id}. Run the review agent first.")
    if product_description is None:
        raise ValueError(f"No product description for product {product_id}. Run the SEO agent first.")
    if price_recommendation is None:
        raise ValueError(f"No price recommendation for product {product_id}. Run the pricing agent first.")

    prompt = f"""You are a marketing expert for an e-commerce store.
            Product: {product['name']}
            Category: {product['category']}
            Base price: {product['base_price']}
            suggested price: {price_recommendation['suggested']}
            Features: {product['features']}

            What customers love: {', '.join(review_insight['praises'])}
            What customers complain about: {', '.join(review_insight['complaints'])}

            Product title: {product_description['title']}
            Product description: {product_description['description']}
            Keywords: {', '.join(product_description['keywords'])}

            Generate a marketing campaign for this product. Choose one channel from email, instagram, or google_ads.
            Write a catchy headline, body text, and a call to action. Be persuasive and concise."""
    
    result = structured_llm.invoke(prompt)
    
    return {
        "product_id": product_id,
        "channel": result.channel,
        "audience": result.audience,
        "headline": result.headline,
        "body": result.body,
        "call_to_action": result.call_to_action,
    }