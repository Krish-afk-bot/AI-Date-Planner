export interface PersonProfile {
  name: string;
  age: number;
  gender: "male" | "female" | "other";
  location: {
    city: string;
    lat?: number;
    lng?: number;
  };
  personalityTags: string[];
  interests: string[];
  dislikes: string[];
}

export interface DateRequest {
  selfProfile: PersonProfile;
  partnerProfile: PersonProfile;
  budgetMin: number;
  budgetMax: number;
  occasion: "first_date" | "anniversary" | "birthday" | "casual";
  maxTravelDistanceKm: number;
  preferredTimeSlots: string[];
  hardConstraints: string[];
  userLocation: {
    lat: number;
    lng: number;
  };
}

export interface DateSegment {
  title: string;
  timeWindow: string;
  placeName?: string;
  placeAddress?: string;
  placeMapUrl?: string;
  actions: string[];
  estimatedCost: number;
}

export interface DatePlan {
  summary: string;
  segments: DateSegment[];
  giftRecommendation: {
    idea: string;
    estimatedCost: number;
    reason: string;
  };
  flowersRecommendation: {
    bouquetType: string;
    explanation: string;
  };
  totalEstimatedCost: number;
  budgetFit: "under" | "within" | "over";
}
