import streamlit as st
import google.generativeai as genai


# --- Configure Gemini ---
genai.configure(api_key="AIzaSyBfbJqduIbFJWledG9IK60X45exlexJMM0")
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# # --- Initialize session state ---
if "story" not in st.session_state:
    st.session_state.story = "Once upon a time in a small Indian village..."
if "choices" not in st.session_state:
    st.session_state.choices = ["Talk to the village elder", "Explore the sacred forest"]

# --- Display current story ---
st.write(st.session_state.story)

# --- Handle user choice ---
for choice in st.session_state.choices:
    if st.button(choice):
        prompt = f"""
Continue the story based on the user's choice:
{st.session_state.story}

User choice: {choice}

Return the output strictly in this format:
Story: <continue the story>
Options:
1. <option one>
2. <option two>
"""
        response = model.generate_content(prompt)
        text = response.text.strip()

        # --- Safe parsing ---
        story_line = ""
        new_choices = []
        for line in text.splitlines():
            if line.startswith("Story:"):
                story_line = line.replace("Story:", "").strip()
            elif line.strip().startswith(("1.", "2.")):
                new_choices.append(line.split(".", 1)[1].strip())

        # --- Fallback if AI response is weird ---
        if not story_line:
            story_line = text
        if not new_choices:
            new_choices = ["Continue the story", "End the story"]

        st.session_state.story = story_line
        st.session_state.choices = new_choices
        # st.experimental_rerun()
