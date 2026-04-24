# AI Companion Chatbot - Specification Document

## 1. Project Overview

**Project Name:** CompanionAI
**Project Type:** Full-stack Web Application
**Core Functionality:** An AI chatbot that behaves like a caring human companion with memory and emotional intelligence, supporting natural conversation, long-term memory, context awareness, and personalized responses.
**Target Users:** Individuals seeking emotional support, companionship, and thoughtful conversation.

---

## 2. Tech Stack

### Backend
- **Framework:** FastAPI (Python)
- **Database:** MongoDB (for user data and chat history)
- **Vector DB:** ChromaDB (for semantic memory storage)
- **Authentication:** JWT (JSON Web Tokens)
- **AI Integration:** OpenAI GPT API

### Frontend
- **Framework:** React 18+ with TypeScript
- **Build Tool:** Vite
- **Styling:** CSS Modules + CSS Variables
- **HTTP Client:** Axios
- **Animations:** Framer Motion

---

## 3. UI/UX Specification

### Color Palette
| Role | Color | Hex Code |
|------|-------|----------|
| Primary | Soft Pink | `#FFB6C1` |
| Primary Dark | Deep Rose | `#E88D9E` |
| Secondary | Lavender | `#E6E6FA` |
| Accent | Soft Coral | `#FF7F7F` |
| Background | Cream White | `#FFF5F5` |
| Surface | Pure White | `#FFFFFF` |
| Text Primary | Dark Charcoal | `#2D2D2D` |
| Text Secondary | Soft Gray | `#6B6B6B` |
| User Bubble | Light Pink | `#FFE4E9` |
| AI Bubble | Lavender | `#E8E0FF` |

### Typography
- **Font Family:** "Quicksand" (Google Fonts) for headings, "Nunito" for body
- **Heading Sizes:** H1: 28px, H2: 24px, H3: 20px
- **Body Text:** 16px
- **Small Text:** 14px

### Spacing System
- **Base Unit:** 8px
- **Margins:** 8px, 16px, 24px, 32px
- **Padding:** 8px, 12px, 16px, 24px
- **Border Radius:** 16px (cards), 24px (bubbles), 50% (avatars)

### Layout Structure

#### Login/Register Page
- Centered card (max-width: 420px)
- Logo at top
- Input fields with soft shadows
- Primary pink button with hover animation
- Background: Gradient from lavender to light pink

#### Chat Page (Main Interface)
- **Header:** Fixed top, 64px height
  - Avatar (40px circle)
  - Companion name
  - Settings icon (right)
- **Chat Area:** Scrollable, flexible height
  - Messages with avatar, name, timestamp
  - User messages aligned right (pink bubble)
  - AI messages aligned left (lavender bubble)
  - Typing indicator animation
- **Input Area:** Fixed bottom, 72px height
  - Text input with placeholder
  - Send button (circular, pink)

### Components

#### Message Bubble
- Max-width: 70% of container
- Padding: 12px 16px
- Shadow: soft drop shadow
- Animation: Fade in + slide up

#### Input Field
- Height: 48px
- Border: 2px solid lavender
- Focus: Border color changes to pink
- Placeholder text in soft gray

#### Send Button
- Size: 48px circle
- Background: Primary pink gradient
- Icon: Arrow/plane icon
- Hover: Scale up 1.05, brighter
- Active: Scale down 0.95

#### Loading Animation
- Three bouncing dots
- Sequential animation
- Duration: 0.6s each

### Responsive Breakpoints
- **Mobile:** < 640px (full width, smaller avatars)
- **Tablet:** 640px - 1024px
- **Desktop:** > 1024px (max-width container: 800px)

### Animations
- **Page Transitions:** Fade + slide (300ms ease)
- **Message Appear:** Fade in + translateY (200ms)
- **Button Hover:** Scale transform (150ms)
- **Typing Indicator:** Bounce animation (infinite)
- **Input Focus:** Border color transition (200ms)

