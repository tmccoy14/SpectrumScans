"""standard library"""
import os

"""third party modules"""
import click

"""internal dataio modules"""
from src.main import pass_environment, VERSION
from src.lib.subprocess import Command
from src.lib import check_image


@click.command("pull", short_help="Pull Docker image.")
@click.option(
    "--image", "-i", required=True, help="Docker image name.",
)
@click.option(
    "--tag", "-t", required=False, help="Docker image tag.",
)
@pass_environment
def cli(ctx, image, tag):
    """scancli pulls the provided Docker image if it doesn't exist locally for vulnerability findings.
    Ex. scancli pull --image image/name --tag 0.0.0"""

    # Setup subprocesses for all of our tools
    docker = Command("docker")

    # Format Docker pull command with image and tag if provided
    if image and tag:
        image_name = "{}:{}".format(image, tag)
    else:
        image_name = "{}:latest".format(image)

    # Check if Docker image exists locally
    image_exists = check_image(ctx, docker, image_name)

    if image_exists:
        ctx.log("Docker image exists locally already!")
    else:
        ctx.log("+ Pulling Docker Image...")

        docker_cmd = "pull {}".format(image_name)

        # Run Docker pull command
        process = docker.run(docker_cmd)

        # Grab stdout line by line as it becomes available
        # This will loop until process terminates
        while process.poll() is None:
            line = process.stdout.readline()
            print(line.decode("utf-8").rstrip())

        output, error = process.communicate()
        if process.returncode != 0:
            ctx.log("Failed to pull Docker image", level="error")
            ctx.log("%s" % error.decode("utf-8"))
            raise click.UsageError("Ensure correct image and tag was provided.")
        ctx.vlog("%s" % output.decode("utf-8"))

        ctx.log("✔ Pulled Docker Image...")
