import time
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

agents = {
    "triage_agent": {
        "id": "asst_SZP3IHrndmnRLtgSTIbbdGmO"
    }
}

# Create the assistant with the tools (functions)
# assistant = client.beta.assistants.create(
#     instructions="You are a knowledgeable assistant. Use the provided functions to answer questions.",
#     model="gpt-4o",
#     tools=[
#         {
#             "type": "function", 
#             "function": {
#                 "name": "get_current_temperature",
#                 "description": "Get the current temperature for a specific location",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "location": {
#                             "type": "string",
#                             "description": "The city and state, e.g., San Francisco, CA"
#                         },
#                         "unit": {
#                             "type": "string",
#                             "enum": ["Celsius", "Fahrenheit"],
#                             "description": "The temperature unit to use."
#                         }
#                     },
#                     "required": ["location", "unit"]
#                 }
#             }
#         },
#         {
#             "type": "function",
#             "function": {
#                 "name": "get_rain_probability",
#                 "description": "Get the probability of rain for a specific location",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "location": {
#                             "type": "string",
#                             "description": "The city and state, e.g., San Francisco, CA"
#                         }
#                     },
#                     "required": ["location"]
#                 }
#             }
#         }
#     ]
# )

thread = client.beta.threads.create()

def contact_medical_doctor(doctor_speciality, description, doctors):
    for doctor in doctors:
        print("the doctor is", doctor)
        if doctor.speciality == doctor_speciality:
            doctor.set_pending_move(description)
            print(f"Dr. {doctor_speciality} has been notified and is approaching you.")
            return f"Dr. {doctor_speciality} has been notified and is approaching you."
    return f"Dr. {doctor_speciality} not found."


def call_ai_assistant(question, doctors, instructions="Please always be concise in your answer. Address the user as Sim the patient."):

    try:
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question    
        )
        
        # Initiate a run with the assistant
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            #assistant_id=assistant.id,
            instructions=instructions,
            assistant_id="asst_SZP3IHrndmnRLtgSTIbbdGmO"
        )

        # Check if the run requires tool outputs
        if run.status == 'requires_action':
            tool_outputs = []
            
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                if tool_call.function.name == "fetch_doctor":
                    print("we are fetching the doctor")
                    # Simulate a response from the get_rain_probability function
                    # get the doctor
                    arguments = tool_call.function.arguments
                    # parse the arguments as json
                    arg_json = json.loads(arguments)
                    speciality = arg_json["speciality"]
                    medical_condition = arg_json["medical_condition"]
                    # get the doctors from the game state

                    contact_medical_doctor(speciality, medical_condition, doctors)

                    ## fetch the doctor

                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": '{"probability": "0.2"}'
                    })

            # Submit all tool outputs at once
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        # Retrieve the assistant's response after tool outputs have been submitted
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            assistant_message = next(msg for msg in messages if msg.role == 'assistant')
            full_response = assistant_message.content[0].text.value
            return full_response
        else:
            return f"Run did not complete successfully: {run.status}"

    except Exception as e:
        print(f"Error in AI call: {str(e)}")
        return "I'm sorry, I couldn't process that request."

# Example of using the function
# response = call_ai_assistant("What's the weather in San Francisco today and the likelihood it'll rain?")
# print(response)