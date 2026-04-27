from models import FlowersRecommendation

async def flowers_tool_async(occasion: str, personality_tags: list):
    """Recommend appropriate flowers based on occasion and personality (async version)"""
    
    # Occasion-based recommendations
    occasion_flowers = {
        'first_date': FlowersRecommendation(
            bouquetType="Small mixed bouquet (roses, lilies, and baby's breath)",
            explanation="A modest yet thoughtful gesture. Mixed flowers show effort without being overwhelming for a first date."
        ),
        'anniversary': FlowersRecommendation(
            bouquetType="Dozen red roses with greenery",
            explanation="Classic and romantic. Red roses symbolize deep love and are perfect for celebrating your relationship milestone."
        ),
        'birthday': FlowersRecommendation(
            bouquetType="Colorful mixed bouquet with gerberas and carnations",
            explanation="Bright and cheerful flowers that celebrate joy and happiness, perfect for a birthday celebration."
        ),
        'casual': FlowersRecommendation(
            bouquetType="Single stem or small bouquet of seasonal flowers",
            explanation="Simple and sweet. Seasonal flowers are fresh, affordable, and show thoughtfulness without formality."
        )
    }
    
    recommendation = occasion_flowers.get(occasion, occasion_flowers['casual'])
    
    # Personality-based adjustments
    personality_lower = [p.lower() for p in personality_tags]
    
    if any(p in personality_lower for p in ['minimalist', 'simple']):
        recommendation = FlowersRecommendation(
            bouquetType="Single elegant stem (rose, lily, or orchid)",
            explanation="A single beautiful flower aligns with minimalist aesthetics and shows refined taste."
        )
    
    if any(p in personality_lower for p in ['romantic', 'traditional']):
        recommendation = FlowersRecommendation(
            bouquetType="Classic red roses bouquet",
            explanation="Timeless and romantic. Red roses are universally recognized as symbols of love and passion."
        )
    
    if any(p in personality_lower for p in ['creative', 'artistic', 'artsy']):
        recommendation = FlowersRecommendation(
            bouquetType="Unique mixed bouquet with exotic flowers (orchids, proteas, or anthuriums)",
            explanation="Unconventional and artistic flowers that stand out and reflect creative personality."
        )
    
    if any(p in personality_lower for p in ['nature lover', 'nature_lover', 'eco_conscious']):
        recommendation = FlowersRecommendation(
            bouquetType="Potted flowering plant (orchid, peace lily, or succulent arrangement)",
            explanation="A living plant is eco-friendly, lasts longer, and can be nurtured together as a symbol of growth."
        )
    
    # Add Indian context
    recommendation.explanation += " In Indian context, flowers are deeply appreciated and culturally significant."
    
    return recommendation
