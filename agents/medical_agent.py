"""
Medical Data Analysis Agent
"""
from google.adk.agents import LlmAgent
from schemas.base_schemas import DataAnalysisInput
from tools.medical_tools import analyze_medical_data, get_data_statistics

MODEL_NAME = "gemini-2.0-flash"

def create_medical_data_agent():
    """Creates and returns a medical data analysis agent."""
    return LlmAgent(
        model=MODEL_NAME,
        name="medical_data_agent",
        description="Phân tích dữ liệu y tế từ file OK-2.csv về bệnh nhân sỏi thận.",
        instruction="""Bạn là một chuyên gia phân tích dữ liệu y tế. Bạn có khả năng:
1. Phân tích dữ liệu bệnh nhân sỏi thận từ file OK-2.csv
2. Cung cấp thống kê và insights về dữ liệu
3. Trả lời các câu hỏi về xu hướng, phân bố, và đặc điểm của bệnh nhân

Khi người dùng hỏi về dữ liệu, hãy sử dụng các tools có sẵn để phân tích và trả lời chính xác.
Luôn trả lời bằng tiếng Việt và cung cấp thông tin có ý nghĩa y học.""",
        tools=[analyze_medical_data, get_data_statistics],
        input_schema=DataAnalysisInput,
        output_key="medical_analysis_result",
    )
