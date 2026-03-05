Trend Setter 🚀
Discover Trends. Turn Ideas into Content.

Trend Setter is a platform designed to help creators discover trending topics, hashtags, and content ideas while organizing their creative workflow in one place.

The platform enables users to explore what is currently trending and transform those insights into structured drafts for future content.

📌 Overview

Creating engaging content requires understanding what people are currently interested in. Trend Setter helps bridge the gap between trend discovery and content creation by providing tools that allow users to:

Discover trending keywords and hashtags

Explore trends across niches

Save and organize content ideas

Manage drafts for future posts

The goal of the platform is to make content ideation faster and more data-driven.

✨ Features
🔐 Authentication

Secure authentication system that allows users to create accounts and log in safely.

Features include:

User registration

Login authentication

Token-based session management

👤 User Profiles

Each user can maintain a personalized profile.

Profiles allow users to:

Select content niches

Manage personal information

Customize their experience on the platform

📝 Draft Management

Users can store and organize their content ideas before publishing.

Draft features include:

Creating new drafts

Updating existing drafts

Viewing all saved drafts

Retrieving a specific draft

Deleting drafts

This allows creators to build and refine content ideas over time.

📈 Trending Insights

Trend Setter provides insight into trending topics and hashtags.

The system collects trending information and exposes it in an easy-to-use format so creators can quickly identify:

Popular keywords

Trending hashtags

Emerging topics across niches

These insights help users align their content with current audience interests.

🏗️ Technology Stack

Trend Setter is built using modern backend technologies designed for scalability and performance.

Core Technologies

Python

FastAPI

SQLAlchemy

Pydantic

Authentication

JWT (JSON Web Tokens)

OAuth2 Password Flow

Database

PostgreSQL

Trend Data

Google Trends (via PyTrends)

Deployment

AWS EC2

Uvicorn ASGI Server

📂 Project Structure
trend_backend/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── drafts.py
│   │       ├── profiles.py
│   │       └── trending.py
│
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│
│   ├── models/
│   │   ├── user.py
│   │   └── draft.py
│
│   ├── schemas/
│   │   ├── user_schema.py
│   │   └── draft_schema.py
│
│   ├── services/
│   │   └── trends_service.py
│
│   └── main.py
│
├── requirements.txt
└── README.md
⚙️ Installation

Clone the repository:

git clone https://github.com/Jaivesh8/Trend_Setter.git
cd Trend_Setter

Create a virtual environment:

python -m venv venv

Activate the environment:

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt
▶️ Running the Application

Start the server:

uvicorn app.main:app --reload

The application will run at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs
🔌 API Endpoints
Authentication
POST /auth/signup
POST /auth/login
Profiles
GET /profile
PUT /profile
Drafts
POST /drafts
GET /drafts
GET /drafts/{id}
PUT /drafts/{id}
DELETE /drafts/{id}
Trends
GET /trending/hashtags
GET /trending/keywords
🚀 Future Improvements

Potential enhancements include:

AI-generated content ideas

Caption and script generation

Personalized trend recommendations

Scheduled trend updates

Creator analytics

Advanced search and filtering

👨‍💻 Author

Jaivesh Chopra
Computer Engineering Student

GitHub:
https://github.com/Jaivesh8
