import openai
import os
import time
from dotenv import load_dotenv

load_dotenv()
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

def generate_mcq_from_file(file_path, num_questions=5):
    # Upload file to OpenAI
    with open(file_path, "rb") as f:
        file_obj = client.files.create(file=f, purpose="assistants")

    # Create assistant with file_search tool
    assistant = client.beta.assistants.create(
        name="Quiz Generator",
        instructions=(
            f"Read the uploaded file and generate {num_questions} multiple-choice questions. "
            "For each question, follow this exact format:\n\n"
            "Q1. <question text>\n"
            "A. <option A>\n"
            "B. <option B>\n"
            "C. <option C>\n"
            "D. <option D>\n"
            "Answer: <correct letter>\n\n"
            "Use this format for all questions, incrementing the number for each question (Q2, Q3, etc.)."
            "DO NOT BEGIN THE OUTPUT WITH ANYTHING BUT THE START OF THE FIRST QUESTION"
            "DO NOT PUT '【4:0†facts.pdf】' AT THE END OF EACH ANSWER"
        ),
        model="gpt-4o",
        tools=[{"type": "file_search"}]
    )

    # Create a new thread
    thread = client.beta.threads.create()

    # Post user message with file attached correctly
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Generate a quiz from the uploaded file.",
        attachments=[{"file_id": file_obj.id, "tools": [{"type": "file_search"}]}]
    )

    # Start a run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # Wait for completion
    while run.status not in ["completed", "failed", "cancelled"]:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Return result
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value
