from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from config import Config, validate_config
from planner.planner_agent import plan_date, plan_date_async, build_preference_vector, run_tools_parallel
from rag.retrieve import retrieve_relevant_docs, build_rag_context
from rag.embed import initialize_knowledge_base
from models import PersonProfile, DateRequest, Location, UserLocation
from datetime import datetime
import traceback
import json
import asyncio
import aiohttp
from groq_client import generate_text_stream

# Validate configuration
validate_config()

# Create Flask app
app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'Python backend running'
    })

@app.route('/api/save-profile', methods=['POST'])
def save_profile():
    """Save couple profiles"""
    try:
        data = request.json
        self_profile = data.get('selfProfile')
        partner_profile = data.get('partnerProfile')
        
        if not self_profile or not partner_profile:
            return jsonify({
                'error': 'Both selfProfile and partnerProfile are required'
            }), 400
        
        # Mock save for local dev
        return jsonify({
            'success': True,
            'profileId': f"local-{datetime.now().timestamp()}"
        })
    except Exception as e:
        print(f"Error saving profile: {e}")
        return jsonify({
            'error': 'Failed to save profile',
            'details': str(e)
        }), 500

@app.route('/api/plan-date/stream', methods=['POST'])
def plan_date_stream():
    """Generate a complete date plan with streaming output"""
    data = request.json
    
    def generate():
        try:
            # Step 1: Signal tools are starting
            yield f"data: {json.dumps({'type': 'status', 'message': 'Finding venues...'})}\n\n"
            
            # Build request object
            date_request = build_date_request(data)
            
            # Build preference vector
            from planner.planner_agent import build_preference_vector, build_rag_query, get_system_prompt, build_planner_prompt
            preference_vector = build_preference_vector(date_request)
            
            # Retrieve RAG context
            rag_query = build_rag_query(date_request, preference_vector)
            rag_results = retrieve_relevant_docs(rag_query)
            rag_context = build_rag_context(rag_results)
            
            # Run parallel tools
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                async def get_tools():
                    async with aiohttp.ClientSession() as session:
                        return await run_tools_parallel(date_request, preference_vector, session)
                
                places, gifts, flowers = loop.run_until_complete(get_tools())
                
                yield f"data: {json.dumps({'type': 'status', 'message': 'Crafting your date plan...'})}\n\n"
                
                # Step 2: Stream Groq output token by token
                system_prompt = get_system_prompt()
                user_prompt = build_planner_prompt(date_request, preference_vector, rag_context, places, gifts, flowers)
                
                full_text = ""
                for chunk in generate_text_stream(user_prompt, system_instruction=system_prompt, temperature=0.7):
                    full_text += chunk
                    yield f"data: {json.dumps({'type': 'chunk', 'text': chunk})}\n\n"
                
                # Step 3: Parse and send structured data
                from planner.planner_agent import parse_date_plan
                date_plan = parse_date_plan(full_text)
                
                # Validate budget
                from tools.budget_tool import budget_tool
                budget_input = {
                    'budget_min': date_request.budgetMin,
                    'budget_max': date_request.budgetMax,
                    'segments': [
                        {'type': seg.title, 'estimatedCost': seg.estimatedCost}
                        for seg in date_plan.segments
                    ]
                }
                budget_analysis = budget_tool(**budget_input)
                date_plan.budgetFit = budget_analysis['fit']
                
                structured = date_plan_to_dict(date_plan)
                yield f"data: {json.dumps({'type': 'structured', 'data': structured})}\n\n"
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
                
            finally:
                loop.close()
                
        except Exception as e:
            print(f"Error in streaming: {e}")
            traceback.print_exc()
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Access-Control-Allow-Origin': '*'
        }
    )

@app.route('/api/plan-date', methods=['POST'])
def plan_date_endpoint():
    """Generate a complete date plan"""
    try:
        data = request.json
        
        # Validate request
        if not data.get('selfProfile') or not data.get('partnerProfile'):
            return jsonify({
                'error': 'Both selfProfile and partnerProfile are required'
            }), 400
        
        if not data.get('userLocation') or not data['userLocation'].get('lat') or not data['userLocation'].get('lng'):
            return jsonify({
                'error': 'User location (lat, lng) is required'
            }), 400
        
        if not data.get('budgetMin') or not data.get('budgetMax'):
            return jsonify({
                'error': 'Budget range (budgetMin, budgetMax) is required'
            }), 400
        
        # Build request object
        date_request = build_date_request(data)
        
        print(f"Received date planning request: {date_request.occasion}, Budget: ₹{date_request.budgetMin}-{date_request.budgetMax}")
        
        # Generate date plan
        date_plan = plan_date(date_request)
        
        # Convert to dict for JSON response
        plan_dict = date_plan_to_dict(date_plan)
        
        return jsonify({
            'success': True,
            'plan': plan_dict
        })
    except Exception as e:
        print(f"Error planning date: {e}")
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to plan date',
            'details': str(e)
        }), 500

