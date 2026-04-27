from groq_client import generate_text
from models import GiftIdea
import json
import re

async def gifts_tool_async(personality_tags: list, interests: list, budget_max: int, occasion: str):
    """Generate personalized gift recommendations (async version)"""
    
    # Build prompt for Gemini
    prompt = f"""Generate 3 thoughtful gift ideas for a date occasion.

Context:
- Occasion: {occasion}
- Personality: {', '.join(personality_tags)}
- Interests: {', '.join(interests)}
- Budget: Up to ₹{budget_max}

Requirements:
- Gifts should be appropriate for Indian context
- Consider the relationship stage ({occasion})
- Balance thoughtfulness with appropriateness
- Include practical and creative options
- Stay within budget

Return ONLY a JSON array with this exact structure:
[
  {{
    "idea": "Gift name and brief description",
    "estimatedCost": number,
    "reason": "Why this gift is suitable"
  }}
]"""

    try:
        response = generate_text(prompt, temperature=0.8)
        
        # Extract JSON from response
        json_match = re.search(r'\[[\s\S]*\]', response)
        if json_match:
            gifts_data = json.loads(json_match.group(0))
            return [GiftIdea(**gift) for gift in gifts_data[:3]]
    except Exception as e:
        print(f"Error generating gifts with LLM: {e}")
    
    # Fallback to rule-based
    return generate_rule_based_gifts(personality_tags, interests, budget_max, occasion)

def generate_rule_based_gifts(personality_tags, interests, budget_max, occasion):
    """Fallback rule-based gift generation"""
    gifts = []
    
    # Interest-based
    if any(i.lower() in ['books', 'reading', 'bookworm'] for i in interests + personality_tags):
        gifts.append(GiftIdea(
            idea="Bestselling book in their favorite genre + bookmark",
            estimatedCost=min(500, int(budget_max * 0.3)),
            reason="Thoughtful and personal for book lovers"
        ))
    
    if any(i.lower() in ['music', 'music lover'] for i in interests + personality_tags):
        gifts.append(GiftIdea(
            idea="Wireless earbuds or concert tickets",
            estimatedCost=min(1500, int(budget_max * 0.5)),
            reason="Enhances their music experience"
        ))
    
    # Occasion-based
    if occasion == 'anniversary':
        gifts.append(GiftIdea(
            idea="Personalized photo frame with memorable picture",
            estimatedCost=min(800, int(budget_max * 0.35)),
            reason="Celebrates your shared memories"
        ))
    
    if occasion == 'birthday':
        gifts.append(GiftIdea(
            idea="Experience voucher (spa, adventure, or workshop)",
            estimatedCost=min(2000, int(budget_max * 0.6)),
            reason="Creates new memories together"
        ))
    
    # Default gifts
    if len(gifts) < 3:
        gifts.append(GiftIdea(
            idea="Handwritten letter with small meaningful item",
            estimatedCost=min(300, int(budget_max * 0.2)),
            reason="Personal and heartfelt gesture"
        ))
    
    if len(gifts) < 3:
        gifts.append(GiftIdea(
            idea="Scented candle set or aromatherapy diffuser",
            estimatedCost=min(700, int(budget_max * 0.3)),
            reason="Creates a relaxing ambiance"
        ))
    
    return gifts[:3]
