"""standard library"""
import os
import json
import requests

"""third party modules"""
import click
import boto3
from botocore.exceptions import ClientError

"""internal dataio modules"""
from src.main import pass_environment, VERSION
from src.lib import (
    path_leaf,
    check_bucket_exists,
    read_table_schema,
    run_bash,
    write_scratch_space_state,
    get_secret,
)
from src.lib.ranger import (
    create_policy,
    create_user,
    get_policy_users,
    update_catalog_users,
)


@click.command("create", short_help="Create dataio scratch space.")
@click.option(
    "--dataset",
    required=True,
    help="Path to dataset file.",
    type=click.Path(exists=True),
)
@click.option(
    "--schema",
    required=True,
    help="Path to table schema definition file.",
    type=click.Path(exists=True),
)
@click.option("--bucket", help="S3 bucket name.")
@click.option("--scratch_space", help="Scratch space name.")
@pass_environment
def cli(ctx, dataset, schema, bucket, scratch_space):
    """Dataio create automates the creation of a scratch space.
    Ex. dataio create --dataset path/to/dataset.csv --schema path/to/schema.sql"""

    # get the files provided from the path
    extracted_file = path_leaf(dataset)

    # get name of s3 bucket for sratch space
    # create s3 client
    # ensure bucket provided exists and user has access
    if bucket is None:
        bucket_name = click.prompt(text="What is the name of the S3 bucket?",)
    else:
        bucket_name = bucket
    s3 = boto3.client("s3")
    check_bucket_exists(ctx, s3, bucket_name)

    # get scratch space folder name for s3 bucket
    if scratch_space is None:
        folder = click.prompt(text="What is the name of your scratch space?",)
    else:
        folder = scratch_space

    # create s3 bucket url
    s3_url = "s3://{0}/{1}/{2}".format(bucket_name, folder, extracted_file)

    ctx.log("+ Preparing your scratch space {0}...".format(s3_url))

    # upload file to the bucket
    try:
        s3.upload_file(dataset, bucket_name, "{}/{}".format(folder, extracted_file))
    except:
        ctx.log(
            "Could not upload {0}/{1} to S3 bucket {3}.".format(
                folder, extracted_file, bucket_name
            ),
            level="error",
        )
        raise click.UsageError("Failed to create scratch space.")

    # get the dataset table schema provided
    schema_statement = read_table_schema(schema)

    # get the emr ssh environment variable
    if os.getenv("EMR_CONNECTION_STRING") is not None:
        emr_connection_string = os.getenv("EMR_CONNECTION_STRING")
    else:
        ctx.log("EMR_CONNECTION_STRING environment variable is not set", level="error")
        ctx.log(
            "export EMR_CONNECTION_STRING='ssh -i path/to/key.pem hadoop@ec2-21-43-308-15.compute-1.amazonaws.com'",
            level="error",
        )
        raise click.UsageError("Failed to create table in hive.")

    # ssh onto emr to create table on hive
    emr_command = """
{0} << EOF
hive -e "{1}"
"""
    process = run_bash(emr_command.format(emr_connection_string, schema_statement))

    output, error = process.communicate()
    if process.returncode != 0:
        ctx.log("Could not create table in hive metastore", level="error")
        ctx.log("%s" % error.decode("utf-8"))
        raise click.UsageError("Failed to create table in hive.")
    ctx.vlog("%s" % output.decode("utf-8"))

    ctx.log("✔ Scratch space is ready...")

    # get aws user name to create ranger policy for
    process = run_bash("aws opsworks describe-my-user-profile")

    output, error = process.communicate()
    if process.returncode != 0:
        ctx.log("Could not create table in hive metastore", level="error")
        ctx.log("%s" % error.decode("utf-8"))
        raise click.UsageError("Failed to create table in hive.")
    ctx.vlog("%s" % output.decode("utf-8"))
    user_response = output.decode("utf-8")

    user = json.loads(user_response)
    username = user["UserProfile"]["Name"]

    ctx.log("+ Preparing your Ranger policies for user {0}...".format(username))

    # get schema table name from statement
    read_schema_file = open(schema)
    create_table_line = read_schema_file.readline()
    get_table_name = create_table_line.split()
    table = get_table_name[-1]

    # get ranger password from aws secret manager
    password = get_secret()

    # create user
    create_user(ctx, username, password)

    # get policy user list
    user_list = get_policy_users(ctx, username, password)

    # create policy for user
    create_policy(ctx, table, username, password)

    # add user list to all - catalog policy
    update_catalog_users(ctx, user_list, password)

    # Write the scratch space state to a JSON file based on CLI responses
    write_scratch_space_state(s3_url, bucket_name, folder, table, username)

    ctx.log("✔ Ranger policies for user {0} is ready...".format(username))
    ctx.log("Scratch space is ready.")
