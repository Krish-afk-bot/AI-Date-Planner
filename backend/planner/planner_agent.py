from models import DateRequest, DatePlan, PreferenceVector, DateSegment, Location
from groq_client import generate_text
from rag.retrieve import retrieve_relevant_docs, build_rag_context
from tools.places_tool_async import places_tool_async
from tools.gifts_tool_async import gifts_tool_async
from tools.flowers_tool_async import flowers_tool_async
from tools.budget_tool import budget_tool
import json
import re
import asyncio
import aiohttp

async def run_tools_parallel(request: DateRequest, preference_vector: PreferenceVector, session: aiohttp.ClientSession):
    """Run all tools in parallel for faster execution"""
    print("Running tools in parallel...")
    
    # Prepare tool inputs
    places_input = {
        'lat': request.userLocation.lat,
        'lng': request.userLocation.lng,
        'radius_km': request.maxTravelDistanceKm,
        'categories': ['cafe', 'restaurant', 'park'] if 'outdoor' in preference_vector.vibe else ['cafe', 'restaurant'],
        'filters': preference_vector.constraints,
        'session': session
    }
    
    # Run all tools concurrently
    places_task = places_tool_async(**places_input)
    gifts_task = gifts_tool_async(
        personality_tags=request.partnerProfile.personalityTags,
        interests=request.partnerProfile.interests,
        budget_max=int(request.budgetMax * 0.3),
        occasion=request.occasion
    )
    flowers_task = flowers_tool_async(
        occasion=request.occasion,
        personality_tags=request.partnerProfile.personalityTags
    )
    
    # Gather results with exception handling
    places_result, gifts_result, flowers_result = await asyncio.gather(
        places_task,
        gifts_task,
        flowers_task,
        return_exceptions=True
    )
    
    # Handle exceptions gracefully
    if isinstance(places_result, Exception):
        print(f"Places tool error: {places_result}")
        places_result = []
    if isinstance(gifts_result, Exception):
        print(f"Gifts tool error: {gifts_result}")
        gifts_result = []
    if isinstance(flowers_result, Exception):
        print(f"Flowers tool error: {flowers_result}")
        flowers_result = None
    
    print(f"Found {len(places_result)} places")
    print(f"Generated {len(gifts_result)} gift ideas")
    print("Flower recommendation generated")
    
    return places_result, gifts_result, flowers_result

async def plan_date_async(request: DateRequest):
    """Main planner agent that orchestrates the date planning process (async version)"""
    print("Starting date planning process...")
    
    # Step 1: Build preference vector
    preference_vector = build_preference_vector(request)
    print("Preference vector built")
    
    # Step 2: Retrieve RAG context
    rag_query = build_rag_query(request, preference_vector)
    rag_results = retrieve_relevant_docs(rag_query)
    rag_context = build_rag_context(rag_results)
    print(f"Retrieved {len(rag_results)} relevant KB documents")
    
    # Step 3: Call tools in parallel
    async with aiohttp.ClientSession() as session:
        places, gifts, flowers = await run_tools_parallel(request, preference_vector, session)
    
    # Step 4: Generate date plan with Gemini
    system_prompt = get_system_prompt()
    user_prompt = build_planner_prompt(request, preference_vector, rag_context, places, gifts, flowers)
    
    print("Calling Gemini to generate date plan...")
    response = generate_text(user_prompt, system_instruction=system_prompt, temperature=0.7)
    
    # Step 5: Parse response
    date_plan = parse_date_plan(response)
    
    # Step 6: Validate budget
    budget_input = {
        'budget_min': request.budgetMin,
        'budget_max': request.budgetMax,
        'segments': [
            {'type': seg.title, 'estimatedCost': seg.estimatedCost}
            for seg in date_plan.segments
        ]
    }
    budget_analysis = budget_tool(**budget_input)
    date_plan.budgetFit = budget_analysis['fit']
    
    print("Date plan generated successfully")
    return date_plan

def plan_date(request: DateRequest):
    """Synchronous wrapper for async plan_date"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(plan_date_async(request))
    finally:
        loop.close()

def build_preference_vector(request: DateRequest):
    """Build preference vector from request"""
    all_personality = request.selfProfile.personalityTags + request.partnerProfile.personalityTags
    all_dislikes = request.selfProfile.dislikes + request.partnerProfile.dislikes
    
    # Determine vibe
    vibe = []
    if request.occasion in ['anniversary', 'birthday']:
        vibe.extend(['romantic', 'special'])
    if 'introvert' in all_personality:
        vibe.extend(['quiet', 'intimate'])
    if 'adventurous' in all_personality:
        vibe.extend(['exciting', 'outdoor'])
    if 'foodie' in all_personality:
        vibe.extend(['culinary', 'gourmet'])
    
    # Food preferences
    food = []
    if 'non-veg' in all_dislikes or 'vegetarian' in request.hardConstraints:
        food.append('vegetarian')
    if 'spicy' in all_dislikes:
        food.append('mild')
    
    # Gift style
    gift_style = []
    if 'practical' in all_personality:
        gift_style.append('practical')
    if 'romantic' in all_personality:
        gift_style.append('romantic')
    if 'creative' in all_personality:
        gift_style.append('creative')
    
    return PreferenceVector(
        budgetRange=(request.budgetMin, request.budgetMax),
        vibe=vibe,
        food=food,
        constraints=request.hardConstraints,
        giftStyle=gift_style,
        occasion=request.occasion,
        location=request.selfProfile.location
    )

def build_rag_query(request: DateRequest, pref: PreferenceVector):
    """Build RAG query from request"""
    personality = ' '.join(request.partnerProfile.personalityTags)
    vibe = ' '.join(pref.vibe)
    return f"{request.occasion} date planning for {personality} personality with {vibe} vibe in Indian city context"


def get_system_prompt():
    """System prompt for the planner agent"""
    return """You are an expert AI date planner specializing in Indian city contexts. Your role is to create personalized, thoughtful, and culturally appropriate date plans.

