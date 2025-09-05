import os
import subprocess
from mcp.server.fastmcp import FastMCP

# Initialize MCP server for Docker management
mcp = FastMCP("docker-manager")

def run_command(cmd: list) -> dict:
    """Helper to run shell commands and return output/errors."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True
        )
        return {"result": result.stdout.strip(), "text": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {
            "result": e.stderr.strip(),
            "text": f"❌ Command failed: {' '.join(cmd)}\n{e.stderr.strip()}"
        }

# ---- MCP TOOLS ----

@mcp.tool()
def docker_version() -> dict:
    """Get Docker version info."""
    return run_command(["docker", "--version"])


@mcp.tool()
def list_containers(all: bool = False) -> dict:
    """List Docker containers (running by default, all if `all=True`)."""
    cmd = ["docker", "ps"]
    if all:
        cmd.append("-a")
    return run_command(cmd)


@mcp.tool()
def list_images() -> dict:
    """List available Docker images."""
    return run_command(["docker", "images"])


@mcp.tool()
def build_image(tag: str, path: str = ".") -> dict:
    """Build a Docker image with a given tag and path (default current dir)."""
    return run_command(["docker", "build", "-t", tag, path])


@mcp.tool()
def run_container(name: str, image: str, mount_host: str = "", mount_container: str = "", interactive: bool = True) -> dict:
    """
    Run a Docker container.
    - `name`: container name
    - `image`: image to run
    - `mount_host`: optional local path to mount
    - `mount_container`: optional path inside container
    - `interactive`: run with -it or detached (-d)
    """
    cmd = ["docker", "run", "--name", name]
    if mount_host and mount_container:
        cmd += ["-v", f"{mount_host}:{mount_container}"]
    cmd.append("-it" if interactive else "-d")
    cmd.append(image)
    return run_command(cmd)


@mcp.tool()
def stop_container(name: str) -> dict:
    """Stop a running container."""
    return run_command(["docker", "stop", name])


@mcp.tool()
def remove_container(name: str, force: bool = False) -> dict:
    """Remove a container by name."""
    cmd = ["docker", "rm"]
    if force:
        cmd.append("-f")
    cmd.append(name)
    return run_command(cmd)


@mcp.tool()
def remove_image(tag: str, force: bool = False) -> dict:
    """Remove a Docker image by tag."""
    cmd = ["docker", "rmi"]
    if force:
        cmd.append("-f")
    cmd.append(tag)
    return run_command(cmd)


if __name__ == "__main__":
    mcp.run()
