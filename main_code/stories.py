import streamlit as st
import cultural
import voice
from dotenv import load_dotenv
import os
import story
import google.generativeai as genai
# Set page configuration
st.set_page_config(
    page_title="Cultural Story Teller",
    page_icon="📚",
    layout="wide",
)

load_dotenv()
api_key = os.getenv("API_KEY")
# Custom CSS for enhanced styling
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 50%, #dee2e6 100%);
        background-attachment: fixed;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Typography */
    h1, h2, h3, h4, .story-font {
        font-family: 'Playfair Display', serif;
        color: #212529;
    }
    
    p, div, .sans-font, input, textarea, select {
        font-family: 'Inter', sans-serif;
        color: #343a40;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4dabf7 0%, #339af0 100%);
        border-right: 1px solid #1c7ed6;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        width: 100%;
        margin: 0.25rem 0;
        transition: all 0.3s;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
    }
    
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown p {
        color: white !important;
    }
    
    /* Card styling */
    .feature-card {
        border-radius: 16px;
        padding: 30px 25px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        background: white;
        border: none;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #74c0fc 0%, #4dabf7 100%);
        padding: 4rem 3rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        color: white;
    }
    
    .hero h1, .hero p {
        color: white !important;
    }
    
    /* Step indicator */
    .step-container {
        display: flex;
        justify-content: space-between;
        max-width: 400px;
        margin: 0 auto 3rem;
        position: relative;
    }
    
    .step-container::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 15px;
        right: 15px;
        height: 3px;
        background: #dee2e6;
        transform: translateY(-50%);
        z-index: 1;
    }
    
    .step {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #e9ecef;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        position: relative;
        z-index: 2;
        border: 3px solid white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .step.active {
        background-color: #4dabf7;
        color: white;
    }
    
    /* Story box */
    .story-box {
        background: linear-gradient(to right, #fff9db 0%, #fff3bf 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2.5rem;
        line-height: 1.7;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #fcc419;
        font-size: 1.05rem;
    }
    
    /* Choice buttons */
    .stButton button {
        background: #b2f2bb !important;


        color: white !important;
        border: none !important;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: bold;
        margin: 0.5rem 0;
        width: 100%;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(240, 62, 62, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(8px);
        box-shadow: 0 8px 20px rgba(240, 62, 62, 0.4);
        color: white !important;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #4dabf7 0%, #339af0 100%);
        padding: 1.5rem;
        text-align: center;
        margin-top: 4rem;
        border-radius: 16px;
        box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.1);
        color: white;
    }
    
    /* Custom select boxes */
    .stSelectbox div {
        border-radius: 12px;
    }
    
    /* Text area */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #dee2e6;
        padding: 1rem;
    }

    
    /* Cultural stories page */
    .culture-card {
        background: linear-gradient(135deg, #d0ebff 0%, #a5d8ff 100%);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }
    
    .culture-card:hover {
        transform: translateY(-3px);
    }
    
    /* Headings */
    .section-heading {
        text-align: center;
        margin-bottom: 2.5rem;
        position: relative;
        padding-bottom: 1rem;
    }
    
    .section-heading::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(135deg, #74c0fc 0%, #4dabf7 100%);
        border-radius: 2px;
    }
    
    /* Feature icons */
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        display: block;
    }
    
    /* Card buttons */
    .card-button {
        background: linear-gradient(135deg, #4dabf7 0%, #339af0 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        display: block;
        margin-top: 1.5rem;
        width: 100%;
        box-shadow: 0 5px 15px rgba(51, 154, 240, 0.3);
    }
    
    .card-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(51, 154, 240, 0.4);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Function to change pages
def navigate_to(page):
    st.session_state.current_page = page

# Sidebar - Available on all pages
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0 1rem;">
            <h1 style="font-size: 2.2rem;">📚 Cultural Story Teller</h1>
            <p style="font-size: 1.1rem;">Your AI Story Companion</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    st.markdown(
        """
        <div style="padding: 1rem;">
            <p>Explore stories from around the world, complete unfinished tales, 
            and shape your own adventure through interactive storytelling.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Navigation menu
    st.markdown("### Navigation")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Home"):
            navigate_to('home')
    with col2:
        if st.button("📚 Stories"):
            navigate_to('cultural_stories')
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("✍️ Complete"):
            navigate_to('complete_story')
    with col4:
        if st.button("🎭 Interactive"):
            navigate_to('interactive_mode')
    
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center;">
            <p>Made with ❤️ by Sakshi</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Home Page
def home_page():
    # Main content
    st.markdown(
        """
        <div class="hero">
            <h1 style="font-size: 3rem;">Begin Your Story Adventure ✨</h1>
            <p style="font-size: 1.3rem;">Discover, create, and interact with stories from cultures around the world</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Feature cards
    st.markdown('<div class="section-heading"><h2>Explore Our Features</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card" style="border-top: 5px solid #4dabf7;">
                <div>
                    <span class="feature-icon">📚</span>
                    <h3>Cultural Story Teller</h3>
                    <p>Explore traditional stories from cultures around the world</p>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("Explore Stories", key="cultures_btn", use_container_width=True):
            navigate_to('cultural_stories')

    with col2:
        st.markdown(
            """
            <div class="feature-card" style="border-top: 5px solid #ff6b6b;">
                <div>
                    <span class="feature-icon">✍️</span>
                    <h3>Complete the Story</h3>
                    <p>Finish partially written stories with your creative touch</p>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("Continue Story", key="complete_btn", use_container_width=True):
            navigate_to('complete_story')

    with col3:
        st.markdown(
            """
            <div class="feature-card" style="border-top: 5px solid #51cf66;">
                <div>
                    <span class="feature-icon">🎭</span>
                    <h3>Interactive Mode</h3>
                    <p>Shape the story through your choices and decisions</p>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("Start Adventure", key="interactive_btn", use_container_width=True):
            navigate_to('interactive_mode')

# Cultural Stories Page
def cultural_stories_page():
    st.markdown(
        """
        <div class="section-heading">
            <h1>📚 Cultural Stories from Around the World</h1>
            <p>Explore traditional tales from different cultures</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Culture selection
    col1, col2 = st.columns(2)
    with col1:
        culture = st.selectbox("Select a Culture", 
                               ["Japanese", "Greek", "Norse", "Indian", "Egyptian", "Native American"] , index=3)
    with col2:
        llm = st.selectbox("Select LLM Model", ["gemini-1.5-flash-latest (default)", "gemini-2.0-flash", "gemini-2.5-pro" , "gemini-2.5-flash-lite"])
    
    if culture:
        st.markdown(f"""
        <div class="culture-card">
            <h3>{culture} Folktales ({llm.split(' ')[0]})</h3>
            <p>Explore traditional stories from {culture} culture</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample stories based on culture
        stories = {
            "Japanese": [
                "The Tale of the Bamboo Cutter",
                "Momotaro - The Peach Boy",
                "Urashima Taro and the Turtle",
                "Other"
            ],
            "Greek": [
                "The Story of Persephone and Hades",
                "The Labors of Hercules",
                "Pandora's Box",
                "Other"
            ],
            "Norse": [
                "The Theft of Thor's Hammer",
                "The Story of Fenrir the Wolf",
                "How Odin Lost His Eye",
                "Other"
            ],
            "Indian": [
                "The Ramayana",
                "Mahabharata - The Game of Dice",
                "The Story of Ganesha",
                "Other"
            ],
            "Egyptian": [
                "The Story of Osiris and Isis",
                "The Battle of Horus and Set",
                "The Journey of the Sun God",
                "Other"
            ],
            "Native American": [
                "How the Rabbit Stole the Fire",
                "The Legend of the Dreamcatcher",
                "The Story of the Thunderbird",
                "Other"
            ]
        }
        
        col1 , col2 = st.columns(2)
        with col1:
            selected_story = st.selectbox("Select a story", stories[culture])
        with col2:
            selected_lang = st.selectbox("Select the Language", ["English", "Hindi", "Hinglish", "French", "German", "Chinese"])

        if selected_story == "Other":
            selected_story = st.text_input("Enter the name of the story you want to hear")

        # change the text here
        if st.button("Generate Story"):
            st.markdown("⏳ Generating your story...\n")
            try:
                text = cultural.generate_story(mythology=culture , specific_story=selected_story , model_name = llm.split(' ')[0] , lang = selected_lang)
                st.success("✅ Story generated successfully!")
                st.markdown("### 📖 Here's your story:\n")
                if selected_story:
                    st.markdown(f"""
                    <div class="story-box">
                        <h3>{selected_story}</h3>
                        <p class="sans-font">{text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.download_button(
                        label="📥 Download Story as TXT",
                        data=text,
                        file_name=f"out.txt",
                        mime="text/plain"
                    )
                    with st.spinner("Generating voice... (this may take a while)"):
                        
                        if f'{selected_story}.wav' in os.listdir('voices'):
                            st.audio(f'voices\{selected_story}.wav', format='audio/wav')
                            st.write("File already exists")

                        else:
                            voice.voice_gen(text, file_name=f'voices\{selected_story}.wav')
                            st.audio(f'voices\{selected_story}.wav', format='audio/wav')
                    

                    st.download_button(
                        label="📥 Download Story as WAV",
                        data=open(f'voices\{selected_story}.wav', 'rb').read(),
                        file_name=f'voices\{selected_story}.wav',
                        mime='audio/wav'
                    )
 
                else:
                    st.markdown(f"""
                    <div class="story-box">
                        <p class="sans-font">{text}</p>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ An error occurred while generating the story: {e}")
    
    col1, col2 = st.columns([2, 4])
    with col1:
        if st.button("← Back to Home"):
            navigate_to('home')

# Complete the Story Page
def complete_story_page():
    st.markdown(
        """
        <div class="section-heading">
            <h1>✍️ Generate Your Own Story</h1>
            <p>Finish these partially written stories with your creative touch</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    col1 , col2 = st.columns(2)
    with col1:
        hero_name = st.text_input("Enter Hero's Name", placeholder="e.g., Alex, Maya, John")
    with col2:
        hero_traits = st.text_input("Enter Hero's Traits (comma separated)", placeholder="e.g., brave, curious, clever")

    col3, col4 , col5 = st.columns(3)
    with col3:
        story_genre = st.selectbox("Select a Story Genre", 
                                    [   "Fantasy",
                                        "Science Fiction",
                                        "Mystery",
                                        "Thriller",
                                        "Horror",
                                        "Romance",
                                        "Adventure",
                                        "Historical Fiction",
                                        "Drama",
                                        "Comedy",
                                        "Mythology",
                                        "Fairy Tale",
                                        "Dystopian",
                                        "Superhero",
                                        "Crime/Detective",
                                        "Slice of Life",
                                        "Poetry/Prose",
                                        "Epic/Legend",
                                        "War/Military",
                                        "Inspirational/Motivational"
                                    ]
)
    with col4:
        llm = st.selectbox("Select LLM Model", ["gemini-1.5-flash-latest (default)", "gemini-2.0-flash", "gemini-2.5-pro" , "gemini-2.5-flash-lite"])
    with col5:
        story_language = st.selectbox("Select the Language", ["English", "Hindi", "Hinglish", "French", "German", "Chinese"])
    if story_genre:
        
        st.markdown("### Your Story Plot ...")
        story_plot = st.text_area("Enter your story basic plot", height=200, 
                                 placeholder="Write your creative plot here...")
        
        if st.button("Generate Story Completion"):
             with st.spinner("Generating your story..."):
                if len(story_plot.strip()) > 0:
                    try:
                        new_story = story.generate_story(name=hero_name, 
                                                 traits=hero_traits ,
                                                    genre=story_genre,
                                                    plot=story_plot,
                                                    lang=story_language,
                                                    model_name = llm.split(' ')[0])
                    except Exception as e:
                        st.error(f"❌ An error occurred while generating the story: {e}")
                        return
    
                    # model integration here 
                    # st.write(new_story)
                    st.markdown(f"""
                    <div class="story-box">
                        <h3>{hero_name}'s {story_genre} Adventure</h3>
                        <p class="story-font">{new_story}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Please write something to continue the story!")

                with st.spinner("Generating voice... (this may take a while)"):

                        voice.voice_gen(new_story, file_name=f'voices\{hero_name}.wav')
                        st.audio(f'voices\{hero_name}.wav', format='audio/wav')
                    

                        st.download_button(
                            label="📥 Download Story as WAV",
                            data=open(f'voices\{hero_name}.wav', 'rb').read(),
                            file_name=f'voices\{hero_name}.wav',
                            mime='audio/wav'
                        )
    
    if st.button("← Back to Home", use_container_width=False):
        navigate_to('home')


# --- Configure Gemini ---


if api_key:
    print("API key loaded successfully.")

def interactive_mode_page():
    genai.configure(api_key=api_key)  
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    st.markdown(
        """
        <div class="section-heading">
            <h1>🎭 Interactive Story Adventure</h1>
            <p>Shape the story through your choices and decisions</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # --- Initialize session state ---
    if "story_history" not in st.session_state:
        st.session_state.story_history = ["Once upon a time in a small Indian village..."]
    if "choices" not in st.session_state:
        st.session_state.choices = ["Talk to the village elder", "Explore the sacred forest"]
    if "story_path" not in st.session_state:
        st.session_state.story_path = []
    if "story_step" not in st.session_state:
        st.session_state.story_step = 1

    st.markdown(
        f"""
        <div class="step-container">
            {''.join([f'<div class="step {"active" if st.session_state.story_step >= i else ""}">{i}</div>' for i in range(1, 6)])}
        </div>
        """, 
        unsafe_allow_html=True
    )
    # --- Show full story history ---
    st.markdown("<h2>📖 Your Story So Far</h2>", unsafe_allow_html=True)
    # --- Step indicator ---
    for idx, part in enumerate(st.session_state.story_history, start=1):
        st.markdown(
            f"""
            <div class="story-box">
                <b>Step {idx}:</b> {part}
            </div>
            """, 
            unsafe_allow_html=True
        )


    # --- If final step reached, end story ---
    if st.session_state.story_step > 5:
        st.markdown(
            """
            <div class="story-box">
                <h3>🏁 The End of Your Adventure</h3>
                <p>You've reached the end of this journey. Your choices shaped a unique story.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("🔄 Restart Story", use_container_width=True):
            st.session_state.story_history = ["Once upon a time in a small Indian village..."]
            st.session_state.choices = ["Talk to the village elder", "Explore the sacred forest"]
            st.session_state.story_step = 1
            st.session_state.story_path = []
            st.rerun()
        return

    # --- Handle user choices dynamically ---
    if st.session_state.choices:  # ✅ Only create columns if choices exist
        st.markdown("<h3>What will you do?</h3>", unsafe_allow_html=True)

        cols = st.columns(len(st.session_state.choices))  # ✅ Safe because list not empty
        for idx, choice in enumerate(st.session_state.choices):
            with cols[idx]:
                if st.button(choice):
                    # --- Build prompt for Gemini ---
                    if st.session_state.story_step <= 5:
                        prompt = f"""
                            You are an interactive storytelling AI. 
                            The story should be exactly 5 steps long. 
                            We are currently at step {st.session_state.story_step}.

                            Here is the story so far:
                            {" ".join(st.session_state.story_history)}

                            User choice: {choice}

                            Continue the story in 5-6 sentences. 
                            Then provide 3-4 new options for the next step. 

                            Return the output strictly in this format:
                            Story: <continue the story>
                            Options:
                            1. <option one>
                            2. <option two>
                            3. <option three>
                            4. <option four>


                            If this is the final step (step 5), just write the conclusion without options.
                            The story should be exactly 5 steps long. 
                            Now write the **conclusion** of the story in 4-6 sentences. 
                            Do not provide options. Just finish the adventure. 

                            Return the output strictly in this format:
                            Story: <concluding story>


                    """
                    # else:  # Step 5 → conclude
                    #     prompt = f"""
                    #         You are an interactive storytelling AI. 
                    #         The story should be exactly 5 steps long. 
                    #         We are at step {st.session_state.story_step}, which must be the final step.

                    #         Here is the story so far:
                    #         {" ".join(st.session_state.story_history)}

                    #         User choice: {choice}

                    #         Now write the **conclusion** of the story in 4-6 sentences. 
                    #         Do not provide options. Just finish the adventure. 

                    #         Return the output strictly in this format:
                    #         Story: <concluding story>
                    #     """

                    # --- Call Gemini ---
                    response = model.generate_content(prompt)
                    text = response.text.strip()

                    # --- Parse Gemini response ---
                    story_line = ""
                    new_choices = []
                    for line in text.splitlines():
                        if line.startswith("Story:"):
                            story_line = line.replace("Story:", "").strip()
                        elif line.strip().startswith(("1.", "2.", "3.", "4.")):
                            new_choices.append(line.split(".", 1)[1].strip())

                    # --- Fallback handling ---
                    if not story_line:
                        story_line = text
                    if st.session_state.story_step < 5 and not new_choices:
                        new_choices = ["Continue the story", "End the story"]

                    # --- Update session state ---
                    st.session_state.story_history.append(story_line)
                    st.session_state.story_path.append(choice)
                    st.session_state.story_step += 1
                    st.session_state.choices = new_choices if st.session_state.story_step < 5 else []
                    st.rerun()

    # --- Restart button (only mid-story) ---
    if st.session_state.story_step > 1:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Restart Story"):
                st.session_state.story_history = ["Once upon a time in a small Indian village..."]
                st.session_state.choices = ["Talk to the village elder", "Explore the sacred forest"]
                st.session_state.story_step = 1
                st.session_state.story_path = []
                st.rerun()

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back to Home"):
            navigate_to('home')

# Main app logic to show the correct page
if st.session_state.current_page == 'home':
    home_page()
elif st.session_state.current_page == 'cultural_stories':
    cultural_stories_page()
elif st.session_state.current_page == 'complete_story':
    complete_story_page()
elif st.session_state.current_page == 'interactive_mode':
    interactive_mode_page()