@app.route('/api/init-kb', methods=['POST'])
def init_kb():
    """Initialize knowledge base"""
    try:
        initialize_knowledge_base()
        return jsonify({
            'success': True,
            'message': 'Knowledge base initialized successfully'
        })
    except Exception as e:
        print(f"Error initializing KB: {e}")
        return jsonify({
            'error': 'Failed to initialize knowledge base',
            'details': str(e)
        }), 500


def build_date_request(data):
    """Build DateRequest object from JSON data"""
    
    # Build self profile
    self_loc = data['selfProfile']['location']
    self_profile = PersonProfile(
        name=data['selfProfile']['name'],
        age=data['selfProfile']['age'],
        gender=data['selfProfile']['gender'],
        location=Location(
            city=self_loc['city'],
            lat=self_loc.get('lat'),
            lng=self_loc.get('lng')
        ),
        personalityTags=data['selfProfile'].get('personalityTags', []),
        interests=data['selfProfile'].get('interests', []),
        dislikes=data['selfProfile'].get('dislikes', [])
    )
    
    # Build partner profile
    partner_loc = data['partnerProfile']['location']
    partner_profile = PersonProfile(
        name=data['partnerProfile']['name'],
        age=data['partnerProfile']['age'],
        gender=data['partnerProfile']['gender'],
        location=Location(
            city=partner_loc['city'],
            lat=partner_loc.get('lat'),
            lng=partner_loc.get('lng')
        ),
        personalityTags=data['partnerProfile'].get('personalityTags', []),
        interests=data['partnerProfile'].get('interests', []),
        dislikes=data['partnerProfile'].get('dislikes', [])
    )
    
    # Build user location
    user_location = UserLocation(
        lat=data['userLocation']['lat'],
        lng=data['userLocation']['lng']
    )
    
    # Build date request
    return DateRequest(
        selfProfile=self_profile,
        partnerProfile=partner_profile,
        budgetMin=data['budgetMin'],
        budgetMax=data['budgetMax'],
        occasion=data.get('occasion', 'casual'),
        maxTravelDistanceKm=data.get('maxTravelDistanceKm', 5),
        preferredTimeSlots=data.get('preferredTimeSlots', ['evening']),
        hardConstraints=data.get('hardConstraints', []),
        userLocation=user_location
    )

def date_plan_to_dict(plan):
    """Convert DatePlan to dictionary"""
    return {
        'summary': plan.summary,
        'segments': [
            {
                'title': seg.title,
                'timeWindow': seg.timeWindow,
                'placeName': seg.placeName,
                'placeAddress': seg.placeAddress,
                'placeMapUrl': seg.placeMapUrl,
                'actions': seg.actions,
                'estimatedCost': seg.estimatedCost
            }
            for seg in plan.segments
        ],
        'giftRecommendation': {
            'idea': plan.giftRecommendation['idea'] if isinstance(plan.giftRecommendation, dict) else plan.giftRecommendation.idea,
            'estimatedCost': plan.giftRecommendation['estimatedCost'] if isinstance(plan.giftRecommendation, dict) else plan.giftRecommendation.estimatedCost,
            'reason': plan.giftRecommendation['reason'] if isinstance(plan.giftRecommendation, dict) else plan.giftRecommendation.reason
        },
        'flowersRecommendation': {
            'bouquetType': plan.flowersRecommendation['bouquetType'] if isinstance(plan.flowersRecommendation, dict) else plan.flowersRecommendation.bouquetType,
            'explanation': plan.flowersRecommendation['explanation'] if isinstance(plan.flowersRecommendation, dict) else plan.flowersRecommendation.explanation
        },
        'totalEstimatedCost': plan.totalEstimatedCost,
        'budgetFit': plan.budgetFit
    }

if __name__ == '__main__':
    print("🚀 Starting AI Date Planner Backend (Python)")
    print(f"   API: http://localhost:{Config.PORT}/api")
    print(f"   Health: http://localhost:{Config.PORT}/api/health")
    print("✅ Ready to accept requests!\n")
    
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )