# SQLAlechmy database table models/definitions

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime, date

# Make these match the Pydantic schemas in app/core/schemas.py
# add logo string url to league/team + picture for player
# Also add League, Team tables with metadata


Base = declarative_base()


class League(Base):
    __tablename__ = "leagues"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False)
    continent = Column(String(20), nullable=False)  # Europe, South America, etc.
    tier = Column(Integer, nullable=False)  # 1 for top tier, 2 for second tier
    quality_rating = Column(Float, nullable=False)  # 1.0 for top leagues, 0.8 for lower
    has_continental_competition = Column(Boolean, default=False)  # Champions League, etc.
    created_at = Column(DateTime, default=datetime.now)
    logo = Column(String(255), nullable=True)  # URL to league logo
    
    # Relationships
    teams = relationship("Team", back_populates="league")
    performances = relationship("PlayerPerformance", back_populates="league")

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    city = Column(String(50))
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    founded_year = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    logo = Column(String(255), nullable=True)  # URL to team logo
    
    # Relationships
    league = relationship("League", back_populates="teams")
    transfers_from = relationship("Transfer", foreign_keys="Transfer.from_team_id", back_populates="from_team")
    transfers_to = relationship("Transfer", foreign_keys="Transfer.to_team_id", back_populates="to_team")
    performances = relationship("PlayerPerformance", back_populates="team")

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    nationality = Column(String(50), nullable=False)
    position = Column(String(20), nullable=False)  # ST, CM, CB, etc.
    picture = Column(String(255), nullable=True)  # URL to player picture

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
   
    
    # Relationships
    performances = relationship("PlayerPerformance", back_populates="player")
    market_values = relationship("MarketValue", back_populates="player")
    gem_grades = relationship("GemGrade", back_populates="player")
    transfers = relationship("Transfer", back_populates="player")

class PlayerPerformance(Base):
    __tablename__ = "player_performances"
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    season = Column(String(10), nullable=False)  # "2023-24"
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    age_at_season_start = Column(Integer, nullable=False)
    minutes_played = Column(Integer, nullable=False)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    
    # Extended stats (you can add more as needed)
    shots = Column(Integer, default=0)
    shots_on_target = Column(Integer, default=0)
    expected_goals = Column(Float, default=0.0)
    expected_assists = Column(Float, default=0.0)
    passes_completed = Column(Integer, default=0)
    pass_accuracy = Column(Float, default=0.0)
    tackles = Column(Integer, default=0)
    interceptions = Column(Integer, default=0)
    dribbles_completed = Column(Integer, default=0)
    dribbles_attempted = Column(Integer, default=0)
    duels_won = Column(Integer, default=0)
    duels_lost = Column(Integer, default=0)

    
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    player = relationship("Player", back_populates="performances")
    team = relationship("Team", back_populates="performances")
    league = relationship("League", back_populates="performances")

class GemGrade(Base):
    __tablename__ = "gem_grades"
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    season = Column(String(10), nullable=False)
    age_at_calculation = Column(Integer, nullable=False)
    raw_production_score = Column(Float, nullable=False)
    league_strength_bonus = Column(Float, nullable=False)
    age_bonus = Column(Float, nullable=False)
    final_grade = Column(Integer, nullable=False)  # 1-100 scale
    model_version = Column(String(20), default="1.0")  # Track model iterations
    calculated_at = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    player = relationship("Player", back_populates="gem_grades")

class MarketValue(Base):
    __tablename__ = "market_values"
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    season = Column(String(10), nullable=False)
    value = Column(Float, nullable=False)  # Value in euros
    update_date = Column(Date, nullable=False)
    source = Column(String(20), default="transfermarkt")
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    player = relationship("Player", back_populates="market_values")

class Transfer(Base):
    __tablename__ = "transfers"
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    from_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)  # None for first contract
    to_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    transfer_date = Column(Date, nullable=False)
    fee = Column(Float, nullable=True)  # Transfer fee in euros, None for free
    transfer_type = Column(String(20), default="permanent")  # permanent, loan, loan_return
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    player = relationship("Player", back_populates="transfers")
    from_team = relationship("Team", foreign_keys=[from_team_id], back_populates="transfers_from")
    to_team = relationship("Team", foreign_keys=[to_team_id], back_populates="transfers_to")

# Indexes for better query performance
from sqlalchemy import Index

Index('idx_player_birth_date', Player.birth_date)
Index('idx_performance_season_league', PlayerPerformance.season, PlayerPerformance.league_id)
Index('idx_performance_player_season', PlayerPerformance.player_id, PlayerPerformance.season)
Index('idx_gem_grade_player_season', GemGrade.player_id, GemGrade.season)
Index('idx_market_value_player_date', MarketValue.player_id, MarketValue.update_date)
Index('idx_transfer_player_date', Transfer.player_id, Transfer.transfer_date)



