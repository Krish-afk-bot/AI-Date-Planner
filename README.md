<div align="center">

# AI Date Planner

**Personalized date planning powered by Groq AI and real-time data**

![Status](https://img.shields.io/badge/Status-MVP-success)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![React](https://img.shields.io/badge/React-18-61dafb)
![License](https://img.shields.io/badge/License-MIT-green)

*Helping couples create memorable experiences through intelligent planning*

![App Demo](demo.gif)

[Quick Start](#quick-start) | [Architecture](#system-architecture) | [Tech Stack](#technology-stack)

</div>

---

## The Challenge

Planning a date involves juggling multiple factors: personality compatibility, budget constraints, venue quality, timing, and local context. Most people spend hours researching venues, reading reviews, and trying to match their partner's preferences — often resulting in generic, uninspired plans.

**The problem gets worse when:**
- You are in an unfamiliar city
- You have specific dietary or lifestyle constraints
- You want to surprise your partner with something thoughtful
- You are working with a tight budget

---

## Our Solution

AI Date Planner is an intelligent system that generates personalized, contextual date plans in under 15 seconds. It combines:

- **Personality-driven matching** using visual chip selectors for intuitive input
- **Real-time venue search** with quality filtering (4.0+ rating, 50+ reviews)
- **RAG-powered recommendations** from curated knowledge base documents
- **Budget optimization** ensuring plans stay within your range
- **Streaming AI generation** with live progress updates

The system orchestrates multiple data sources in parallel, applies intelligent filtering, and crafts a complete date narrative — all while respecting cultural context and safety considerations for Indian cities.

---

## Key Features

| Feature | Description |
|---------|-------------|
| Personality Matching | Select from 20 personality traits, 20 interests, and 10 dislikes using visual chips |
| Quality Filtering | Only venues with 4.0+ ratings and 50+ reviews; excludes inappropriate types |
| Parallel Execution | Tools run concurrently, reducing generation time from 30s to 10-15s |
| Real-time Streaming | Watch your date plan appear progressively with step-by-step status updates |
| City-Specific Context | Curated guides covering Jaipur, Delhi, Mumbai, Bangalore with budget tiers |
| Budget Intelligence | Automatic cost estimation and validation across all segments |
| Gift & Flower Recommendations | Personalized suggestions based on occasion and personality |
| Google Maps Integration | Direct links to venues with addresses and ratings |

---

## How It Works

```
User Input -> Preference Vector -> Parallel Tool Execution -> RAG Retrieval -> AI Generation -> Structured Plan
```

1. **Profile Creation**: Users select personality traits, interests, and dislikes using visual chips
2. **Location Detection**: Browser geolocation provides current coordinates
3. **Parallel Tool Execution**: Three tools run simultaneously via `asyncio.gather()`:
   - Places API searches nearby venues with quality filters
   - Gift engine generates personalized recommendations
   - Flower selector matches bouquets to occasion
4. **RAG Retrieval**: Query embeddings (sentence-transformers) fetch relevant city guides and dating tips
5. **AI Generation**: Groq (llama-3.3-70b-versatile) streams a narrative plan in real-time
6. **Budget Validation**: Final plan is checked against budget constraints

---

## System Architecture

```
+-------------------------------------------------------------+
|                     Frontend (React + Vite)                  |
|  +--------------+  +--------------+  +--------------+       |
|  | ChipSelector |  | LoadingState |  | DatePlanView |       |
|  +--------------+  +--------------+  +--------------+       |
|                         |                                    |
|                   SSE Streaming                              |
+-------------------------+------------------------------------+
                          |
+-------------------------+------------------------------------+
|                   Backend (Python / Flask)                   |
|                                                              |
|         +------------------+------------------+             |
|         |         Planner Agent (Async)        |             |
|         +------------------+------------------+             |
|                            |                                 |
|         +------------------+------------------+             |
|         |                  |                  |             |
|    +----+----+      +------+-----+    +-------+-----+       |
|    | Places  |      |   Gifts   |    |  Flowers    |       |
|    |  Tool   |      |   Tool    |    |    Tool     |       |
|    +----+----+      +------+-----+    +-------+-----+       |
|         |                  |                  |             |
|         +------------------+------------------+             |
|                   asyncio.gather()                          |
|                            |                                 |
|         +------------------+------------------+             |
|         |             RAG System               |             |
|         |  +------------+  +------------+     |             |
|         |  | Embeddings |  |  Retrieval |     |             |
|         |  +------------+  +------------+     |             |
|         +------------------+------------------+             |
+-------------------------------------------------------------+
                          |
+-------------------------------------------------------------+
|                    External Services                         |
|  +--------------+  +--------------+                         |
|  |   Groq AI    |  | Google Places|                         |
|  | llama-3.3-70b|  |     API      |                         |
|  +--------------+  +--------------+                         |
+-------------------------------------------------------------+
```

---

## User Journey

| Step | User Action | System Response |
|------|-------------|-----------------|
| 1 | Opens app | Displays multi-step form with chip selectors |
| 2 | Selects personality traits (e.g., Romantic, Foodie) | Chips highlight on selection |
| 3 | Chooses interests and dislikes | Max limits enforced, summary shown |
| 4 | Enters budget range (Rs.1000-3000) | Validates min/max input |
| 5 | Allows location access | Browser geolocation captured |
| 6 | Submits form | Streaming begins: "Finding venues..." |
| 7 | Waits 10-15 seconds | Progress steps update: venues -> gifts -> flowers -> crafting |
| 8 | Watches text stream | Date plan appears progressively with blinking cursor |
| 9 | Reviews complete plan | Sees timeline, venues, gifts, flowers, budget breakdown |
| 10 | Clicks venue links | Opens Google Maps for navigation |

---

## Technology Stack

### Frontend
- **React 18** with TypeScript for type safety
- **Vite** for fast development and optimized builds
- **Vanilla CSS** with custom design system (Playfair Display + DM Sans fonts)
- **Server-Sent Events (SSE)** for real-time streaming

### Backend
- **Python 3.9+** with Flask for REST API
- **asyncio + aiohttp** for parallel tool execution
- **Groq SDK** for LLM integration (llama-3.3-70b-versatile)
- **sentence-transformers** (all-MiniLM-L6-v2) for local embeddings
- **NumPy** for vector operations in RAG system

### AI & Data
- **Groq** (llama-3.3-70b-versatile) for fast text generation and streaming
- **sentence-transformers** for semantic search embeddings (runs locally, no API needed)
- **Google Places API** for real-time venue data
- **RAG System** with curated knowledge base documents (city guides, dating tips)

---

## Current Status

### Implemented (MVP)
- Complete frontend with chip selectors and streaming UI
- Async backend with parallel tool execution
- RAG system with knowledge base documents
- Venue quality filtering (4.0+ rating, 50+ reviews)
- Real-time streaming with progress indicators
- Budget validation and cost estimation
- Gift and flower recommendation engines
- Google Maps integration

### Planned (Future)
- User authentication and profile persistence
- Saved date plans and history
- Vendor partnerships for bookings
- Mobile app (React Native)
- Multi-language support

---

## Quick Start

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- A [Groq API key](https://console.groq.com) (free)
- A [Google Places API key](https://console.cloud.google.com/apis/credentials)

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy the env template and fill in your keys
cp .env.example .env
# Edit .env with your GROQ_API_KEY and GOOGLE_PLACES_API_KEY

# Run the server
python app.py
```

Backend starts at `http://localhost:5001`

### Frontend Setup

```bash
cd web

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend starts at `http://localhost:3000`

### Get API Keys

1. **Groq API Key**: Visit [console.groq.com](https://console.groq.com) — free tier available
2. **Google Places API Key**: Visit [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Enable the **Places API** for your project
   - Create credentials -> API Key

---

## Project Structure

```
AI-Date-Planner/
+-- backend/
|   +-- planner/
|   |   +-- planner_agent.py     # Orchestrates the full date planning pipeline
|   +-- rag/
|   |   +-- city_guides.json     # Curated city-specific dating guides
|   |   +-- embed.py             # Embedding + knowledge base initialization
|   |   +-- kb_docs.py           # Static knowledge base documents
|   |   +-- retrieve.py          # Cosine similarity retrieval
|   +-- tools/
|   |   +-- budget_tool.py       # Budget validation and suggestions
|   |   +-- flowers_tool_async.py # Flower recommendations by occasion
|   |   +-- gifts_tool_async.py   # AI-generated gift ideas via Groq
|   |   +-- places_tool_async.py  # Google Places venue search
|   +-- app.py                   # Flask entry point and API routes
|   +-- config.py                # Environment config
|   +-- groq_client.py           # Groq LLM + embedding client
|   +-- models.py                # Python dataclasses (request/response models)
|   +-- requirements.txt
|   +-- .env.example             # Copy this to .env
+-- web/
|   +-- src/
|   |   +-- components/
|   |   |   +-- ChipSelector.tsx  # Reusable pill-chip multi-select
|   |   |   +-- DateForm.tsx      # Multi-step form (3 steps)
|   |   |   +-- DatePlanView.tsx  # Renders the completed date plan
|   |   |   +-- LoadingState.tsx  # Animated progress + streaming preview
|   |   +-- App.tsx               # Root component + SSE streaming logic
|   |   +-- index.css             # All styles and design tokens
|   |   +-- main.tsx              # React entry point
|   |   +-- types.ts              # TypeScript interfaces
|   +-- index.html
|   +-- vite.config.ts            # Vite + proxy config (port 3000 -> 5001)
+-- .gitignore
+-- README.md
```

---

## Contributing

We welcome contributions! If you would like to help improve the AI Date Planner, please **⭐ Star** and **🍴 Fork** the repository, then submit a pull request with your changes.

### Areas that need help
- Additional city guides for the knowledge base
- UI/UX improvements
- Unit and integration test coverage
- Performance optimization

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- **Groq** for fast, free LLM inference
- **Google Places API** for real-time venue data
- **Hugging Face / sentence-transformers** for local embedding models
- **React and Vite** community for excellent tooling

---

<div align="center">

Built for couples who deserve better date nights.

[Report Bug](https://github.com/yourusername/ai-date-planner/issues) | [Request Feature](https://github.com/yourusername/ai-date-planner/issues)

</div>
