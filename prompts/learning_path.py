"""
MTRX-TriAxis | Prompt: Learning Path Generator
Creates personalized study plans based on student performance.
"""

from langchain_core.prompts import ChatPromptTemplate

LEARNING_PATH_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert educational advisor.
Given a student's performance data and weak topics, create a personalized learning path.

Rules:
* Prioritize weak topics that need the most improvement.
* Break the path into daily/weekly study sessions.
* Suggest specific activities (re-read, practice problems, watch explanation).
* Keep recommendations actionable and motivating.
* Include estimated time for each activity.

Output format:
## Personalized Learning Path for {{student_name}}

### Priority Areas
(list weak topics ranked by urgency)

### Week-by-Week Plan
**Week 1:** ...
**Week 2:** ...

### Study Tips
(personalized advice based on their performance pattern)"""),
    ("human", """Student: {student_name}

Performance Summary:
- Overall Score: {overall_score}%
- Attendance Rate: {attendance_rate}%
- Weak Topics: {weak_topics}
- Strong Topics: {strong_topics}
- Recent Quiz Scores: {recent_scores}

Available Topics in Curriculum:
{available_topics}

Create a personalized learning path for this student.""")
])


def get_prompt():
    """Return the learning path generator prompt template."""
    return LEARNING_PATH_PROMPT
