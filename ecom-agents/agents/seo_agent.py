from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from repository.queries import get_product, get_review_insight

load_dotenv()

class ProductDescriptionOutput(BaseModel):
    title: str = Field(description="Product title for SEO")
    description: str = Field(description="Product description for SEO")
    keywords: list[str] = Field(description="List of keywords for SEO")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
structured_llm = llm.with_structured_output(ProductDescriptionOutput)

def run_seo_agent(product_id: int) -> dict:
    product = get_product(product_id)
    review_insight = get_review_insight(product_id)

    if review_insight is None:
        raise ValueError(f"No review insight for product {product_id}. Run the review agent first.")

    prompt = f"""You are an SEO expert for an e-commerce store.
            Product: {product['name']}
            Category: {product['category']}
            Base price: {product['base_price']}
            Features: {product['features']}

            What customers love: {', '.join(review_insight['praises'])}
            What customers complain about: {', '.join(review_insight['complaints'])}

            Generate a product title, description, and a list of keywords for SEO.
            Be concise and persuasive. Write about what customers love, and never invent features that aren't listed.
            Do not mention the complaints in the description, but do not make claims that contradict them."""
    
    result = structured_llm.invoke(prompt)
    
    return {
        "product_id": product_id,
        "title": result.title,
        "description": result.description,
        "keywords": result.keywords,
    }