CRITICAL RULES:
1. Use ONLY real places provided in the tool outputs - NEVER invent place names or addresses
2. Respect the budget constraints strictly
3. Consider safety and comfort in Indian city context
4. Duration must be 2-4 hours total
5. Output MUST be valid JSON only - no extra text, explanations, or markdown
6. All costs must be in Indian Rupees (₹)
7. Be culturally sensitive and respectful
8. Consider dietary restrictions and preferences
9. Prioritize well-lit, public, safe venues
10. Account for traffic and travel time in Indian cities

OUTPUT FORMAT:
You must return ONLY a valid JSON object with this exact structure:
{
  "summary": "Brief 2-3 sentence overview of the date plan",
  "segments": [
    {
      "title": "Segment name",
      "timeWindow": "Time range",
      "placeName": "Exact name from places tool output",
      "placeAddress": "Exact address from places tool output",
      "placeMapUrl": "Google Maps URL from places tool output",
      "actions": ["Action 1", "Action 2"],
      "estimatedCost": number
    }
  ],
  "giftRecommendation": {
    "idea": "Gift description",
    "estimatedCost": number,
    "reason": "Why this gift"
  },
  "flowersRecommendation": {
    "bouquetType": "Flower type",
    "explanation": "Why these flowers"
  },
  "totalEstimatedCost": number,
  "budgetFit": "within"
}

IMPORTANT: Return ONLY the JSON object. No markdown, no explanations."""

def build_planner_prompt(request, pref, rag_context, places, gifts, flowers):
    """Build the user prompt with all context"""
    
    # Convert objects to dicts for JSON serialization
    places_data = [
        {
            'name': p.name,
            'address': p.address,
            'rating': p.rating,
            'priceLevel': p.priceLevel,
            'mapsUrl': p.mapsUrl,
            'tags': p.tags,
            'approxCostForTwo': p.approxCostForTwo
        }
        for p in places
    ]
    
    gifts_data = [
        {
            'idea': g.idea,
            'estimatedCost': g.estimatedCost,
            'reason': g.reason
        }
        for g in gifts
    ]
    
    flowers_data = {
        'bouquetType': flowers.bouquetType,
        'explanation': flowers.explanation
    }
    
    return f"""Plan a complete date based on the following information:

=== DATE REQUEST ===
Occasion: {request.occasion}
Budget: ₹{request.budgetMin} - ₹{request.budgetMax}
Max Travel Distance: {request.maxTravelDistanceKm} km
Preferred Time: {', '.join(request.preferredTimeSlots)}
Hard Constraints: {', '.join(request.hardConstraints)}

=== SELF PROFILE ===
Name: {request.selfProfile.name}
Age: {request.selfProfile.age}
Personality: {', '.join(request.selfProfile.personalityTags)}
Interests: {', '.join(request.selfProfile.interests)}
Dislikes: {', '.join(request.selfProfile.dislikes)}

=== PARTNER PROFILE ===
Name: {request.partnerProfile.name}
Age: {request.partnerProfile.age}
Personality: {', '.join(request.partnerProfile.personalityTags)}
Interests: {', '.join(request.partnerProfile.interests)}
Dislikes: {', '.join(request.partnerProfile.dislikes)}

=== PREFERENCE VECTOR ===
Vibe: {', '.join(pref.vibe)}
Food Preferences: {', '.join(pref.food)}
Gift Style: {', '.join(pref.giftStyle)}

{rag_context}

=== AVAILABLE PLACES (USE THESE EXACT DETAILS) ===
{json.dumps(places_data, indent=2)}

=== GIFT IDEAS (CHOOSE ONE) ===
{json.dumps(gifts_data, indent=2)}

=== FLOWER RECOMMENDATION ===
{json.dumps(flowers_data, indent=2)}

Now create a complete date plan following all rules. Return ONLY valid JSON."""

def parse_date_plan(response: str):
    """Parse date plan from Gemini response"""
    try:
        # Remove markdown code blocks
        json_str = response.strip()
        json_str = re.sub(r'```json\n?', '', json_str)
        json_str = re.sub(r'```\n?', '', json_str)
        
        # Find JSON object
        json_match = re.search(r'\{[\s\S]*\}', json_str)
        if json_match:
            json_str = json_match.group(0)
        
        plan_data = json.loads(json_str)
        
        # Validate structure
        if 'summary' not in plan_data or 'segments' not in plan_data:
            raise ValueError("Invalid date plan structure")
        
        # Convert to DatePlan object
        segments = [DateSegment(**seg) for seg in plan_data['segments']]
        
        return DatePlan(
            summary=plan_data['summary'],
            segments=segments,
            giftRecommendation=plan_data['giftRecommendation'],
            flowersRecommendation=plan_data['flowersRecommendation'],
            totalEstimatedCost=plan_data['totalEstimatedCost'],
            budgetFit=plan_data.get('budgetFit', 'within')
        )
    except Exception as e:
        print(f"Error parsing date plan: {e}")
        print(f"Response was: {response}")
        raise Exception("Failed to parse date plan from AI response")