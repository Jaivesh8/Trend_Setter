# 🚀 Trend Setter

**Discover Trends. Turn Ideas into Content.**

Trend Setter is an AI-powered platform designed for content creators to
discover trending topics, hashtags, and content ideas while organizing
their creative workflow in one place.

The platform helps creators transform real-time trend insights into
structured content drafts, making content creation more data-driven and
efficient.

------------------------------------------------------------------------

# 📌 Overview

Trend Setter bridges the gap between trend discovery and content
creation by providing tools that allow users to:

-   Discover trending keywords and hashtags
-   Explore trends across niches
-   Save and organize content ideas
-   Manage drafts for future posts
-   Generate AI-powered content insights

------------------------------------------------------------------------

# 🧠 Problem

Content creators often struggle with:

-   Finding trending topics quickly
-   Understanding why certain content goes viral
-   Organizing multiple content drafts
-   Generating consistent content ideas

------------------------------------------------------------------------

# 💡 Solution

Trend Setter provides a creator toolkit that enables users to:

-   Discover trending reels and hashtags
-   Generate optimized content ideas
-   Analyze engagement patterns
-   Manage drafts in one place
-   Refine ideas using AI chat

------------------------------------------------------------------------

# 📱 Mobile Application (TrendCrafters)

The Android app provides an interactive experience to discover trends
and manage content ideas.

Built using **Kotlin + Jetpack Compose** with a modern UI and smooth
animations.

------------------------------------------------------------------------

# ✨ Features

## 🎬 Trending Reels Discovery

-   Animated video card stack showcasing trending reels
-   Videos streamed from AWS S3
-   Auto rotating card stack every 3 seconds
-   Smooth spring animations

## 🔐 Authentication

-   Secure login & signup
-   JWT token management
-   Password visibility toggle
-   Error handling with loading indicators

## 🧭 Onboarding

7-step personalization questionnaire:

-   Content niche
-   Target audience
-   Platform
-   Creator goals
-   Experience level

## 🏠 Home Dashboard

-   Trending reels
-   Live hashtag suggestions
-   Interactive hashtag chips
-   AI content inspiration

## 📝 Draft Manager

Manage and organize content drafts.

Draft states:

-   Ready
-   In Progress
-   Needs Review

## 💬 AI Chat Assistant

Helps creators:

-   Generate reel ideas
-   Improve captions
-   Brainstorm viral concepts

------------------------------------------------------------------------

# 🛠 Tech Stack

  Layer          Technology
  -------------- --------------------
  Language       Kotlin
  UI             Jetpack Compose
  Architecture   MVVM
  Networking     Retrofit
  Video          ExoPlayer
  Animations     Lottie
  Navigation     Compose Navigation

------------------------------------------------------------------------

# 🖥 Backend

Backend built with **FastAPI** and **PostgreSQL**.

## Backend Stack

-   Python
-   FastAPI
-   SQLAlchemy
-   Pydantic
-   JWT Authentication
-   PostgreSQL
-   PyTrends
-   AWS EC2

------------------------------------------------------------------------

# 📂 Backend Structure

trend_backend/

app/ api/routes/ auth.py drafts.py profiles.py trending.py

core/ config.py security.py

models/ user.py draft.py

schemas/ user_schema.py draft_schema.py

services/ trends_service.py

main.py

------------------------------------------------------------------------

# ▶️ Run Backend

``` bash
uvicorn app.main:app --reload
```

Server runs at:

http://127.0.0.1:8000

Docs:

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# 👨‍💻 AuthorS
Ayush Poddar\
Computer Engineering Student
https://github.com/ayush2006-creator
Jaivesh Chopra\
Computer Engineering Student

GitHub: https://github.com/Jaivesh8

------------------------------------------------------------------------

# 📄 License

Hackathon project -- Trend Setter Team
