# SQLAlechmy database models/definitions

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import date

# continue filling out in correspondence with the Pydantic schemas
# Also add League, Team tables with metadata


Base = declarative_base()

class Player(Base):
    __tablename__ = "players"



