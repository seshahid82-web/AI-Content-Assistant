import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered",
)

st.title("✍️ AI Content Assistant")
st.write("Create social media content with Groq and Python.")

def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.getenv("GROQ_API_KEY", "")

api_key = get_api_key()

if not api_key:
    st.warning("Please add your GROQ_API_KEY in Streamlit secrets or as an environment variable.")
    st.stop()

client = Groq(api_key=api_key)

content_type = st.selectbox(
    "Content type",
    ["Social media post", "LinkedIn post", "Instagram caption", "Blog introduction", "Marketing email"],
)

platform = st.selectbox(
    "Platform",
    ["Facebook", "LinkedIn", "Instagram", "X/Twitter", "Website", "Email"],
)

topic = st.text_input(
    "Topic",
    placeholder="Example: Benefits of learning Python",
)

audience = st.text_input(
    "Target audience",
    placeholder="Example: Beginners and IT students",
)

tone = st.selectbox(
    "Tone",
    ["Professional", "Friendly", "Simple", "Inspirational", "Persuasive", "Educational"],
)

extra_instructions = st.text_area(
    "Extra instructions (optional)",
    placeholder="Example: Keep it short and include a call to action.",
)

generate = st.button("Generate content", type="primary", use_container_width=True)

if generate:
    if not topic.strip():
        st.error("Please enter a topic.")
        st.stop()

    if not audience.strip():
        st.error("Please enter the target audience.")
        st.stop()

    prompt = f"""
Create a complete piece of content using these details:

Content type: {content_type}
Platform: {platform}
Topic: {topic}
Target audience: {audience}
Tone: {tone}
Extra instructions: {extra_instructions or "None"}

Return the result in this exact structure:

Title:
[short title]

Post:
[complete ready-to-publish content]

Caption:
[short caption]

Hashtags:
[5 to 10 relevant hashtags]

Do not add explanations outside this structure.
"""

    with st.spinner("Generating content..."):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful social media and content writing assistant.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=900,
            )

            result = response.choices[0].message.content
            st.success("Content generated successfully!")
            st.markdown(result)

            st.download_button(
                label="Download content",
                data=result,
                file_name="generated_content.txt",
                mime="text/plain",
                use_container_width=True,
            )

        except Exception as error:
            st.error(f"An error occurred: {error}")
