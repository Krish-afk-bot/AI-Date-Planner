import sys
import os
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

groq = os.getenv('GROQ_API_KEY', '')
places = os.getenv('GOOGLE_PLACES_API_KEY', '')
placeholder_groq = 'your_groq_api_key_here'
placeholder_places = 'your_google_places_api_key_here'
print('GROQ key set:', bool(groq) and groq != placeholder_groq)
print('Places key set:', bool(places) and places != placeholder_places)
if groq and groq != placeholder_groq:
    print('GROQ key preview:', groq[:8], '...')
if places and places != placeholder_places:
    print('Places key preview:', places[:8], '...')
