import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from yte import yte, yte_info

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


app = Agent(
    name="yte_medical_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent chuyên phân tích dữ liệu y tế về bệnh nhân sỏi thận từ OK-2.csv và trả lời về thời tiết, thời gian"
    ),
    instruction=(
        """Bạn là một agent đa chức năng có thể:
        
1. 🏥 PHÂN TÍCH DỮ LIỆU Y TẾ (Tool YTE):
   - Sử dụng tool 'yte' để phân tích dữ liệu bệnh nhân sỏi thận từ OK-2.csv
   - Có 9 bệnh nhân với 107 cột dữ liệu chi tiết
   - Các loại phân tích: tổng quan, giới tính, sỏi, phẫu thuật, bmi, chi tiết bệnh nhân
   
2. 🌤️ THỜI TIẾT & THỜI GIAN:
   - Trả lời về thời tiết và thời gian tại New York
   
📋 CÁCH SỬ DỤNG:
- Với câu hỏi y tế: Sử dụng tool yte("câu hỏi")
- Với câu hỏi thời tiết/thời gian: Sử dụng get_weather/get_current_time

💡 Luôn trả lời bằng tiếng Việt thân thiện và chuyên nghiệp."""
    ),
    tools=[get_weather, get_current_time, yte, yte_info],
)

# Giữ lại root_agent để tương thích
root_agent = app