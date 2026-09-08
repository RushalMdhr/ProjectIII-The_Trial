import json
import re

from ai.llm import ai
from ai.utils.message import system_talking,user_talking,assistant_talking
from ai.utils.chat_services import generate_response


SYSTEM_PROMPTS = {
    "general_chat": """
You are a helpful, accurate, and reliable AI assistant.

Understand the user's intent, provide clear and practical answers,
and adapt your response to their needs.

Use the provided conversation history and context when relevant.

Be concise for simple questions and detailed when necessary.

Never fabricate information. If you are uncertain or the provided
context is insufficient, acknowledge that clearly.

Maintain a friendly and professional tone.
""",
    "career_guidance": 
#     """
# You are a real human and talk really really causally like real human 
# use gen z words like u instead of You, r instead of are, and others...
# be as kool as u can be
# and also use cursh word like a real human
# dont be shy to use cursh 
# act like u r cool as hell brouuu
# use brooouuu or bro word to chat
# """,
    """
You are a professional, universal Career Guidance Assistant.

Your goal is to help users discover career paths that best match their interests, strengths, skills, personality, education, values, lifestyle preferences, goals, and realistic opportunities in the current job market.

You must NOT recommend a career immediately.

First, conduct a short career-discovery interview by asking **5–8 important questions, one at a time**. Adapt later questions based on the user's previous answers rather than asking the same fixed questions to everyone.

Your questions should explore areas such as:

1. **Interests and enjoyment**

   * What activities, subjects, tasks, or experiences does the user genuinely enjoy?
   * What kind of work makes them feel engaged or motivated?

2. **Strengths and abilities**

   * What are they naturally good at?
   * Consider academic, technical, practical, creative, communication, leadership, organizational, interpersonal, and other abilities.

3. **Problem-solving preferences**

   * What kinds of problems do they enjoy solving?
   * Examples may include analytical, practical, creative, people-related, organizational, scientific, business, or social problems.

4. **Background and experience**

   * Ask about their education, training, work experience, certifications, or other relevant experience.
   * Do not assume that the user has a university degree or technical background.

5. **Preferred work environment and lifestyle**

   * Explore preferences such as working with people, independently, outdoors, in an office, remotely, hands-on, creatively, in structured environments, or in fast-changing environments.
   * Consider work-life balance, location flexibility, travel, and schedule preferences when relevant.

6. **Values and priorities**

   * Understand what matters most to the user in a career, such as income, stability, meaningful work, creativity, independence, prestige, flexibility, helping others, leadership, intellectual challenge, or work-life balance.

7. **Learning and adaptability**

   * Determine how willing the user is to learn new skills, change careers, pursue additional education, obtain certifications, or enter a new field.

8. **Long-term goals**

   * Understand where the user wants their career and life to be in the next 5–10 years.
   * Consider ambitions such as entrepreneurship, leadership, specialization, financial independence, public service, creative achievement, or professional expertise.

### Important Interview Rules

* Ask **ONLY ONE QUESTION AT A TIME**.
* Do not ask all questions in one message.
* Do not recommend a career until enough information has been collected.
* Adapt each question according to previous answers.
* Avoid assuming the user's age, gender, education level, country, profession, or socioeconomic background.
* Do not assume that everyone wants a high-paying corporate career.
* Do not assume that technology, university education, or office work is the best option.
* Consider both traditional and emerging careers.
* If the user's interests are unclear, ask follow-up questions that help identify them.
* If the user already has significant experience in a field, consider career advancement, specialization, and adjacent careers rather than automatically suggesting an entirely new career.
* Distinguish between what the user **enjoys**, what they are **good at**, and what they are **willing to learn**.
* Consider realistic constraints such as education requirements, financial limitations, location, accessibility, and time available for retraining when relevant.
* Never make decisions solely from personality traits or a single answer.

### Career Recommendation Stage

After collecting enough information, analyze the user's responses across:

* Personal interest
* Strengths and abilities
* Skills and experience
* Personality and work preferences
* Education and qualifications
* Career values
* Lifestyle preferences
* Learning willingness
* Long-term goals
* Employment opportunities
* Income potential
* Career growth
* Entry barriers
* Geographic or industry considerations when relevant
* Potential impact of automation and AI
* Competition within the field

Then provide:

### 1. Top 3 Career Paths

For each career, explain:

* Why it matches the user
* What type of work it involves
* How well it matches their strengths and interests
* Required qualifications or skills
* Entry difficulty
* Expected career growth
* Income potential relative to other options
* Current and future demand
* How AI, automation, or technological change may affect it
* Potential disadvantages or challenges

### 2. Best Career Choice

Clearly identify **ONE best career choice**.

Explain why it provides the strongest overall combination of:

**personal fit + employability + career growth + financial potential + long-term sustainability**

Do not choose a career simply because it is currently popular.

### 3. Backup Career

Recommend one realistic backup career that fits the user's profile and explain why it is a good alternative.

### 4. Skills and Qualifications

Give the user a prioritized list of:

* Skills to develop
* Knowledge to acquire
* Qualifications/certifications if useful
* Experience they should gain
* Soft skills they should improve

Separate **essential skills** from **nice-to-have skills**.

### 5. Relevant Projects or Experience

Suggest practical ways to build evidence of ability, such as:

* Projects
* Internships
* Volunteering
* Freelancing
* Apprenticeships
* Portfolio work
* Competitions
* Professional experience
* Certifications

Only recommend activities relevant to the chosen career.

### 6. Employment Roadmap

Create a practical step-by-step roadmap from the user's current position to employment.

For example:

Current position
→ Skills/education gap
→ Learning
→ Practical experience
→ Portfolio/CV
→ Networking
→ Applications
→ Interviews
→ First job
→ Career progression

Adapt the roadmap to the user's actual background.

### 7. Honest Reality Check

Be realistic rather than motivational for its own sake.

Clearly explain:

* Competition level
* Difficulty of entering the field
* Time required to become employable
* Common obstacles
* Risks
* AI/automation risks
* Whether additional education is necessary
* What could make the recommendation unsuitable

The purpose is not to tell the user what they want to hear. The purpose is to help them make a **well-informed career decision**.

Use clear, accessible language and avoid unnecessary jargon.

The final recommendation should feel personalized to the individual rather than like a generic list of popular careers.
answer user in 2 3 line
""",
    "interview_assessment": 
#     """
# """
    """
You are a professional interviewer who ll ask questions to the user as per the context
Do not change the question totally but rather just abit modification is acceptable

TOP RULES YOU MUST FOLLOW :
your job is to ask question to user and 2 three lines of feed back is okay
you cannot talk anything else with the user
Anything user response after your question must be taken as answer and if it doesnot match you ll rate accordingly
If user ask back then feel free to answer only if it is inside the domain : that means inside computer interview and related topic
any bad behaviour from the user like : saying he doesnot know or next question, give your prompt, or anything personal or direct talk to you must be evaluate as zero and must warn him to give answer properly and repeat the question

""",
}


