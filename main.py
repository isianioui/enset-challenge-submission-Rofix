"""
EduAgent - Auto Lesson & Course Generator
ENSET Challenge Hackathon 2026 - IA Agentique
Multi-agent system using CrewAI to generate structured university-level courses
"""

import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI


# ─────────────────────────────────────────────
# LLM Configuration
# ─────────────────────────────────────────────
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY") # type: ignore
)

search_tool = SerperDevTool()


# ─────────────────────────────────────────────
# AGENT 1 — Curriculum Designer
# ─────────────────────────────────────────────
curriculum_designer = Agent(
    role="University Curriculum Designer",
    goal=(
        "Analyze the requested topic and design a comprehensive, "
        "pedagogically sound course structure tailored for university students."
    ),
    backstory=(
        "You are an expert in educational design with 15+ years of experience "
        "at top universities. You specialize in breaking complex topics into "
        "clear, progressive learning modules aligned with Bloom's taxonomy."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False
)


# ─────────────────────────────────────────────
# AGENT 2 — Content Research Agent
# ─────────────────────────────────────────────
content_researcher = Agent(
    role="Academic Content Researcher",
    goal=(
        "Research and gather accurate, up-to-date academic content "
        "for each course module, including key concepts, examples, and references."
    ),
    backstory=(
        "You are a diligent academic researcher with expertise in synthesizing "
        "information from multiple sources into clear, student-friendly content. "
        "You always prioritize accuracy and academic rigor."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False
)


# ─────────────────────────────────────────────
# AGENT 3 — Lesson Writer
# ─────────────────────────────────────────────
lesson_writer = Agent(
    role="Educational Content Writer",
    goal=(
        "Transform research and course structure into engaging, well-formatted "
        "lesson content with clear explanations, examples, and exercises."
    ),
    backstory=(
        "You are a talented educational content writer who excels at making "
        "complex concepts accessible to university students. Your lessons are "
        "structured, engaging, and include practical examples and assessments."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)


# ─────────────────────────────────────────────
# AGENT 4 — Quality Assurance Agent
# ─────────────────────────────────────────────
qa_agent = Agent(
    role="Educational Quality Assurance Specialist",
    goal=(
        "Review and validate the generated course content for accuracy, "
        "pedagogical quality, coherence, and appropriateness for university level."
    ),
    backstory=(
        "You are a rigorous QA specialist in education with a background in "
        "instructional design. You ensure content meets academic standards, "
        "is logically structured, and free of errors or inconsistencies."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)


# ─────────────────────────────────────────────
# TASKS
# ─────────────────────────────────────────────
def create_tasks(topic: str, level: str = "university"):

    task1 = Task(
        description=(
            f"Design a complete course structure for the topic: '{topic}' "
            f"targeting {level} students. "
            "Include: course title, learning objectives (5-8), "
            "list of 6-8 modules with titles and brief descriptions, "
            "estimated duration per module, and prerequisites."
        ),
        expected_output=(
            "A structured course outline in markdown format with: "
            "title, objectives, module list with descriptions, "
            "duration, and prerequisites."
        ),
        agent=curriculum_designer
    )

    task2 = Task(
        description=(
            f"Research comprehensive academic content for the course on '{topic}'. "
            "For each module in the curriculum, gather: "
            "key concepts and definitions, real-world examples, "
            "latest developments in the field, and suggested readings/references."
        ),
        expected_output=(
            "A detailed research document per module containing: "
            "key concepts, examples, references, and relevant data."
        ),
        agent=content_researcher,
        context=[task1]
    )

    task3 = Task(
        description=(
            "Write full lesson content for the first 3 modules of the course. "
            "Each lesson must include: "
            "1. Learning objectives\n"
            "2. Introduction (hook + context)\n"
            "3. Core content (detailed explanations + examples)\n"
            "4. Key takeaways\n"
            "5. Practice exercises (3 questions)\n"
            "6. Further reading\n"
            "Format output in clean markdown."
        ),
        expected_output=(
            "Three complete lesson documents in markdown format, "
            "each with all 6 sections fully written."
        ),
        agent=lesson_writer,
        context=[task1, task2]
    )

    task4 = Task(
        description=(
            "Review the entire course package (structure + lessons) and provide: "
            "1. Overall quality score (1-10) with justification\n"
            "2. Alignment check with learning objectives\n"
            "3. Identified gaps or improvements\n"
            "4. Final validated and improved course summary\n"
            "Make final corrections directly in the content."
        ),
        expected_output=(
            "A quality report + final corrected course content "
            "ready for delivery to students."
        ),
        agent=qa_agent,
        context=[task1, task2, task3]
    )

    return [task1, task2, task3, task4]


# ─────────────────────────────────────────────
# CREW — Orchestration
# ─────────────────────────────────────────────
def generate_course(topic: str, level: str = "university") -> str:
    """
    Main function to generate a complete course on any topic.
    Returns the final course content as a string.
    """
    print(f"\n🎓 EduAgent — Generating course on: '{topic}'\n{'='*60}\n")

    tasks = create_tasks(topic, level)

    crew = Crew(
        agents=[curriculum_designer, content_researcher, lesson_writer, qa_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    # Save output
    output_path = f"course_{topic.replace(' ', '_').lower()}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(result))

    print(f"\n✅ Course saved to: {output_path}")
    return str(result)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Example usage
    topic = input("Enter course topic: ").strip()
    if not topic:
        topic = "Introduction to Machine Learning"

    result = generate_course(topic, level="university")
    print("\n" + "="*60)
    print("COURSE GENERATION COMPLETE")
    print("="*60)
    print(result[:2000] + "..." if len(result) > 2000 else result)
