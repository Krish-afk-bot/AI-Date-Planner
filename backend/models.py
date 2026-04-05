from dataclasses import dataclass, field
from typing import List, Optional, Dict, Literal
from datetime import datetime

@dataclass
class Location:
    city: str
    lat: Optional[float] = None
    lng: Optional[float] = None

@dataclass
class PersonProfile:
    name: str
    age: int
    gender: Literal["male", "female", "other"]
    location: Location
    personalityTags: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    dislikes: List[str] = field(default_factory=list)
    loveLanguageGuess: Optional[List[str]] = None

@dataclass
class UserLocation:
    lat: float
    lng: float

@dataclass
class DateRequest:
    selfProfile: PersonProfile
    partnerProfile: PersonProfile
    budgetMin: int
    budgetMax: int
    occasion: Literal["first_date", "anniversary", "birthday", "casual"]
    maxTravelDistanceKm: int
    preferredTimeSlots: List[str]
    hardConstraints: List[str]
    userLocation: UserLocation

@dataclass
class PreferenceVector:
    budgetRange: tuple
    vibe: List[str]
    food: List[str]
    constraints: List[str]
    giftStyle: List[str]
    occasion: str
    location: Location

@dataclass
class DateSegment:
    title: str
    timeWindow: str
    placeName: Optional[str] = None
    placeAddress: Optional[str] = None
    placeMapUrl: Optional[str] = None
    actions: List[str] = field(default_factory=list)
    estimatedCost: int = 0

@dataclass
class GiftRecommendation:
    idea: str
    estimatedCost: int
    reason: str

@dataclass
class FlowersRecommendation:
    bouquetType: str
    explanation: str

@dataclass
class DatePlan:
    summary: str
    segments: List[DateSegment]
    giftRecommendation: GiftRecommendation
    flowersRecommendation: FlowersRecommendation
    totalEstimatedCost: int
    budgetFit: Literal["under", "within", "over"]

@dataclass
class PlaceResult:
    name: str
    address: str
    rating: Optional[float]
    priceLevel: Optional[int]
    mapsUrl: str
    tags: List[str]
    approxCostForTwo: int
    photoUrl: Optional[str] = None

@dataclass
class GiftIdea:
    idea: str
    estimatedCost: int
    reason: str

@dataclass
class KBDocument:
    id: str
    title: str
    content: str
    tags: List[str]
    embedding: Optional[List[float]] = None
    createdAt: Optional[datetime] = None