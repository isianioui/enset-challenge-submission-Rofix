# 🎓 EduAgent — Agentic AI Course Generator

> **ENSET Challenge Hackathon 2026 | IA Agentique | Education Track**

EduAgent is a multi-agent AI system that automatically generates complete, structured, and pedagogically sound university-level courses on any topic — from curriculum design to full lesson content.

---

## 🚀 Demo

> Input: `"Introduction to Quantum Computing"`
> Output: Complete course with 8 modules, 3 full lessons, exercises, and references — generated in minutes.

---

## 🧠 Agentic Architecture

EduAgent uses **CrewAI** to orchestrate 4 autonomous specialized agents working in sequence:

```
User Input (Topic)
       │
       ▼
┌─────────────────────┐
│  Curriculum Designer │  ──► Designs course structure & modules
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│  Content Researcher  │  ──► Researches academic content per module
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│   Lesson Writer      │  ──► Writes full lesson content + exercises
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│   QA Specialist      │  ──► Reviews, validates & improves content
└─────────────────────┘
       │
       ▼
  Final Course Package (.md)
```

### Agent Roles

| Agent | Role | Tools |
|-------|------|-------|
| Curriculum Designer | Designs course structure using Bloom's taxonomy | Web Search |
| Content Researcher | Gathers accurate academic content per module | Web Search |
| Lesson Writer | Writes engaging lessons with examples & exercises | LLM |
| QA Specialist | Validates quality, coherence, and academic rigor | LLM |

---

## ⚙️ Tech Stack

- **Framework**: [CrewAI](https://crewai.com) — Multi-agent orchestration
- **LLM**: OpenAI GPT-4o-mini
- **Tools**: SerperDev (web search), LangChain
- **Output**: Structured Markdown course documents
- **Language**: Python 3.10+

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-team/eduagent.git
cd eduagent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

---

## 🎯 Usage

```bash
python main.py
```

```
Enter course topic: Introduction to Machine Learning
```

The system will automatically:
1. Design a complete curriculum (6-8 modules)
2. Research content for each module
3. Write 3 full lesson documents with exercises
4. Run quality validation and corrections
5. Save the course as a `.md` file

---

## 📁 Project Structure

```
eduagent/
├── main.py              # Main orchestration & agent definitions
├── requirements.txt     # Dependencies
├── .env.example         # Environment variables template
├── README.md            # This file
└── outputs/             # Generated course files
    └── course_*.md
```

---

## 📋 Requirements

```
crewai==0.28.0
crewai-tools==0.1.6
langchain-openai==0.1.6
python-dotenv==1.0.0
```
