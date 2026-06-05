

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

## 🎯 The Challenge

Planning a date involves juggling multiple factors: personality compatibility, budget constraints, venue quality, timing, and local context. Most people spend hours researching venues, reading reviews, and trying to match their partner's preferences—often resulting in generic, uninspired plans.

**The problem gets worse when:**
- You're in an unfamiliar city
- You have specific dietary or lifestyle constraints
- You want to surprise your partner with something thoughtful
- You're working with a tight budget

---

## 💡 Our Solution

AI Date Planner is an intelligent system that generates personalized, contextual date plans in under 15 seconds. It combines:

- **Personality-driven matching** using visual chip selectors for intuitive input
- **Real-time venue search** with quality filtering (4.0+ rating, 50+ reviews)
- **RAG-powered recommendations** from 18 curated knowledge base documents
- **Budget optimization** ensuring plans stay within your range
- **Streaming AI generation** with live progress updates

The system orchestrates multiple data sources in parallel, applies intelligent filtering, and crafts a complete date narrative—all while respecting cultural context and safety considerations for Indian cities.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎭 **Personality Matching** | Select from 20 personality traits, 20 interests, and 10 dislikes using visual chips |
| 🏆 **Quality Filtering** | Only venues with 4.0+ ratings and 50+ reviews; excludes inappropriate types (hotels, hospitals, etc.) |
| ⚡ **Parallel Execution** | Tools run concurrently, reducing generation time from 30s to 10-15s |
| 📡 **Real-time Streaming** | Watch your date plan appear progressively with step-by-step status updates |
| 🌆 **City-Specific Context** | 12 curated guides covering Jaipur, Delhi, Mumbai, Bangalore with budget tiers |
| 💰 **Budget Intelligence** | Automatic cost estimation and validation across all segments |
| 🎁 **Gift & Flower Recommendations** | Personalized suggestions based on occasion and personality |
| 🗺️ **Google Maps Integration** | Direct links to venues with addresses and ratings |

---

## 🔄 How It Works

```
User Input → Preference Vector → Parallel Tool Execution → RAG Retrieval → AI Generation → Structured Plan
```

1. **Profile Creation**: Users select personality traits, interests, and dislikes using visual chips
2. **Location Detection**: Browser geolocation provides current coordinates
3. **Parallel Tool Execution**: Three tools run simultaneously:
   - Places API searches nearby venues with quality filters
   - Gift engine generates personalized recommendations
   - Flower selector matches bouquets to occasion
4. **RAG Retrieval**: Query embeddings fetch relevant city guides and dating tips
5. **AI Generation**: Gemini 2.5 Flash crafts a narrative plan streaming in real-time
6. **Budget Validation**: Final plan is checked against budget constraints

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ ChipSelector │  │ LoadingState │  │ DatePlanView │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                    SSE Streaming                             │
└────────────────────────────┼────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────┐
│                    Backend (Python/Flask)                    │
│                            │                                 │
│         ┌──────────────────┴──────────────────┐             │
│         │     Planner Agent (Async)            │             │
│         └──────────────────┬──────────────────┘             │
│                            │                                 │
│         ┌──────────────────┼──────────────────┐             │
│         │                  │                  │             │
│    ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐       │
│    │ Places  │      │   Gifts   │     │  Flowers  │       │
│    │  Tool   │      │   Tool    │     │   Tool    │       │
│    └────┬────┘      └─────┬─────┘     └─────┬─────┘       │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                   asyncio.gather()                          │
│                            │                                 │
│         ┌──────────────────┴──────────────────┐             │
│         │         RAG System                   │             │
│         │  ┌────────────┐  ┌────────────┐     │             │
│         │  │ Embeddings │  │  Retrieval │     │             │
│         │  └────────────┘  └────────────┘     │             │
│         └──────────────────┬──────────────────┘             │
│                            │                                 │
└────────────────────────────┼────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────┐
│                    External Services                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Gemini AI   │  │ Google Places│  │   Firebase   │      │
│  │  (2.5 Flash) │  │     API      │  │  (Planned)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 👥 User Journey

