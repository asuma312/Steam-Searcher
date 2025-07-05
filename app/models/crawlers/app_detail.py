from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import List

class PcRequirements(BaseModel):
    minimum: str = Field(
        default="", description="Minimum PC requirements for the app or game."
    )
    recommended: str = Field(
        default="", description="Recommended PC requirements for the app or game."
    )




class AppDetail(BaseModel):
    type: str = Field(..., description="Type of the app detail, e.g., 'app', 'game', etc.")
    name: str = Field(..., description="Name of the app or game.")
    steam_appid: int = Field(..., description="Steam App ID of the app or game.")
    required_age: int = Field(..., description="Required age to play the app or game.")
    is_free: bool = Field(..., description="Whether the app is free or not.")
    dlc: List[int] = Field(
        default_factory=list, description="List of downloadable content (DLC) IDs for the app."
    )
    detailed_description: str = Field(
        default="", description="Detailed description of the app or game."
    )
    about_the_game: str = Field(
        default="", description="Information about the game."
    )
    short_description: str = Field(
        default="", description="Short description of the app or game."
    )
    supported_languages: str = Field(
        default="", description="Languages supported by the app or game."
    )
    header_image: str = Field(
        default="", description="URL of the header image for the app or game."
    )
    website: str = Field(
        default="", description="Official website of the app or game."
    )
    pc_requirements: PcRequirements = Field(
        default_factory=PcRequirements, description="PC requirements for the app or game."
    )
    mac_requirements: PcRequirements = Field(
        default_factory=PcRequirements, description="Mac requirements for the app or game."
    )
    linux_requirements: PcRequirements = Field(
        default_factory=PcRequirements, description="Linux requirements for the app or game."
    )
    developers: List[str] = Field(
        default_factory=list, description="List of developers of the app or game."
    )
    publishers: List[str] = Field(
        default_factory=list, description="List of publishers of the app or game."
    )
    price_overview: dict = Field(
        default_factory=dict, description="Price overview of the app or game."
    )
    packages: List[int] = Field(
        default_factory=list, description="List of package IDs for the app."
    )
    platforms: dict = Field(
        default_factory=dict, description="Platforms on which the app or game is available."
    )
    metacritic: dict = Field(
        default_factory=dict, description="Metacritic score and URL for the app or game."
    )
    categories: List[dict] = Field(
        default_factory=list, description="List of categories the app or game belongs to."
    )
    genres: List[dict] = Field(
        default_factory=list, description="List of genres the app or game belongs to."
    )
    screenshots: List[dict] = Field(
        default_factory=list, description="List of screenshots for the app or game."
    )
    movies: List[dict] = Field(
        default_factory=list, description="List of movies related to the app or game."
    )
    recommendations: dict = Field(
        default_factory=dict, description="User recommendations for the app or game."
    )
    achievements: dict = Field(
        default_factory=dict, description="Achievements available in the app or game."
    )
    release_date: dict = Field(
        default_factory=dict, description="Release date information for the app or game."
    )
    support_info: dict = Field(
        default_factory=dict, description="Support information for the app or game."
    )
    background: str = Field(
        default="", description="Background image URL for the app or game."
    )
    content_descriptors: dict = Field(
        default_factory=dict, description="Content descriptors for the app or game."
    )
    tags: List[str] = Field(
        default_factory=list, description="List of tags associated with the app or game."
    )

    @field_validator("mac_requirements", "linux_requirements", "pc_requirements",mode='before')
    def validate_requirements(cls, v: str, info: ValidationInfo):
        if v == []:
            return {}
        return v

    @field_validator('website',mode='before')
    def validate_website(cls, v, info):
        if not v:
            return 'N/A'
        return v

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create an AppDetail instance from a dictionary.
        """
        return cls.model_validate(data)


class AppDetailResponse(BaseModel):
    """
    Response model for app detail retrieval.
    """
    success: bool = Field(..., description="Indicates if the request was successful.")
    data: AppDetail = Field(..., description="App detail data.")
    message: str = Field(default="", description="Message providing additional context or error information.")

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create an AppDetailResponse instance from a dictionary.
        """
        return cls.model_validate(data)