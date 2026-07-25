import subprocess
import typer


class UpdateCommand:
  """
  Command to update Solomon to the latest version by re-running the bootstrap script.
  The bootstrap is idempotent: it pulls the latest code, refreshes deps, updates the
  shell alias, re-seeds the database, and restarts the cron daemon only if not running.
  """

  BOOTSTRAP_URL = "https://raw.githubusercontent.com/stanleygomes/solomon/refs/heads/master/scripts/bootstrap.sh"

  def execute(self) -> None:
    """
    Download and run the bootstrap script to update the full Solomon installation.
    """
    typer.echo("🔄 Updating Solomon...")
    cmd = f"curl -sSL {self.BOOTSTRAP_URL} | bash"
    try:
      result = subprocess.run(cmd, shell=True, check=True)
      if result.returncode == 0:
        typer.echo("✅ Solomon updated successfully!")
      else:
        typer.echo(f"❌ Update failed with return code {result.returncode}")
        raise typer.Exit(code=1)
    except subprocess.CalledProcessError as e:
      typer.echo(f"❌ Update failed: {e}")
      raise typer.Exit(code=1)
