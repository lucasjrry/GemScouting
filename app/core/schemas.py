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
    picture: Optional[str] = None  # URL to player picture

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

    shots: Optional[int] = 0
    shots_on_target: Optional[int] = 0
    expected_goals: Optional[float] = 0.0
    expected_assists: Optional[float] = 0.0
    passes_completed: Optional[int] = 0
    pass_accuracy: Optional[float] = 0.0
    tackles: Optional[int] = 0
    interceptions: Optional[int] = 0

    dribbles_completed: Optional[int] = 0
    dribbles_attempted: Optional[int] = 0
    duels_won: Optional[int] = 0
    duels_lost: Optional[int] = 0


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