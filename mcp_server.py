from mcp.server.fastmcp import FastMCP
import httpx

# Initialize the FastMCP server
mcp = FastMCP("MultiAgentServer")

# --- Agent 1: Weather Agent ---
@mcp.tool()
async def get_weather(location: str, date: str = "today") -> str:
    """
    Fetches weather for a specific location and date/time.
    Args:
        location: City or region name.
        date: The day to check (e.g., 'today', 'tomorrow', or '2026-05-10').
    """
    # Using wttr.in (a free, no-key weather API)
    url = f"https://wttr.in/{location}?format=3"
    if date != "today":
        url = f"https://wttr.in/{location}?0&format=4" # simplified forecast
        
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return f"Weather for {location} ({date}): {response.text.strip()}"
        return f"Could not retrieve weather for {location}."

# --- Agent 2: Calculator Agent ---
@mcp.tool()
def calculate(operation: str, a: float, b: float) -> str:
    """
    Performs basic math operations: plus, minus, multiplication, division.
    Args:
        operation: One of 'add', 'subtract', 'multiply', 'divide'.
        a: First number.
        b: Second number.
    """
    if operation == "add":
        return f"Result: {a + b}"
    elif operation == "subtract":
        return f"Result: {a - b}"
    elif operation == "multiply":
        return f"Result: {a * b}"
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero is not allowed."
        return f"Result: {a / b}"
    else:
        return "Invalid operation. Use add, subtract, multiply, or divide."

if __name__ == "__main__":
    mcp.run()
    