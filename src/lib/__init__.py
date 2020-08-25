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