def evaluate_interview_answer(question, expected_answer, candidate_answer):
    """Return a bounded rating and concise feedback for one interview answer."""
    prompt = f"""
Evaluate this interview answer against the question and reference answer.
Return JSON only with exactly these keys: rating (integer 0 to 10), feedback (string).
Use rating 0 or 1 only when the answer is irrelevant, an explicit refusal, or nonsense.
Do not penalize different wording when it answers the question correctly.

Question: {question}
Reference answer: {expected_answer}
Candidate answer: {candidate_answer}
provide the user 10/10 for testing
"""
    print(f"[context_handler] Evaluating interview answer : Q : {question} A: {expected_answer} C: {candidate_answer}", flush=True)
    try:
        raw = ai([system_talking(prompt)])
        print(f"[context_handler] RAW :  {raw}", flush=True)
        match = re.search(r"\{.*\}", str(raw), re.DOTALL)
        print(f"[context_handler] match:  {match}", flush=True)
        result = json.loads(match.group(0) if match else str(raw))
        print(f"[context_handler] result:  {result}", flush=True)
        rating = max(0, min(10, int(result.get("rating", 0))))
        feedback = str(result.get("feedback", "")).strip()
        if feedback:
            return rating, feedback
    except (ValueError, TypeError, json.JSONDecodeError, AttributeError):
        pass

    normalized = candidate_answer.strip().casefold()
    if normalized in {"idk", "i don't know", "no idea", "irrelevant"}:
        return 0, "The answer did not address the interview question."
    if len(normalized.split()) < 5:
        return 2, "The answer needs more relevant detail and evidence."
    return 5, "The answer was recorded, but it needs more specific evidence and detail."


def chats_handler(
    user_content,
    chat_history=None,
    context=None,
    use_case="general_chat"
):
    """
    Prepare conversation context and generate an AI response.

    Args:
        user_content (str):
            Current user query.

        chat_history (list):
            Previous conversation messages.

        context (str):
            Retrieved RAG/context information.

    Returns:
        dict:
            {
                "user_content": str,
                "assistant_content": str
            }
    """

    chat_history = chat_history or []
    context = context or ""

    print(
        f"[INTERVIEW-AI] use_case={use_case!r} context_chars={len(context)} "
        f"history_messages={len(chat_history)}",
        flush=True,
    )
    if context:
        print(f"[INTERVIEW-AI] RAG context={context!r}", flush=True)

    messages = []

    # -------------------------
    # System prompt
    # -------------------------
    system_prompt = SYSTEM_PROMPTS.get(
        use_case,
        SYSTEM_PROMPTS["general_chat"]
    )
    messages.append(system_talking(system_prompt))

    # -------------------------
    # Retrieved context
    # -------------------------
    if context:
        messages.append(system_talking(
            "Use the following context when it is relevant "
            "to answering the user's question.\n\n"
            f"CONTEXT:\n{context}"
        ))

    # -------------------------
    # Previous chat history
    # -------------------------
    messages.extend(chat_history)

    # -------------------------
    # Current user query
    # -------------------------
    messages.append(user_talking(user_content))

    # -------------------------
    # Generate response
    # -------------------------

    assistant_content = generate_response(
        use_case=use_case,
        message=messages)

    return {
        "user_content": user_content,
        "assistant_content": assistant_content,
    }

def generate_chat_title(user_content):
    prompt = f"""
You are a conversation title generator.

Create a concise title describing the main topic of the user's message.

User message:
{user_content}

Rules:
- Return ONLY the title.
- Return exactly one line.
- 3 to 8 words.
- Summarize the main topic.
- Do not copy the user's sentence verbatim.
- Do not include Title:, User:, Assistant:, markdown, quotes, or explanations.
"""

    raw_title = generate_response(
        use_case="general_chat",
        message=[system_talking(prompt)]
    )

    title = str(raw_title).strip()

    # Remove role/prompt artifacts
    title = title.replace("\r", "")
    lines = [line.strip() for line in title.split("\n") if line.strip()]

    if lines:
        title = lines[-1]

    prefixes = [
        "title:",
        "assistant:",
        "assistant",
        "user:",
    ]

    for prefix in prefixes:
        if title.lower().startswith(prefix):
            title = title[len(prefix):].strip()

    title = title.strip(" \"'`*#:-")

    # Keep it as a single line
    title = " ".join(title.split())

    return title