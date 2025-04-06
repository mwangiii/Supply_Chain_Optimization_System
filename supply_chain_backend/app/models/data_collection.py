"""data collection model managed by SQLAlchemy"""
from app import db

class DataCollection(db.Model):
    __tablename__ = "data"
    dataid = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    data = db.Column(db.Text, nullable=False)

  