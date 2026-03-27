from fastmcp import FastMCP
import random
import json

mcp = FastMCP(name="Simple Calculator Server")

@mcp.tool()
def add(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Args:
        a (float): The first number.
        b (float): The second number.
    
    Returns:
        float: The sum of a and b.
    """
    return a + b

@mcp.tool()
def random_number(min_val: int = 1, max_val: int = 100) -> int:
    """
    Generate a random integer between min_val and max_val.
    
    Args:
        min_val (int): The minimum value (inclusive).
        max_val (int): The maximum value (inclusive).
    
    Returns:
        int: A random integer between min_val and max_val.
    """
    return random.randint(min_val, max_val)

@mcp.resource("info://server")
def server_info():
    """
    Get information about the server.
    
    Returns:
        dict: A dictionary containing server information.
    """
    info = {
        "name": "Simple Calculator Server",
        "version": "1.0.0",
        "description": "A simple server that provides basic calculator functions and random number generation.",
        "tools": ["add", "random_number"],
        "authors": ["Shubham"],
    }

    return json.dumps(info, indent=2)

if __name__ == "__main__":    
    mcp.run(transport="http", host="0.0.0.0", port=8000)