---

## 4. Functionality Specification

### Authentication (JWT)

#### Register
- Endpoint: `POST /auth/register`
- Fields: username, email, password
- Returns: JWT token, user info

#### Login
- Endpoint: `POST /auth/login`
- Fields: email, password
- Returns: JWT token, user info

#### Token Refresh
- Endpoint: `POST /auth/refresh`
- Headers: Authorization Bearer token
- Returns: New JWT token

### Chat API

#### Send Message
- Endpoint: `POST /chat/send`
- Headers: Authorization Bearer token
- Request Body: `{ "message": "string" }`
- Response: `{ "reply": "string", "timestamp": "ISO date" }`

#### Get Chat History
- Endpoint: `GET /chat/history`
- Headers: Authorization Bearer token
- Query: `?limit=50&before=timestamp`
- Response: `{ "messages": [{ "role": "user|assistant", "content": "string", "timestamp": "ISO date" }] }`

#### Clear Chat
- Endpoint: `DELETE /chat/clear`
- Headers: Authorization Bearer token

### Memory System

#### Store Memory
- Store important conversation context in MongoDB
- Store semantic embeddings in ChromaDB
- Key information extraction for long-term memory

#### Retrieve Context
- Query vector DB for relevant past conversations
- Include in AI prompt context

### AI Integration

#### Prompt Template
```
You are a caring, empathetic AI companion named "CompanionAI".
You listen attentively, respond with warmth and understanding.
Remember details from our conversations to show you care.
Keep responses conversational, natural, and not too long.

User's name: {user_name}

Recent conversation context:
{context}

Current conversation:
{chat_history}

Remember to be supportive, ask follow-up questions when appropriate,
and show genuine interest in the user's wellbeing.
```

---

## 5. Database Schema

### MongoDB Collections

#### users
```json
{
  "_id": "ObjectId",
  "username": "string",
  "email": "string",
  "password_hash": "string",
  "created_at": "datetime",
  "preferences": {
    "name": "string"
  }
}
```

#### conversations
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "messages": [
    {
      "role": "user|assistant",
      "content": "string",
      "timestamp": "datetime"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### memories
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "content": "string",
  "embedding": "vector",
  "importance": "number",
  "created_at": "datetime"
}
```

---

## 6. API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register new user |
| POST | /auth/login | User login |
| POST | /auth/refresh | Refresh JWT token |
| POST | /chat/send | Send message to AI |
| GET | /chat/history | Get chat history |
| DELETE | /chat/clear | Clear chat history |
| GET | /user/profile | Get user profile |
| PUT | /user/profile | Update user profile |

---

## 7. Acceptance Criteria

### Authentication
- [ ] Users can register with username, email, password
- [ ] Users can login and receive JWT token
- [ ] Protected routes require valid JWT

### Chat
- [ ] Users can send messages and receive AI responses
- [ ] Chat history is persisted
- [ ] Typing indicator shows during AI response

### Memory
- [ ] AI remembers key details from conversations
- [ ] Context is included in AI prompts

### UI/UX
- [ ] Pink/lavender girly theme applied
- [ ] Smooth message animations
- [ ] Mobile responsive
- [ ] Chat bubbles properly styled

### Performance
- [ ] API response time < 2s for chat
- [ ] Frontend loads without errors

---

## 8. Project Structure

```
/backend
  /app
    /api
      /routes
        auth.py
        chat.py
        user.py
    /core
      config.py
      security.py
    /models
      user.py
      chat.py
    /services
      ai.py
      memory.py
    main.py
  /requirements.txt

/frontend
  /src
    /components
      ChatBubble.jsx
      ChatInput.jsx
      Header.jsx
      LoadingDots.jsx
    /pages
      Login.jsx
      Register.jsx
      Chat.jsx
    /services
      api.js
    /styles
      variables.css
      global.css
    App.jsx
    main.jsx
  package.json
  vite.config.js
```