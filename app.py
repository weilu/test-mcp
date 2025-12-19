import os
import pandas as pd
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="BOOST MCP")

mcp = FastMCP("boost-mcp")

SERVER_HOSTNAME = os.getenv("DATABRICKS_SERVER_HOSTNAME")

def credentials_provider():
    config = Config(
        host = f"https://{SERVER_HOSTNAME}",
        client_id     = os.getenv("DATABRICKS_CLIENT_ID"),
        client_secret = os.getenv("DATABRICKS_CLIENT_SECRET"))
    return oauth_service_principal(config)


def execute_query(query):
    with sql.connect(
        server_hostname = SERVER_HOSTNAME,
        http_path = os.getenv("DATABRICKS_HTTP_PATH"),
        credentials_provider=credentials_provider,
    ) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        df = cursor.fetchall_arrow().to_pandas()
    return df


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
    Query budget summary data from Databricks with optional filters.
    """
    conditions = [f"country_name = '{country_name}'", f"year = {year}"]

    if admin0:
        conditions.append(f"admin0 = '{admin0}'")
    if func:
        conditions.append(f"func = '{func}'")
    if econ:
        conditions.append(f"econ = '{econ}'")
    if geo0:
        conditions.append(f"geo0 = '{geo0}'")

    where_clause = " AND ".join(conditions)

    query = f"""
        SELECT
            SUM(approved) as approved,
            SUM(revised) as revised,
            SUM(executed) as executed
        FROM prd_mega.boost.boost_gold
        WHERE {where_clause}
    """

    df = execute_query(query)

    if df.empty or df.iloc[0]['approved'] is None:
        return {
            "filters": {
                "country_name": country_name,
                "year": year,
                "admin0": admin0,
                "func": func,
                "econ": econ,
                "geo0": geo0,
            },
            "approved": 0.0,
            "revised": 0.0,
            "executed": 0.0,
            "execution_rate": 0.0,
            "note": "No data found for the given filters.",
        }

    row = df.iloc[0]
    approved = float(row['approved']) if pd.notna(row['approved']) else 0.0
    revised = float(row['revised']) if pd.notna(row['revised']) else 0.0
    executed = float(row['executed']) if pd.notna(row['executed']) else 0.0
    execution_rate = executed / revised if revised > 0 else 0.0

    return {
        "filters": {
            "country_name": country_name,
            "year": year,
            "admin0": admin0,
            "func": func,
            "econ": econ,
            "geo0": geo0,
        },
        "approved": approved,
        "revised": revised,
        "executed": executed,
        "execution_rate": execution_rate,
    }

# 4) Mount the MCP Streamable HTTP app at /mcp
# This exposes the MCP protocol over HTTP for Claude/clients.
mcp_asgi_app = mcp.streamable_http_app()
app.mount("/mcp", mcp_asgi_app)

# Optional: a simple health check for debugging / Connect monitoring
@app.get("/healthz")
async def healthz():
    return {"ok": True}

@app.get("/test/budget_summary")
async def test_budget_summary(
    country_name: str = "Kenya",
    year: int = 2023,
    admin0: str | None = None,
    func: str | None = None,
    econ: str | None = None,
    geo0: str | None = None,
):
    """Test endpoint to call budget_summary directly via HTTP GET"""
    return await budget_summary(country_name, year, admin0, func, econ, geo0)

