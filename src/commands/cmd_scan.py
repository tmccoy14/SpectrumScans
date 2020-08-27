"""standard library"""
import os

"""third party modules"""
import click

"""internal dataio modules"""
from src.main import pass_environment, VERSION
from src.lib.subprocess import Command
from src.lib import vulnerability_color


@click.command("scan", short_help="Scan Docker image.")
@click.option(
    "--image", "-i", required=True, help="Docker image name.",
)
@click.option(
    "--tag", "-t", required=False, help="Docker image tag.",
)
@pass_environment
def cli(ctx, image, tag):
    """scancli scans the provided Docker image for vulnerability findings.
    Ex. scancli scan --image image/name --tag 0.0.0"""

    # Setup subprocesses for all of our tools
    curl = Command("curl")

    # Format Docker image name
    if image and tag:
        image_name = "{}:{}".format(image, tag)
    else:
        image_name = "{}:latest".format(image)

    ctx.log("+ Scanning Docker Image...")

    # Format Anchore scan command with image and tag if provided
    curl_cmd = "-s https://ci-tools.anchore.io/inline_scan-v0.6.0 | bash -s -- -f -r {}".format(
        image_name
    )

    # Run Anchore Docker image scan command
    process = curl.run(curl_cmd)

    # Grab stdout line by line as it becomes available
    # This will loop until process terminates
    while process.poll() is None:
        line = process.stdout.readline()
        print(vulnerability_color(line.decode("utf-8").rstrip()))

    output, error = process.communicate()
    if process.returncode != 0:
        ctx.log("%s" % error.decode("utf-8"))
    ctx.vlog("%s" % output.decode("utf-8"))

    ctx.log("✔ Scanned Docker Image...")
