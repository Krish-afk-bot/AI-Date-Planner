

# 💕 AI Date Planner

**Personalized date planning powered by Gemini AI and RAG**

![Status](https://img.shields.io/badge/status-MVP-green)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![React](https://img.shields.io/badge/react-18-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

*Helping couples create memorable experiences through AI-powered recommendations*

[Quick Start](#-quick-start) • [Features](#-key-features) • [Architecture](#-system-architecture) • [Tech Stack](#-technology-stack)

</div>

---

## 🎯 Mission

AI Date Planner transforms the stress of date planning into a delightful experience by combining personality analysis, location intelligence, and cultural context to generate personalized date itineraries in minutes.

## 🔍 The Challenge

Planning a memorable date involves juggling multiple factors:
- Understanding both partners' personalities and preferences
- Finding suitable venues within budget and location constraints
- Balancing activities, timing, and cultural appropriateness
- Selecting thoughtful gifts and flowers
- Ensuring safety and comfort in urban Indian contexts

Traditional approaches rely on generic recommendations that ignore individual preferences, leading to mediocre experiences and wasted time.

## 💡 Our Solution

AI Date Planner uses a multi-agent AI system that:

1. **Analyzes** both partners' profiles (personality, interests, dislikes)
2. **Retrieves** relevant dating knowledge from a curated knowledge base using RAG
3. **Searches** real venues via Google Places API based on location and preferences
4. **Generates** personalized gift and flower recommendations
5. **Orchestrates** everything into a complete date plan with timing, costs, and directions
6. **Validates** budget constraints and provides alternatives

The result: A complete, personalized date itinerary in under 30 seconds.

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Personality-Driven Planning** | Analyzes personality tags (introvert, adventurous, foodie) to match venue vibes |
| 📍 **Location Intelligence** | Uses real-time location and Google Places API to find nearby venues |
| 💰 **Budget Optimization** | Allocates budget across segments (dining, gifts, flowers) and validates fit |
| 🎁 **Smart Recommendations** | Generates personalized gift ideas and flower bouquet suggestions |
| 🇮🇳 **Cultural Context** | Considers Indian city safety, dietary restrictions, and social norms |
| 📚 **RAG-Powered Knowledge** | Retrieves relevant dating advice from curated knowledge base |
| ⚡ **Real-Time Generation** | Complete date plans generated in 20-30 seconds |

## 🔄 How It Works

```
User Input → Profile Analysis → RAG Retrieval → Tool Orchestration → AI Planning → Validated Output
```

### Detailed Flow

1. **User submits profiles**: Self and partner details (age, personality, interests, dislikes)
2. **Preference vector built**: System extracts vibe, food preferences, gift style, constraints
3. **RAG retrieval**: Queries knowledge base for relevant dating patterns and tips
4. **Tool execution**:
   - Places Tool: Searches Google Places API for venues
   - Gifts Tool: Generates personalized gift ideas
   - Flowers Tool: Recommends appropriate bouquet
5. **AI orchestration**: Gemini 2.5 Flash synthesizes all inputs into coherent plan
6. **Budget validation**: Ensures total cost fits within user's budget range
7. **Output delivery**: Complete itinerary with segments, timing, costs, and map links

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  DateForm    │  │ LoadingSpinner│  │ DatePlanView │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/JSON
┌────────────────────────────┴────────────────────────────────────┐
│                    Backend (Python/Flask)                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Planner Agent                          │   │
│  │  • Preference Vector Builder                             │   │
│  │  • RAG Query Constructor                                 │   │
│  │  • Tool Orchestrator                                     │   │
│  │  • Response Parser                                       │   │
│  └────┬─────────────────┬─────────────────┬─────────────┬──┘   │
│       │                 │                 │             │        │
│  ┌────▼────┐      ┌─────▼─────┐    ┌─────▼─────┐  ┌───▼────┐  │
│  │   RAG   │      │  Places   │    │   Gifts   │  │ Flowers│  │
│  │ System  │      │   Tool    │    │   Tool    │  │  Tool  │  │
│  └────┬────┘      └─────┬─────┘    └───────────┘  └────────┘  │
│       │                 │                                        │
│  ┌────▼────┐      ┌─────▼─────┐                                │
│  │ Gemini  │      │  Google   │                                │
│  │Embedding│      │  Places   │                                │
│  └─────────┘      │    API    │                                │
│                   └───────────┘                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Gemini 2.5 Flash (Text Generation)          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Purpose |
|-----------|---------|
| **Planner Agent** | Orchestrates entire planning workflow, builds prompts, parses responses |
| **RAG System** | Embeds and retrieves relevant knowledge from curated dating tips |
| **Places Tool** | Searches Google Places API for venues matching preferences |
| **Gifts Tool** | Generates personalized gift ideas based on personality and occasion |
| **Flowers Tool** | Recommends appropriate flower bouquets |
| **Budget Tool** | Validates total cost against user's budget constraints |

## 👥 User Journey

| Step | User Action | System Response |
|------|-------------|-----------------|
| 1 | Opens app | Displays multi-step form |
| 2 | Fills self profile (name, age, personality, interests) | Validates input |
| 3 | Fills partner profile | Validates input |
| 4 | Sets occasion, budget, time preferences | Validates constraints |
| 5 | Grants location access | Captures GPS coordinates |
| 6 | Submits form | Shows loading spinner |
| 7 | Waits 20-30 seconds | Backend processes request |
| 8 | Views generated plan | Displays segments, costs, map links |
| 9 | Clicks map links | Opens Google Maps for navigation |
| 10 | Plans new date | Resets form |

## 🛠️ Technology Stack

### Backend (Python)
| Technology | Purpose |
|------------|---------|
| **Flask 3.0** | Web framework for REST API |
| **google-generativeai** | Gemini AI SDK for text generation and embeddings |
| **NumPy** | Vector operations for cosine similarity |
| **Requests** | HTTP client for Google Places API |
| **python-dotenv** | Environment variable management |

### Frontend (React)
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **TypeScript** | Type-safe development |
| **Vite** | Build tool and dev server |
| **CSS3** | Styling with mobile-first design |

### AI & APIs
| Service | Purpose |
|---------|---------|
| **Gemini 2.5 Flash** | Text generation for date plan synthesis |
| **Gemini Embedding 001** | Text embeddings for RAG retrieval |
| **Google Places API** | Real-time venue search and details |

### Architecture Pattern
- **Multi-Agent System**: Specialized tools coordinated by planner agent
- **RAG (Retrieval-Augmented Generation)**: Knowledge base retrieval for contextual planning
- **Tool-Based Architecture**: Modular tools for places, gifts, flowers, budget

## 📊 Current Status

### ✅ Implemented (MVP)
- Complete profile input system (self + partner)
- Personality-based preference vector generation
- RAG system with 6 curated knowledge base documents
- Google Places API integration for venue search
- Gift and flower recommendation engines
- Budget validation and allocation
- Gemini 2.5 Flash integration for plan generation
- Complete date plan output with segments, costs, and map links
- Mobile-responsive React frontend
- Flask REST API backend

### 🎯 Planned (Future Enhancements)
- User authentication and profile persistence
- Date plan history and favorites
- Multi-city support with city-specific knowledge
- Weather integration for outdoor activity planning
- Restaurant reservation integration
- Ride-sharing cost estimation
- User feedback loop for plan refinement
- A/B testing for recommendation quality
- Analytics dashboard for popular venues and patterns

### 🔮 Target Features (Roadmap)
- Firebase Firestore integration for data persistence
- Social sharing of date plans
- Community-contributed venue reviews
- ML-based personalization from user feedback
- Multi-language support (Hindi, Tamil, Telugu)
- Voice input for profile creation
- Calendar integration for scheduling

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Google Places API key ([Get one here](https://developers.google.com/maps/documentation/places/web-service/get-api-key))

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys:
# GEMINI_API_KEY=your_gemini_key
# GOOGLE_PLACES_API_KEY=your_places_key

# Run backend server
python run.py
```

Backend will start at `http://localhost:5001`

### Frontend Setup

```bash
# Navigate to frontend directory
cd web

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will start at `http://localhost:3000`

### Testing the Application

1. Open `http://localhost:3000` in your browser
2. Fill in your profile (name, age, personality tags like "introvert, foodie")
3. Fill in partner's profile
4. Set occasion (e.g., "anniversary"), budget (e.g., ₹2000-5000)
5. Grant location access
6. Click "Plan My Date"
7. View generated plan with venues, gifts, flowers, and costs

## 🗺️ MVP Roadmap

### Phase 1: Core Functionality ✅
- [x] Profile input system
- [x] Preference vector generation
- [x] RAG knowledge base (6 documents)
- [x] Google Places integration
- [x] Gift/flower recommendation engines
- [x] Gemini AI integration
- [x] Budget validation
- [x] Basic frontend UI

### Phase 2: Enhancement (Target: Q2 2026)
- [ ] User authentication (Firebase Auth)
- [ ] Profile persistence (Firestore)
- [ ] Date plan history
- [ ] Improved error handling
- [ ] Loading states and animations
- [ ] Mobile app (React Native)

### Phase 3: Scale & Optimize (Target: Q3 2026)
- [ ] Multi-city knowledge bases
- [ ] Weather integration
- [ ] Restaurant reservation API
- [ ] User feedback collection
- [ ] A/B testing framework
- [ ] Performance optimization
- [ ] Analytics dashboard

## 🤝 Contribution Guidelines

We welcome contributions! Here's how you can help:

### Areas for Contribution
- **Knowledge Base**: Add more dating tips and patterns for different scenarios
- **Tools**: Create new tools (e.g., weather, transportation, events)
- **Frontend**: Improve UI/UX, add animations, enhance mobile experience
- **Testing**: Write unit tests, integration tests, end-to-end tests
- **Documentation**: Improve setup guides, add tutorials, create videos

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Standards
- Python: Follow PEP 8, use type hints
- TypeScript: Use strict mode, define interfaces
- Comments: Explain "why", not "what"
- Tests: Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ using Gemini AI**

[Report Bug](https://github.com/yourusername/ai-date-planner/issues) • [Request Feature](https://github.com/yourusername/ai-date-planner/issues)

</div>
