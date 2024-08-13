import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)
thread = client.beta.threads.create()

def call_ai_assistant(question):
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )
        
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_SZP3IHrndmnRLtgSTIbbdGmO",
            instructions="Please address the user as Jane Doe. The user has a premium account."
        )
        
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status == 'completed':
                break
            time.sleep(1)  # Wait for a second before checking again
        
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_message = next(msg for msg in messages if msg.role == 'assistant')
        full_response = assistant_message.content[0].text.value
        
        return full_response
    except Exception as e:
        print(f"Error in AI call: {str(e)}")
        return "I'm sorry, I couldn't process that request."