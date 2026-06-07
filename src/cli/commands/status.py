import urllib.request
import json
import typer


class StatusCommand:
  """
  Command to check the connection status of the remote Solomon API.
  """

  def execute(self, url: str | None) -> None:
    """
    Connect to the remote API and verify operational status.
    """
    if not url:
      from cli.config import get_api_host

      url = f"{get_api_host().rstrip('/')}/status"

    typer.echo(f"Connecting to Solomon API at {url}...")
    try:
      req = urllib.request.Request(
        url,
        headers={"User-Agent": "Solomon-CLI/1.0"},
      )
      with urllib.request.urlopen(req, timeout=5) as response:
        if response.status == 200:
          data = json.loads(response.read().decode())
          typer.echo("✅ Connection successful!")
          typer.echo(f"  App:     {data.get('app', 'Unknown')}")
          typer.echo(f"  Version: {data.get('version', 'Unknown')}")
          typer.echo(f"  Status:  {data.get('status', 'Unknown')}")
        else:
          typer.echo(f"❌ API returned status code {response.status}")
          raise typer.Exit(code=1)
    except Exception as e:
      typer.echo(f"❌ Failed to connect to API: {e}")
      raise typer.Exit(code=1)
