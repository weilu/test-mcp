# Test MCP

A minimal MCP (Model Context Protocol) server for testing.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run locally:
   ```bash
   uvicorn app:app --reload
   ```

## Endpoints

- `/mcp` - MCP protocol endpoint (Streamable HTTP)
- `/healthz` - Health check

## MCP Tool

### `budget_summary`

Returns dummy budget summary data for testing purposes.

**Parameters:**
- `country_name` (required): Country name
- `year` (required): Budget year
- `admin0` (optional): Administrative level 0 filter
- `func` (optional): Functional classification filter
- `econ` (optional): Economic classification filter
- `geo0` (optional): Geographic level 0 filter

**Returns:** Dummy budget metrics (approved, revised, executed, execution_rate)
