from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import db

class Warranties(db.Model):
    __tablename__ = "Warranties"

    warranty_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Products.product_id"), nullable=False)
    warranty_months = db.Column(db.Integer(), nullable=False)

    product = db.relationship("Products", back_populates="warranty", uselist=False)


    def __init__(self, product_id, warranty_months):
        self.product_id = product_id
        self.warranty_months = warranty_months

        