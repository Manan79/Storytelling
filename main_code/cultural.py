
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

# 🔑 Configure Gemini
genai.configure(api_key=api_key)

model_name = "gemini-1.5-flash-latest"
# 🧠 Story Generator Function
def generate_story(mythology , specific_story , model_name = "gemini-1.5-flash-latest", lang = 'english'):
    # Use the latest available model that supports generateContent
    model = genai.GenerativeModel(model_name)
    prompt = f"""
    Mythological Storytelling with Chapters Prompt

    You are a master cultural storyteller, speaking directly to a human listener as though seated by a fire.
    Your task is to create a detailed, immersive mythological story, divided into chapters, covering every important event, character, and turning point.

    User Input:

    Mythology: {mythology} (e.g., Hindu, Greek, Norse, Egyptian)

    Specific Story/Character (optional): {specific_story}

    Language: {lang}

    Instructions:

    Narration Style

    Speak in the style of oral tradition storytelling.

    Use rich sensory descriptions (sights, sounds, emotions).

    Include dialogues where appropriate.

    Story Structure

    Start with a warm, inviting introduction (as though by firelight).

    Divide the story into chapters, each with a clear title.

    Chapters should follow a natural flow and each chapter should build on the previous one. and have 400-500 words.:

    Chapter 1: Origins/Introduction

    Chapter 2: Rising Events

    Chapter 3: Conflict/Struggles

    Chapter 4: Climax

    Chapter 5: Resolution/Aftermath

    If Specific Story/Character is Provided

    Stay faithful to cultural roots.

    Expand with vivid details but do not alter the essence.

    If No Specific Story is Provided

    Craft an original myth-inspired tale rooted in chosen mythology.

    Tone & Themes (based on mythology)

    Hindu → moral wisdom, dharma, karma, cosmic balance.

    Greek → heroism, hubris, fate, tragedy.

    Norse → destiny, honor, inevitable doom, courage.

    Egyptian → balance (Ma'at), gods, afterlife, kingship.

    Ending

    After the story, provide a section of moral teachings and learnings.

    Output Format:

    Language: {lang}

    Opening: Storyteller's voice (“Come closer, let me tell you…”)

    Chapters: Clear structure with titles (Chapter 1, Chapter 2…)

    Closing: Moral teachings at the end.

    Example Opening:
    "Come closer, child. The fire is warm, and the night is long. Let me tell you the tale of {specific_story}, a story carried through the winds of {mythology}…"

  """

    response = model.generate_content(prompt)
    return response.text

