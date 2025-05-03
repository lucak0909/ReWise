from openai import OpenAI
import os
from dotenv import load_dotenv
import time

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_mcq_from_file(file_path, num_questions=5):
    # 1. Upload file
    with open(file_path, "rb") as f:
        file_upload = client.files.create(file=f, purpose="assistants")

    # 2. Create assistant with file access
    assistant = client.beta.assistants.create(
        name="Quiz Generator",
        instructions=f"""You are a quiz-generating tutor. Read the uploaded file and generate {num_questions} multiple choice questions. 
Each question should have 4 options (A-D) and the correct answer labeled.

Format:
Q: Question text
A. Option A
B. Option B
C. Option C
D. Option D
Answer: C
""",
        model="gpt-4-1106-preview",
        tools=[{"type": "file_search"}]
    )

    # 3. Start a thread (session)
    thread = client.beta.threads.create()

    # 4. Send a message to trigger the assistant
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Generate a quiz from the uploaded file.",
        file_ids=[file_upload.id]
    )

    # 5. Run the assistant on the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # 6. Poll until complete
    while run.status not in ["completed", "failed", "cancelled"]:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # 7. Fetch the response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    reply = messages.data[0].content[0].text.value
    return reply
