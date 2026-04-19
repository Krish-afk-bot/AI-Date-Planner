import aiohttp
from config import Config
from models import PlaceResult

# Types to EXCLUDE from venue results
EXCLUDED_TYPES = {
    'lodging', 'hotel', 'motel', 'hospital', 'doctor', 'pharmacy',
    'gas_station', 'parking', 'bank', 'atm', 'grocery_or_supermarket',
    'convenience_store', 'laundry', 'car_wash', 'car_repair',
    'funeral_home', 'police', 'post_office'
}

# Minimum quality thresholds
MIN_RATING = 4.0
MIN_REVIEWS = 50

async def places_tool_async(lat: float, lng: float, radius_km: float, categories: list, filters: list, session: aiohttp.ClientSession):
    """Search for nearby venues using Google Places API (async version)"""
    radius_meters = int(radius_km * 1000)
    
    type_mapping = {
        'restaurant': 'restaurant',
        'cafe': 'cafe',
        'park': 'park',
        'museum': 'museum',
        'bar': 'bar',
        'shopping': 'shopping_mall',
        'entertainment': 'movie_theater'
    }
    
    results = []
    
    for category in categories:
        place_type = type_mapping.get(category, category)
        
        try:
            # Google Places Nearby Search
            url = f"{Config.GOOGLE_PLACES_BASE_URL}/nearbysearch/json"
            params = {
                'location': f"{lat},{lng}",
                'radius': radius_meters,
                'type': place_type,
                'key': Config.GOOGLE_PLACES_API_KEY,
                'rankby': 'prominence'  # Better quality over distance
            }
            
            # Remove radius if using rankby=prominence
            if params['rankby'] == 'prominence':
                del params['radius']
                params['radius'] = radius_meters  # Keep it for now
            
            async with session.get(url, params=params) as response:
                data = await response.json()
            
            if data.get('status') == 'OK':
                places = data.get('results', [])[:10]  # Get more for filtering
                
                for place in places:
                    # Get place details
                    details_url = f"{Config.GOOGLE_PLACES_BASE_URL}/details/json"
                    details_params = {
                        'place_id': place['place_id'],
                        'fields': 'name,formatted_address,rating,price_level,photos,url,types,user_ratings_total',
                        'key': Config.GOOGLE_PLACES_API_KEY
                    }
                    
                    async with session.get(details_url, params=details_params) as details_response:
                        details_data = await details_response.json()
                    
                    if details_data.get('status') == 'OK':
                        details = details_data['result']
                        
                        # Apply quality filters
                        if not passes_quality_filters(details):
                            continue
                        
                        # Apply user filters
                        if not matches_filters(details, filters):
                            continue
                        
                        # Estimate cost
                        price_level = details.get('price_level', 2)
                        approx_cost = estimate_cost(price_level, category)
                        
                        # Get photo URL
                        photo_url = None
                        if details.get('photos'):
                            photo_ref = details['photos'][0]['photo_reference']
                            photo_url = f"{Config.GOOGLE_PLACES_BASE_URL}/photo?maxwidth=400&photoreference={photo_ref}&key={Config.GOOGLE_PLACES_API_KEY}"
                        
                        results.append(PlaceResult(
                            name=details['name'],
                            address=details['formatted_address'],
                            rating=details.get('rating'),
                            priceLevel=details.get('price_level'),
                            mapsUrl=details['url'],
                            tags=extract_tags(details.get('types', []), category, filters),
                            approxCostForTwo=approx_cost,
                            photoUrl=photo_url
                        ))
        except Exception as e:
            print(f"Error searching for {category}: {e}")
    
    # Sort by rating
    results.sort(key=lambda x: x.rating or 0, reverse=True)
    return results[:10]

def passes_quality_filters(place: dict) -> bool:
    """Check if place meets minimum quality standards"""
    venue_types = set(place.get('types', []))
    rating = place.get('rating', 0)
    review_count = place.get('user_ratings_total', 0)
    
    # Skip excluded types
    if venue_types & EXCLUDED_TYPES:
        return False
    
    # Skip low-rated or unreviewed venues
    if rating < MIN_RATING or review_count < MIN_REVIEWS:
        return False
    
    return True

def score_venue_vibe(venue: dict, personality_tags: list) -> float:
    """Score how well a venue matches the user's personality"""
    score = venue.get('rating', 3.0)
    venue_name = venue.get('name', '').lower()
    venue_types = venue.get('types', [])
    
    vibe_map = {
        'Romantic': ['rooftop', 'fine dining', 'bistro', 'candlelight', 'lounge'],
        'Foodie': ['restaurant', 'cafe', 'bistro', 'food', 'kitchen', 'eatery'],
        'Adventurous': ['adventure', 'outdoor', 'garden', 'park', 'activity'],
        'Artsy': ['gallery', 'art', 'museum', 'cultural', 'heritage'],
        'Introvert': ['cafe', 'bookstore', 'quiet', 'library', 'cozy'],
        'Nature Lover': ['garden', 'park', 'lake', 'outdoor', 'nature'],
    }
    
    for tag in personality_tags:
        keywords = vibe_map.get(tag, [])
        for kw in keywords:
            if kw in venue_name or any(kw in t for t in venue_types):
                score += 0.3
    
    return score

def matches_filters(place, filters):
    """Check if place matches user filters"""
    types = place.get('types', [])
    
    for filter_name in filters:
        filter_lower = filter_name.lower()
        
        if filter_lower == 'quiet' or filter_lower == 'quiet_place':
            if any(t in types for t in ['night_club', 'bar', 'stadium']):
                return False
        elif filter_lower == 'outdoor':
            if 'park' not in types and 'campground' not in types:
                return False
        elif filter_lower == 'vegetarian':
            # This would need menu data - for now just pass
            pass
    
    return True

def estimate_cost(price_level: int, category: str):
    """Estimate cost for two based on price level"""
    base_costs = {
        'restaurant': [600, 1200, 2000, 3500],
        'cafe': [300, 500, 800, 1200],
        'bar': [800, 1500, 2500, 4000],
        'park': [0, 50, 100, 200],
        'museum': [100, 200, 400, 600]
    }
    
    costs = base_costs.get(category, [500, 1000, 1500, 2500])
    index = max(0, min(price_level - 1, len(costs) - 1)) if price_level else 1
    
    return costs[index]

def extract_tags(types, category, filters):
    """Extract relevant tags from place types"""
    tags = [category]
    
    relevant_types = ['romantic', 'cozy', 'outdoor', 'indoor', 'casual', 'fine_dining']
    
    for t in types:
        if t in relevant_types:
            tags.append(t)
    
    tags.extend(filters)
    return list(set(tags))
