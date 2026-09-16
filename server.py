from mcp.server import MCPServer
import os

mcp = MCPServer("MCP Climatisation")


@mcp.tool()
def watts_vers_btu_h(watts: float) -> float:
    """Convertit des watts en BTU/h."""
    if watts < 0:
        raise ValueError("La puissance doit être positive.")
    return round(watts * 3.412141633, 2)


@mcp.tool()
def btu_h_vers_watts(btu_h: float) -> float:
    """Convertit des BTU/h en watts."""
    if btu_h < 0:
        raise ValueError("La puissance doit être positive.")
    return round(btu_h / 3.412141633, 2)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port
    )
