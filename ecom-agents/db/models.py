from sqlalchemy import String, Text, Numeric, Integer, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(100))
    base_price: Mapped[float] = mapped_column(Numeric(10, 2))
    features: Mapped[str] = mapped_column(Text)

class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    rating: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)

class CompetitorPrice(Base):
    __tablename__ = "competitor_prices"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    competitor_name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Numeric(10, 2))

# agent OUTPUT table
class ReviewInsight(Base):
    __tablename__ = "review_insights"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    sentiment_score: Mapped[float] = mapped_column(Numeric(3, 2))
    top_praises: Mapped[list[str]] = mapped_column(ARRAY(String))
    top_complaints: Mapped[list[str]] = mapped_column(ARRAY(String))
    created_at = mapped_column(DateTime, server_default=func.now())

class PriceRecommendation(Base):
    __tablename__ = "price_recommendations"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    current_price: Mapped[float] = mapped_column(Numeric(10, 2))
    competitor_avg: Mapped[float] = mapped_column(Numeric(10, 2))
    suggested_price: Mapped[float] = mapped_column(Numeric(10, 2))
    action: Mapped[str] = mapped_column(String(20))
    reason: Mapped[str] = mapped_column(Text)
    created_at = mapped_column(DateTime, server_default=func.now())

class ProductDescription(Base):                      
    __tablename__ = "product_descriptions"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))   
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    keywords: Mapped[list[str]] = mapped_column(ARRAY(String))
    created_at = mapped_column(DateTime, server_default=func.now())     

class campaigns(Base):
    __tablename__ = "campaigns"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    channel: Mapped[str] = mapped_column(String(50))
    audience: Mapped[str] = mapped_column(String(100))
    headline: Mapped[str] = mapped_column(String(200))
    call_to_action: Mapped[str] = mapped_column(String(200))
    created_at = mapped_column(DateTime, server_default=func.now())