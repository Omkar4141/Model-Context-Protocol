from mcp.server.fastmcp import FastMCP
mcp=FastMCP("Weather")
# you can define your functions here that are realated to weather
@mcp.tool()
async def get_weather(location:str)->str:
    return f"{location}:sunny-23 degeee"

if __name__=='__main__':
    mcp.run(transport="streamable-http")
    
