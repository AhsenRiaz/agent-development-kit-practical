import uuid
import asyncio
import os

from dotenv import load_dotenv, dotenv_values, find_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

# Find the .env file inside the question_answering_agent folder
env_path = find_dotenv("question_answering_agent/.env")
load_dotenv(env_path)
env_vars = dotenv_values(env_path)
print("Loaded variables from .env file:")
for key, value in env_vars.items():
    print(f"env variables = {key}={value}")

async def main():

    # in memory session state
    session_service_stateful = InMemorySessionService()

    initial_state = {
        "user_name": "Muhammad Ahsan Riaz",
        "user_preferences": """
            I like to play Football, Counter-Strike..
            My favorite TV show is Dexter.
            Likes to develop anything using AI.
        """,
    }

    APP_NAME = "Know You"
    USER_ID = "m_ahs_rz"
    SESSION_ID = str(uuid.uuid4())

    stateful_session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )

    print("CREATED NEW SESSION:")
    print(f"\tSession ID: {SESSION_ID}")

    runner = Runner(
        agent=question_answering_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful
    )

    new_message = types.Content(
        role="user",
        parts=[types.Part(text="What is Ahsan's favourite TV show?")]
    )

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"Final Response , {event.content.parts[0].text}")

    print("==== Session Event Exploration ====")
    session = await session_service_stateful.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    print(f'Session Caught, {session}')

asyncio.run(main())