import subprocess
import typer


class UpdateCommand:
  """
  Command to update the Solomon CLI client to the latest version.
  """

  def execute(self) -> None:
    """
    Download and run the bootstrap CLI script to update the installation.
    """
    typer.echo("🔄 Updating Solomon CLI...")
    cmd = "curl -sSL https://raw.githubusercontent.com/stanleygomes/solomon/refs/heads/master/scripts/bootstrap_cli.sh | bash"
    try:
      result = subprocess.run(cmd, shell=True, check=True)
      if result.returncode == 0:
        typer.echo("✅ Solomon CLI updated successfully!")
      else:
        typer.echo(f"❌ Update failed with return code {result.returncode}")
        raise typer.Exit(code=1)
    except subprocess.CalledProcessError as e:
      typer.echo(f"❌ Update failed with error: {e}")
      raise typer.Exit(code=1)
