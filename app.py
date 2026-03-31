from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP

app = FastAPI(title="Test MCP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://claude.ai", "https://*.anthropic.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mcp = FastMCP("test-mcp")


@mcp.tool()
async def budget_summary(
    country_name: str,
    year: int,
    admin0: str | None = None,
    func: str | None = None,
    econ: str | None = None,
    geo0: str | None = None,
) -> dict:
    """
    Returns dummy budget summary data for testing purposes.
    """
    return {
        "note": "This is dummy data for testing purposes only.",
        "filters": {
            "country_name": country_name,
            "year": year,
            "admin0": admin0,
            "func": func,
            "econ": econ,
            "geo0": geo0,
        },
        "approved": 1000000.0,
        "revised": 950000.0,
        "executed": 875000.0,
        "execution_rate": 0.92,
    }


mcp_asgi_app = mcp.streamable_http_app()
app.mount("/mcp", mcp_asgi_app)


@app.get("/healthz")
async def healthz():
    return {"ok": True}