| Step | User Action | System Response |
|------|-------------|-----------------|
| 1️⃣ | Opens app | Displays form with chip selectors |
| 2️⃣ | Selects personality traits (e.g., Romantic, Foodie) | Chips highlight with pop animation |
| 3️⃣ | Chooses interests and dislikes | Max limits enforced, summary shown |
| 4️⃣ | Enters budget range (₹1000-3000) | Validates input |
| 5️⃣ | Allows location access | Browser geolocation captured |
| 6️⃣ | Submits form | Streaming begins with status: "Finding venues..." |
| 7️⃣ | Waits 10-15 seconds | Progress steps update: venues → gifts → flowers → crafting |
| 8️⃣ | Watches text stream | Date plan appears progressively with blinking cursor |
| 9️⃣ | Reviews complete plan | Sees timeline, venues, gifts, flowers, budget breakdown |
| 🔟 | Clicks venue links | Opens Google Maps for navigation |

---

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript for type safety
- **Vite** for fast development and optimized builds
- **CSS3** with custom design system (Playfair Display + DM Sans fonts)
- **Server-Sent Events (SSE)** for real-time streaming

### Backend
- **Python 3.9+** with Flask for REST API
- **asyncio + aiohttp** for parallel tool execution
- **Google Generative AI SDK** for Gemini 2.5 Flash integration
- **NumPy** for vector operations in RAG system

### AI & Data
- **Gemini 2.5 Flash** for text generation
- **gemini-embedding-001** for semantic search
- **Google Places API** for real-time venue data
- **RAG System** with 18 curated knowledge base documents

### Infrastructure (Planned)
- **Firebase Functions** for serverless deployment
- **Firestore** for user profile storage
- **Firebase Hosting** for frontend delivery

---

## 📊 Current Status

### ✅ Implemented (MVP)
- Complete frontend with chip selectors and streaming UI
- Async backend with parallel tool execution
- RAG system with 18 knowledge base documents
- Venue quality filtering (4.0+ rating, 50+ reviews)
- Real-time streaming with progress indicators
- Budget validation and cost estimation
- Gift and flower recommendation engines
- Google Maps integration

### 🎯 Planned (Future Phases)
- User authentication and profile persistence
- Saved date plans and history
- Vendor partnerships for bookings
- Payment integration for reservations
- Mobile app (React Native)
- Multi-language support
- Social sharing features

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- Google Cloud API keys (Gemini AI + Places API)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_PLACES_API_KEY=your_places_api_key_here
PORT=5001
DEBUG=True
EOF

# Run the server
python run.py
```

Backend will start at `http://localhost:5001`

### Frontend Setup

```bash
# Navigate to web directory
cd web

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will start at `http://localhost:3000`

### Get API Keys

1. **Gemini API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Places API Key**: Visit [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Enable Places API for your project
   - Create credentials → API Key

---

## 📈 MVP Roadmap

### Phase 1: Core Experience ✅
- [x] Personality-driven input system
- [x] Parallel tool execution
- [x] Real-time streaming UI
- [x] Quality venue filtering
- [x] RAG-powered recommendations

### Phase 2: Persistence (Target: Q2 2026)
- [ ] User authentication (Firebase Auth)
- [ ] Profile storage (Firestore)
- [ ] Date plan history
- [ ] Favorite venues

### Phase 3: Monetization (Target: Q3 2026)
- [ ] Vendor partnerships
- [ ] Booking integration
- [ ] Commission system
- [ ] Premium features

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit with clear messages**: `git commit -m 'Add amazing feature'`
5. **Push to your branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request** with a detailed description

### Areas We Need Help
- Mobile app development (React Native)
- Additional city guides for knowledge base
- UI/UX improvements
- Performance optimization
- Test coverage

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful language generation
- **Google Places API** for real-time venue data
- **React community** for excellent tooling and libraries
- **Open source contributors** who inspire us daily

---

<div align="center">

**Made with ❤️ for couples everywhere**

[Report Bug](https://github.com/yourusername/ai-date-planner/issues) • [Request Feature](https://github.com/yourusername/ai-date-planner/issues)

</div>
