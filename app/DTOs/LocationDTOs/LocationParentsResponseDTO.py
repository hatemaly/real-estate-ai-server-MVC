# app/DTOs/LocationDTOs/LocationParentsDTO.py
from pydantic import BaseModel
from app.DTOs.LocationDTOs.LocationResponseDTO import LocationResponseDTO

class LocationParentsResponseDTO(BaseModel):
    items: list[LocationResponseDTO]