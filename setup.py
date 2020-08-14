from setuptools import setup, find_packages

setup(
    name="dataio",
    version="0.1",
    description="Dataio is a dataset automation tool.",
    author="Accenture Federal Services",
    author_email="tucker.m.mccoy@accenturefederal.com",
    keywords="sec edw python data automation",
    packages=find_packages(exclude=["tests"]),
    install_requires=["Click==7.0", "boto3", "colorama==0.4.1", "requests==2.23.0"],
    entry_points={"console_scripts": ["dataio=src.main:cli"]},
)
