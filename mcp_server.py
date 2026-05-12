from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(name="Multiply MCP Server")

@mcp.tool
def multiply(a: float, b: float) -> float:
    """add two numbers."""
    return a + b

if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0", port=8000)