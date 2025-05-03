import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_mcq_from_file(file_path, num_questions=5):
    # Upload the file
    with open(file_path, "rb") as f:
        upload = openai.files.create(file=f, purpose="assistants")
        file_id = upload.id

    # Now send the prompt using that file
    prompt = f"""You are a tutor. Generate {num_questions} multiple choice questions based on the content of the uploaded file.
Each question should have 4 answer options and clearly indicate the correct answer.

Format:
Q: Question here
A. Option A
B. Option B
C. Option C
D. Option D
Answer: B
"""

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",  # supports file inputs
        messages=[
            {"role": "user", "content": prompt}
        ],
        tools=[{"type": "file_search"}],  # This enables GPT to use uploaded file
        tool_choice="auto",
        file_ids=[file_id],
    )

    return response.choices[0].message["content"]
