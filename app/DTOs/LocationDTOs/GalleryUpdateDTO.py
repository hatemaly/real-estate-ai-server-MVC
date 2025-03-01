# app/DTOs/LocationDTOs/GalleryUpdateDTO.py
from pydantic import BaseModel

class GalleryUpdateRequestDTO(BaseModel):
    gallery_urls: list[str]

class GalleryUpdateResponseDTO(BaseModel):
    gallery_urls: list[str]