# Pydantic schemas for data validation and serialization


from pydantic import BaseModel
from typing import Optional, Literal
from datetime import date


class Player(BaseModel):
    player_id: int
    name: str
    birth_date: date
    nationality: str
    position: str

class PlayerPerformance(BaseModel):
    player_id: int
    season: str
    team_id: int
    league_id: int
    age_at_season_start: int
    minutes_played: int
    goals: int
    assists: int
    # ... other stats

class GemGrade(BaseModel):
    player_id: int
    season: str
    age_at_calculation: int
    raw_production_score: float
    league_strength_bonus: float
    age_bonus: float
    final_grade: int
    calculated_at: date

class MarketValue(BaseModel):
    player_id: int
    season: str
    value: float
    update_date: date


class Transfer(BaseModel):
    player_id: int
    from_team_id: Optional[int]  # None for first professional contract
    to_team_id: int
    transfer_date: date
    fee: Optional[float]  # None for loans (0 for free)
    transfer_type: str # (free, loan, permanent, youth)