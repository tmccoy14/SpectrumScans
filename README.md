# Spectrum Scans

<img src="https://www.docker.com/blog/wp-content/uploads/Docker-Security-Banner-01.png" width="400" height="400" />

#### Development & Install

To get started, create some sort of virtual environment before you install `scancli` the CLI tool. Scancli is the standardized tool that can be used to scan Docker images to find security vulnerabilities. To do this, it uses the open source tool, [Anchore](https://anchore.com/).

#### Install Development Packages

```sh
# Activate your virtual environment
$ cd spectrumscans/
$ pip install -r requirements/development.txt
```

#### Install Scancli Tool

```sh
# Install scancli
$ cd spectrumscans/
$ pip install --editable .
```

The `--editable` flag will allow for you to make edits to code without having to re-run `pip install ...` locally.

#### Validate The Install

Run `scancli --version` to verify the installation was successful.

```sh
$ scancli --version
scancli version: v0.1.0
```

#### Show The Tool Capabilities

Run `scancli` to learn what the tool does and the commands you can runn with it.

```sh
$ scancli
Usage: scancli [OPTIONS] COMMAND [ARGS]...

Scancli is the standardize tool that can be used to scan Docker images to find security vulnerabilities. It uses the open source tool Anchore, to ensure vulnerability scanning and policy compliance for containers. It can be done as easy as passing in the name of the Docker image and tag you'd like to scan. Once you do that, sit back and let Scancli do the rest for you!

Options:
  --home DIRECTORY  Project folder to operate on.
  -v, --verbose     Enables verbose mode.
  --version         Print the current version of scancli.
  --help            Show this message and exit.

Commands:
  scan  Scan Docker image.
```

#### Running The Tool

Scancli only has one command, `scancli scan`, which will take the image and tag that you want to scan and return the found vulnerabilities.

```sh
$ scancli scan --help
Usage: scancli scan [OPTIONS]

scancli scans the provided Docker image for vulnerability findings. Ex. scancli scan --image image/name --tag 0.0.0

Options:
  -i, --image TEXT  Docker image name.  [required]
  -t, --tag TEXT    Docker image tag.
  --help            Show this message and exit.
```
