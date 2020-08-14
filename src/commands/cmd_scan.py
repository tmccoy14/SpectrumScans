"""standard library"""
import os

"""third party modules"""
import click

"""internal dataio modules"""
from src.main import pass_environment, VERSION


@click.command("scan", short_help="Scan Docker image.")
@click.option(
    "--image", required=True, help="Docker image name.",
)
@click.option(
    "--tag", required=False, help="Docker image tag.",
)
@pass_environment
def cli(ctx, image, tag):
    """Scancli scans the provided Docker image for vulnerability findings.
    Ex. scancli scan --image image/name --tag 0.0.0"""

    ctx.log("Scanning Docker Image...")
