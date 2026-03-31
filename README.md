# Test MCP

A minimal MCP (Model Context Protocol) server that exposes data from Databricks.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file with your Databricks credentials:
   ```
   DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
   DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
   DATABRICKS_CLIENT_ID=your-client-id
   DATABRICKS_CLIENT_SECRET=your-client-secret
   ```

3. Run locally:
   ```bash
   uvicorn app:app --reload
   ```

## Endpoints

- `/mcp` - MCP protocol endpoint (Streamable HTTP)
- `/healthz` - Health check
- `/test/budget_summary` - HTTP test endpoint for the budget_summary tool

## MCP Tool

### `budget_summary`

Query budget summary data from the BOOST database.

**Parameters:**
- `country_name` (required): Country name
- `year` (required): Budget year
- `admin0` (optional): Administrative level 0 filter
- `func` (optional): Functional classification filter
- `econ` (optional): Economic classification filter
- `geo0` (optional): Geographic level 0 filter

**Returns:** Budget metrics (approved, revised, executed, execution_rate)

## Deployment

Deploy to Posit Connect:
```bash
rsconnect deploy fastapi -n posit-connect app:app
```
