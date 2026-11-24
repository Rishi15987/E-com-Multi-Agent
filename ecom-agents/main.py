from agents.review_agents import run_review_agent
from agents.price_agent import run_price_agent
from agents.seo_agent import run_seo_agent
from repository.queries import save_review_insight, save_price_recommendation, save_description

def main():
    product_id = 10

    insight = run_review_agent(product_id)
    save_review_insight(product_id, insight.sentiment_score,
                        insight.top_praises, insight.top_complaints)

    p = run_price_agent(product_id)
    print(p)
    save_price_recommendation(p["product_id"], p["current"], p["avg"],
                              p["suggested"], p["action"], p["reason"])

    d = run_seo_agent(product_id)
    print(d)
    save_description(d["product_id"], d["title"], d["description"], d["keywords"])

if __name__ == "__main__":
    main()