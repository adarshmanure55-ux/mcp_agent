
import gradio as gr
import asyncio
import re
from mcp_client import MCPClient

# Initialize the persistent client
client = MCPClient()

async def chat_handler(message, history):
    """
    Main chat function. 
    'message' is the current user input.
    'history' is the list of previous messages (handled by Gradio).
    """
    text = message.lower()
    
    try:
        # --- Calculator Detection ---
        if any(op in text for op in ["+", "-", "*", "/", "plus", "minus", "times", "divide"]):
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
            if len(numbers) >= 2:
                a, b = float(numbers[0]), float(numbers[1])
                op = "add"
                if "-" in text or "minus" in text: op = "subtract"
                elif "*" in text or "times" in text or "multiply" in text: op = "multiply"
                elif "/" in text or "divide" in text: op = "divide"
                
                result = await client.call_tool("calculate", {"operation": op, "a": a, "b": b})
                return f"🔢 {result}"
            else:
                return "I detected a math request. Please provide two numbers (e.g., '12 + 4')."

        # --- Weather Detection ---
        if any(word in text for word in ["weather", "temp", "forecast", "hot", "cold"]):
            city = "London" 
            if "in " in text:
                city = text.split("in ")[-1].strip("?").strip()
            elif len(text.split()) > 1:
                city = text.split()[-1].strip("?").strip()
                
            result = await client.call_tool("get_weather", {"location": city, "date": "today"})
            return f"🌦️ {result}"

        return "I'm your MCP Assistant! Try asking 'Weather in Paris' or 'Calculate 50 * 2'."

    except Exception as e:
        return f"❌ Error: {str(e)}"

# Launching the Chat Interface
demo = gr.ChatInterface(
    fn=chat_handler,
    title="MCP Multi-Agent Assistant",
    description="Ask me about the weather or perform calculations. I'll remember our conversation history below!",
    examples=["What is 15 + 25?", "Weather in Tokyo", "Multiply 12 by 12", "Is it hot in Dubai?"],
)

if __name__ == "__main__":
    demo.launch()