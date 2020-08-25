from setuptools import setup, find_packages

setup(
    name="scancli",
    version="0.1",
    description="Scancli is a Docker image security scanning tool.",
    author="Tucker McCoy",
    author_email="tuckermmccoy@gmail.com",
    keywords="anchore security scan docker image automation",
    packages=find_packages(exclude=["tests"]),
    install_requires=["Click==7.0", "pychalk==2.0.1"],
    entry_points={"console_scripts": ["scancli=src.main:cli"]},
)
