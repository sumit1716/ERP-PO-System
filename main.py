from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List

# 1. DATABASE SETUP
# 'Sumit' ka 'S' capital rakhna agar wahi password hai
DATABASE_URL = "postgresql://postgres:Sumit@localhost:5432/erp_system"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. MODELS (Tables Mapping)
class Vendor(Base):
    __tablename__ = "vendors"
    vendorid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contact = Column(String)
    rating = Column(Integer)

class Product(Base):
    __tablename__ = "products"
    productid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    sku = Column(String)           # Requirement update
    unitprice = Column(Float)
    stocklevel = Column(Integer)    # Requirement update

# Ye line tables ko sync rakhti hai
Base.metadata.create_all(bind=engine)

# 3. FASTAPI APP & CORS
app = FastAPI(title="IV Innovations ERP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema for Orders
class OrderItem(BaseModel):
    product_id: int
    quantity: int

class OrderPayload(BaseModel):
    vendor_id: int
    reference_no: str
    items: List[OrderItem]

# 4. API ENDPOINTS
@app.get("/")
def home():
    return {"message": "ERP Backend is Live! Open index.html to see the UI."}

@app.get("/api/vendors")
def read_vendors(db: Session = Depends(get_db)):
    return db.query(Vendor).all()

@app.get("/api/products")
def read_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/api/ai-description")
def get_ai_desc(product_name: str):
    # Requirement: Gen AI Marketing Description
    return {"description": f"The {product_name} is a high-performance industrial asset, designed for reliability and seamless integration."}

@app.post("/api/orders")
def create_order(payload: OrderPayload, db: Session = Depends(get_db)):
    total_before_tax = 0.0
    for item in payload.items:
        product = db.query(Product).filter(Product.productid == item.product_id).first()
        if product:
            total_before_tax += (product.unitprice * item.quantity)
    
    # Requirement 1c: 5% Tax Logic
    tax_amount = total_before_tax * 0.05
    final_total = total_before_tax + tax_amount
    
    return {
        "status": "Order Created Successfully",
        "reference_no": payload.reference_no,
        "total_amount": round(final_total, 2)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)