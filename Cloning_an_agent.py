from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled , ModelSettings , Handoff, function_tool
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
import dotenv, os
from dotenv import load_dotenv, find_dotenv
import asyncio

_=load_dotenv(find_dotenv())
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

#client setup
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
set_tracing_disabled(disabled=True)
@function_tool
def get_weather(city: str) -> str:
    # Simulating a real API call
    fake_weather_data = {
        "London": "The weather in London is sunny.",
        "Paris": "The weather in Paris is rainy."
    }
    return fake_weather_data.get(city, "Weather data not available.")

async def main():
    # Create a base agent
    base_agent = Agent(
        name="BaseAssistant",
        instructions="You are a helpful (assistant.",
        model=OpenAIChatCompletionsModel(model="gemini-2.5-flash",openai_client=client),
        model_settings=ModelSettings(temperature=0.7)
    )

    # Create multiple specialized variants
    agents = {
        "Creative": base_agent.clone(
            name="CreativeWriter",
            instructions="You are a creative writer. Use vivid language.",
            model_settings=ModelSettings(temperature=0.9)
        ),
        "Precise": base_agent.clone(
            name="PreciseAssistant", 
            instructions="You are a precise assistant. Be accurate and concise.",
            model_settings=ModelSettings(temperature=0.1)
        ),
        "Friendly": base_agent.clone(
            name="FriendlyAssistant",
            instructions="You are a very friendly assistant. Be warm and encouraging."
        ),
        "Professional": base_agent.clone(
            name="ProfessionalAssistant",
            instructions="You are a professional assistant. Be formal and business-like."
        )
    }

    # Test all variants
    query = "Tell me about artificial intelligence."

    for name, agent in agents.items():
        result = await Runner.run(agent, query)
        print(f"\n{name} Agent:")
        print(result.final_output[:100] + "...")

asyncio.run(main())