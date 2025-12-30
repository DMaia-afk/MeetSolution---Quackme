from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

llm = OllamaLLM(model="deepseek-r1:8b")
template = PromptTemplate.from_template("""
You are an assistant specialized in analyzing and synthesizing meeting transcriptions.
Your goal is to extract clear, objective, and reliable information, without inferring or inventing data that is not explicitly present in the text.

Language: English
Tone: Professional, direct, and neutral
Maximum expected reading time for the result: up to 5 minutes
Single source of truth: only the provided transcription

TASK:
From the transcription below, generate a structured summary extracting exclusively explicit information.

TRANSCRIPTION:
{transcricao}

MANDATORY FIELDS:
1. Main Subject
2. My Activities (what was assigned to me)
3. Goals
4. The Most Important of the Meeting
5. Deadlines / Dates / Time Ranges / Deliverables

CRITICAL RULE:
If there is not enough information for any field, write exactly:
"Not mentioned in the transcription."

RULES:
- Do not assume
- Do not interpret implicit intentions
- Do not use external knowledge
- Use short and objective sentences
- Prioritize actionable information
- Faithfully preserve names, tasks, and deadlines
- Record deadlines exactly as mentioned, even if vague

OUTPUT FORMAT (MANDATORY):

Main Subject:
<text or "Not mentioned in the transcription.">

My Activities:
- <activity 1>
- <activity 2>
(or "Not mentioned in the transcription.")

Goals:
- <goal 1>
- <goal 2>
(or "Not mentioned in the transcription.")

The Most Important of the Meeting:
<objective summary or "Not mentioned in the transcription.">

Deadlines / Deliverables:
- <deadline or deliverable>
(or "Not mentioned in the transcription.")

FINAL INSTRUCTION:
Return only the summary in the format above, without additional comments, explanations, or opinions.
""")

chain = template | llm

def generate_summary(transcricao: str) -> str:
    response = chain.invoke({"transcricao": transcricao})
    return response

