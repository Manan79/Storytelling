from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
api_key = os.getenv("API_KEY")

print("API_KEY found, configuring Gemini...")


# 🔑 Configure Gemini
genai.configure(api_key=api_key)

# 🧠 Story Generator Function
def generate_story(name, traits, genre, plot , lang = 'english' , model_name = "gemini-1.5-flash-latest"):
    # Use the latest available model that supports generateContent
    model = genai.GenerativeModel(model_name)
    prompt = f"""
    You are a master storyteller. Write a detailed and immersive {genre} story featuring a main character named {name}, who is {traits}.
    The story should center around the following plot idea: {plot} and the language in which story is generated must {lang}

    Instructions:
    - The story should be vivid, imaginative, and emotionally compelling.
    - Use rich descriptions, character development, and dialogues where appropriate.
    - Maintain a clear beginning, middle, and end.
    - Word count can be 700 words or more.
    - The tone should match the genre (e.g., mysterious for horror, whimsical for fantasy, futuristic for sci-fi).
    - Include a conflict or challenge that the main character must overcome.
    - Incorporate at least one plot twist to keep the reader engaged.
    - Use sensory details to create an immersive experience (sights, sounds, emotions).
    - Reflect on the main character's growth or change by the end of the story.
    

    End the story with a satisfying or thought-provoking conclusion.
  """

    response = model.generate_content(prompt)
    return response.text


# 🖥️ Console Input
# def main():
#     print("\n📘 Welcome to the Gemini Smart Storyteller\n")

#     name = input("Enter hero's name: ")
#     traits = input("Enter hero's traits (comma separated): ")
#     genre = input("Enter genre (e.g., Fantasy, Sci-Fi, Horror): ")
#     plot = input("Enter a brief plot idea: ")
#     # lang = "Hindi"

#     print("\n⏳ Generating your story...\n")
#     story = generate_story(name, traits, genre, plot)

#     print("📖 Here's your story:\n")
#     print(story)



    # with open(f"{name}_story.txt", "w", encoding="utf-8") as f:
    #     f.write(story)

# if __name__ == "__main__":
#     main()