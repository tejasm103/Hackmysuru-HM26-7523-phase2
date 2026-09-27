# Hackmysuru-HM26-7523-phase2 
# Adaptive Learning & Real-Time Intervention Platform

## 1. Problem Understanding & Solution

Traditional learning platforms provide the same content to every student, even though students have different interests, learning speeds, and skill levels.

Our solution uses **video-based learning analytics** to understand what subjects and topics a student is interested in. The system analyzes engagement with short educational video clips and builds a personalized interest and learning profile.

Based on this analysis, the platform recommends:
- Relevant learning topics
- Personalized learning paths
- Suitable courses
- Skill-development opportunities
- Career-oriented learning guidance

---

## 2. Target Users & Use Cases

### Target Users
- Primary school students
- High school students
- College/degree students
- Professional learners
- Teachers and facilitators

### Use Cases
- Discovering student interests
- Personalized subject recommendations
- Identifying weak and strong areas
- Creating a structured learning path
- Recommending courses based on interests and skills
- Helping students build skills for future careers

---

## 3. Solution Overview & Core Journey

### Core Journey

Student watches educational video clips
↓
System tracks engagement
↓
Video/content is analyzed
↓
Student interest profile is created
↓
Learning gaps and strengths are identified
↓
Personalized learning path is generated
↓
Courses and resources are recommended
↓
Progress is continuously monitored

The system adapts recommendations as the student's interests and learning progress change.

---

## 4. Architecture

The platform follows a modular architecture:

### Frontend
Provides:
- Student dashboard
- Video learning feed
- Interest visualization
- Recommended courses
- Learning-path interface
- Progress tracking

### Backend
Handles:
- Student profiles
- Video/content management
- Engagement data
- Recommendation logic
- Learning-path generation
- Progress management

### AI/Analytics Layer
Analyzes:
- Video engagement
- Watch duration
- Completion rate
- Topic preferences
- Learning performance

It converts these signals into an **interest and mastery profile**.

### Database
Stores:
- Student information
- Video metadata
- Engagement records
- Interest profiles
- Course information
- Learning progress

---

## 5. Tech Stack & AI Usage

### Frontend
- Next.js / React
- TypeScript
- Tailwind CSS
- Chart libraries

### Backend
- Node.js
- Next.js API routes
- REST APIs

### Database
- PostgreSQL / MongoDB

### AI & Analytics
- Video/content analysis
- Natural Language Processing
- Recommendation algorithms
- Student interest analysis
- Learning-path generation

### AI Usage

AI analyzes educational video content and student engagement patterns to identify topics that attract the student's attention.

The system combines:
- Watch time
- Completion rate
- Repeated views
- Topic interaction
- Learning performance

to generate personalized recommendations.

---

## 6. Decision Logic Summary + Links

The recommendation engine follows a simple decision process:

1. Collect student learning activity.
2. Analyze engagement with educational videos.
3. Identify frequently engaged topics.
4. Compare interests with current mastery.
5. Identify learning gaps.
6. Generate a prerequisite-based learning path.
7. Recommend relevant courses and resources.
8. Continuously update recommendations using new activity.

### Important Links

- **GitHub Repository:** [Add GitHub URL]
- **Live Demo:** [Add Demo URL]
- **Presentation:** [Add PPT URL]
- **Demo Video:** [Add Video URL]

---

## 7. Setup & Run

### Prerequisites

Install:
- Node.js
- npm
- Git

### Installation

```bash
git clone <repository-url>
cd adaptive-learning-platform
npm install
