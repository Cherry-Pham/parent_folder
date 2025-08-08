"""
Structured Info Agent with Output Schema
"""
import json
from google.adk.agents import LlmAgent
from schemas.base_schemas import CountryInput, CapitalInfoOutput

MODEL_NAME = "gemini-2.0-flash"

def create_structured_info_agent():
    """Creates and returns a structured info agent that uses output schema."""
    return LlmAgent(
        model=MODEL_NAME,
        name="structured_info_agent_schema",
        description="Provides capital and estimated population in a specific JSON format.",
        instruction=f"""You are an agent that provides country information.
The user will provide the country name in a JSON format like {{"country": "country_name"}}.
Respond ONLY with a JSON object matching this exact schema:
{json.dumps(CapitalInfoOutput.model_json_schema(), indent=2)}
Use your knowledge to determine the capital and estimate the population. Do not use any tools.
""",
        input_schema=CountryInput,
        output_schema=CapitalInfoOutput,
        output_key="structured_info_result",
    )
