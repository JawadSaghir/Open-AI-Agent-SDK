from agents import Runner, Agent, AgentHooks, RunHooks, ModelSettings, OpenAIChatCompletionsModel, RunContextWrapper, set_tracing_disabled
from openai import AsyncOpenAI
from typing import TypeVar, Any
from dataclasses import dataclass
from pydantic import BaseModel
import asyncio
import dotenv, os 
from dotenv import find_dotenv, load_dotenv
_=load_dotenv(find_dotenv( ))
Gemini_api_key=os.getenv("GEMINI_API_KEY")

set_tracing_disabled(disabled=True)

external_client=AsyncOpenAI(
    api_key=Gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class My_context(BaseModel):
    name : str = "ahmed" 
    age : int  = 22

class Agent_lifecycle_hooks(AgentHooks):
    async def on_start(self, context:RunContextWrapper[Any], agent:Agent):
        print(f"{agent.name} Agent is Started")
    async def on_end(self,context:RunContextWrapper[Any], agent, output):
        print("{agent.name} Agent has completed its lifecycle.")


async def main():
    Joker=Agent(
        name="Joker",
        instructions="Act like a joker.  Your task is to make the people laugh. Everytime they ask anything.Give the answer in a funny way.",
        model=OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=external_client
            ),
        model_settings=ModelSettings(
            temperature=0.5,
            top_p=0.7,
            max_tokens=500,
            tool_choice="auto",
            # frequency_penalty=0.5
        ),
        hooks = Agent_lifecycle_hooks(),
        tool_use_behavior="run_llm_again"
    )

    # Define Runner
    Run=await Runner.run(
        starting_agent=Joker,
        input="tell me the joke i can't stop laughing",
        context=My_context,
        )
    output=Run.final_output
    print(output)
asyncio.run(main())
