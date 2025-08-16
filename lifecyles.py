from agents import (
    Runner, Agent, AgentHooks, RunHooks,
    ModelSettings, OpenAIChatCompletionsModel,
    RunContextWrapper, set_tracing_disabled, 
    function_tool,
    )
from agents.extensions.visualization import draw_graph
from openai import AsyncOpenAI
from typing import TypeVar, Any
from dataclasses import dataclass
from pydantic import BaseModel
import asyncio
import dotenv, os 
import pyjokes 

from dotenv import find_dotenv, load_dotenv
_=load_dotenv(find_dotenv( ))

Gemini_api_key=os.getenv("GEMINI_API_KEY")

set_tracing_disabled(disabled=True)

external_client=AsyncOpenAI(
    api_key=Gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
@dataclass
class My_context:
    name : str  
    age : int  

class Agent_lifecycle_hooks(AgentHooks):
    async def on_start(self, ctx:RunContextWrapper[Any], agent:Agent):
        print(f"{agent.name} Agent is Started. Your details are {ctx.context.name} ")
    async def on_end(self,context:RunContextWrapper[Any], agent, output):
        print(f"{agent.name} Agent has completed its lifecycle.")

class Run_lifecycle_hooks(RunHooks):
    async def on_agent_start(self,context:RunContextWrapper[Any],agent:Agent):
        print("======Run lifecycle has been started======")
    async def on_agent_end(self, context:RunContextWrapper, agent:Agent, output:Any):
        print("=====The Runner Agent lifecycle has ended ======")
        
@function_tool
def joke_teller() ->str:
   print("---Tool is called-----")
   return pyjokes.get_jokes()

async def main():
    Joker=Agent(
        name="Joker",
        instructions="Act like a joker.  Your task is to make the people laugh. Everytime they ask anything.Give the answer in a funny way.Everytime user ask the joker give the different joke and use different strategy",
        model=OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=external_client
            ),
        model_settings=ModelSettings(
            temperature=0.7,
            top_p=0.6,
            max_tokens=500,
            tool_choice="required",#if i put it on auto it will decide on the basis of instructions and what it understand
            # frequency_penalty=0.5
        ),
        hooks = Agent_lifecycle_hooks(),
        tools=[joke_teller],
        tool_use_behavior="auto"
    )
    test_data = My_context(name="ahmed",age=21)
    # Define Runner
    Run=await Runner.run(
        starting_agent=Joker,
        input="tell me the joke i can't stop laughing",
        context=test_data,#this context will not be passed to LLM. This context is used by agent.
        hooks=Run_lifecycle_hooks() # this must be callable
        )
    p=Run_lifecycle_hooks().__dict__
    print(f"=================================={p}=========================")
    output=Run.final_output
    print(output)
    draw_graph(Joker,filename="graph")
asyncio.run(main())
