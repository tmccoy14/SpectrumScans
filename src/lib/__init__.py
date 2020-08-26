"""third party modules"""
import chalk


def vulnerability_color(line):
    """Color code the vulnerabilites based on level of warning"""

    if "CRITICAL Vulnerability found" in line:
        red = chalk.Chalk("red")
        return red(line)
    elif "HIGH Vulnerability found" in line:
        yellow = chalk.Chalk("yellow")
        return yellow(line)
    elif "MEDIUM Vulnerability found" in line:
        cyan = chalk.Chalk("cyan")
        return cyan(line)
    else:
        return line


def check_image(ctx, docker, image_name):
    """Check if docker image and version, if provided, exists locally. If not pull the docker image"""

    process = docker.run("images -q {} 2> /dev/null".format(image_name))

    # Grab stdout line by line as it becomes available
    # This will loop until process terminates
    while process.poll() is None:
        line = process.stdout.readline()
        print(line.decode("utf-8").rstrip())

    output, error = process.communicate()
    if process.returncode != 0:
        ctx.log("%s" % error.decode("utf-8"))
    ctx.vlog("%s" % output.decode("utf-8"))

    return output.decode("utf-8").rstrip()
