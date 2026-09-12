import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "openai/gpt-oss-120b"


def test_connection():
    """
    Send a simple test message to Groq to confirm the API key and connection work.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "Say 'GeneLens AI is connected!' and nothing else."}
            ],
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error connecting to Groq: {e}"


SYSTEM_PROMPT = """You are GeneLens AI, a bioinformatics research assistant.

You will be given structured EVIDENCE retrieved from NCBI (Gene, Nucleotide, Protein) and PubMed.
Your job is to write a clear, organized research brief based ONLY on this evidence.

STRICT RULES:
1. You must clearly separate two types of statements:
   - RETRIEVED FACT: a fact that appears directly in the evidence provided (e.g. gene ID, accession number, GC%, a paper's title or PMID).
   - AI INTERPRETATION: your own explanation, summary, or reasoning about what the retrieved facts might mean.
   Label each paragraph or bullet point with one of these two tags in brackets, like: [RETRIEVED FACT] or [AI INTERPRETATION].

2. NEVER invent PMIDs, accession numbers, gene IDs, experimental results, biological functions, or disease associations that are not present in the evidence.

3. If the evidence does not contain information needed to answer something, explicitly say: "This information was not found in the retrieved evidence." Do NOT fill the gap with outside knowledge.

4. Base biological calculations (like GC%) ONLY on the numbers given in the evidence. Do not recalculate or guess new numbers.

5. When referencing a paper, always include its PMID so the user can verify the source.

Write the brief with these sections:
- Gene Summary
- Sequence Characteristics
- Protein Overview
- Relevant Literature
- Notes on Evidence Gaps (mention anything that was not found, if applicable)
"""


def generate_research_brief(evidence):
    """
    Generate an evidence-grounded research brief using Groq.
    Returns the AI's response text, or an error message string if something fails.
    """
    if not os.getenv("GROQ_API_KEY"):
        return "Error: Groq API key is missing. Please check your .env file."

    evidence_text = json.dumps(evidence, indent=2)

    user_prompt = f"""Here is the retrieved evidence for gene query "{evidence.get('query')}":

{evidence_text}

Write the research brief following the rules and section structure you were given."""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating research brief: {e}"