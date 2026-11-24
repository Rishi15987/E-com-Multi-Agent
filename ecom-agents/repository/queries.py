from db.session import SessionLocal
from db.models import ProductDescription, Review, CompetitorPrice, ReviewInsight, Product, PriceRecommendation

# READ methods
def get_reviews(product_id: int, limit: int = 50) -> list[dict]:
    with SessionLocal() as s:
        rows = s.query(Review).filter(Review.product_id == product_id).limit(limit).all()
        return [{"rating": r.rating, "text": r.text} for r in rows]

def get_competitor_prices(product_id: int) -> list[dict]:
    with SessionLocal() as s:
        rows = s.query(CompetitorPrice).filter(CompetitorPrice.product_id == product_id).all()
        return [{"competitor": r.competitor_name, "price": float(r.price)} for r in rows]

# WRITE method (the agent's output)
def save_review_insight(product_id: int, score: float, praises: list[str], complaints: list[str]):
    with SessionLocal() as s:
        s.add(ReviewInsight(product_id=product_id, sentiment_score=score,
                            top_praises=praises, top_complaints=complaints))
        s.commit()

def get_product(product_id: int) -> dict:
    with SessionLocal() as s:
        p = s.get(Product, product_id)
        return {"id": p.id, "name": p.name, "category": p.category,
                "base_price": float(p.base_price), "features": p.features}

def save_price_recommendation(product_id: int, current: float, avg: float, suggested: float, action: str, reason: str):
    with SessionLocal() as s:
        s.add(PriceRecommendation(
            product_id=product_id, current_price=current, competitor_avg=avg,
            suggested_price=suggested, action=action, reason=reason))
        s.commit()

def get_review_insight(product_id: int) -> dict | None:
    with SessionLocal() as s:
        r = (s.query(ReviewInsight)
               .filter(ReviewInsight.product_id == product_id)
               .order_by(ReviewInsight.created_at.desc())
               .first())
        if r is None:
            return None
        return {"praises": r.top_praises, "complaints": r.top_complaints,
                "sentiment": float(r.sentiment_score)}

def save_description(product_id, title, description, keywords):
    with SessionLocal() as s:
        s.add(ProductDescription(product_id=product_id, title=title,
                                 description=description, keywords=keywords))
        s.commit()

def get_product_description(product_id: int) -> dict | None:
    with SessionLocal() as s:
        d = (s.query(ProductDescription)
               .filter(ProductDescription.product_id == product_id)
               .order_by(ProductDescription.created_at.desc())
               .first())
        if d is None:
            return None
        return {"title": d.title, "description": d.description, "keywords": d.keywords}

def get_price_recommendation(product_id: int) -> dict | None:
    with SessionLocal() as s:
        p = (s.query(PriceRecommendation)
               .filter(PriceRecommendation.product_id == product_id)
               .order_by(PriceRecommendation.created_at.desc())
               .first())
        if p is None:
            return None
        return {"current": float(p.current_price), "avg": float(p.competitor_avg),
                "suggested": float(p.suggested_price), "action": p.action, "reason": p.reason}