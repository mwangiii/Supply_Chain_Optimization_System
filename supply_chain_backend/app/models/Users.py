"""User model managed by sqlalchemy"""

from app import db
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
import bcrypt

class User(db.Model):
  __tablename__ = "users"
  userid = db.Column(db.string, primary_key=True)
  firstname = db.Column(db.String(50), nullable=False)
  lastname = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, server_default=func.now())

  