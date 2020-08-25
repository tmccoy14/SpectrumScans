"""standard library"""
import os

"""third party modules"""
import click

"""internal dataio modules"""
from src.main import pass_environment, VERSION
from src.lib.subprocess import Command


@click.command("scan", short_help="Scan Docker image.")
@click.option(
    "--image", "-i", required=True, help="Docker image name.",
)
@click.option(
    "--tag", "-t", required=False, help="Docker image tag.",
)
@click.option("--export", "-e", required=False, help="Export scan findings.")
@pass_environment
def cli(ctx, image, tag):
    """scancli scans the provided Docker image for vulnerability findings.
    Ex. scancli scan --image image/name --tag 0.0.0"""

    # Setup subprocesses for all of our tools
    docker = Command("docker")
    curl = Command("curl")

    ctx.log("Scanning Docker Image...")

    # Format Docker pull command with image and tag if provided
    if image and tag:
        image_name = "{}:{}".format(image, tag)
        docker_cmd = "pull {}:{}".format(image_name)
    else:
        image_name = "{}:latest".format(image)
        docker_cmd = "pull {}".format(image_name)

    # Run Docker pull command
    process = docker.prefix_run(docker_cmd)
    output, error = process.communicate()
    if process.returncode != 0:
        ctx.log("Failed to pull Docker image", level="error")
        ctx.log("%s" % error.decode("utf-8"))
        raise click.UsageError("Ensure correct image and tag was provided.")
    ctx.vlog("%s" % output.decode("utf-8"))

    # Format Anchore scan command with image and tag if provided
    curl_cmd = "-s https://ci-tools.anchore.io/inline_scan-v0.6.0 | bash -s -- -f -r {}".format(
        image_name
    )

    # Run Anchore Docker image scan command
    process = curl.prefix_run(curl_cmd)
    output, error = process.communicate()
    if process.returncode != 0:
        ctx.log("Failed to pull Docker image", level="error")
        ctx.log("%s" % error.decode("utf-8"))
        raise click.UsageError("Ensure correct image and tag was provided.")
    ctx.vlog("%s" % output.decode("utf-8"))

    # TODO -- Format output of Anchore scan
