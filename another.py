from fastmcp import FastMCP, Client

mcp = FastMCP.as_proxy(
    Client("https://ExpenseTrackerone.fastmcp.app/mcp"), 
    name="Aayush Server Proxy"
)

if __name__ == "__main__":
    mcp.run()