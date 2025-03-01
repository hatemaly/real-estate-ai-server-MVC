# app/DTOs/LocationDTOs/PriceUpdateDTO.py
from pydantic import BaseModel

class PriceUpdateRequestDTO(BaseModel):
    average_price_m2: float

class PriceUpdateResponseDTO(BaseModel):
    average_price_m2: float