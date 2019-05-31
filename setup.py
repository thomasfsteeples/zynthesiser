from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="zynthesiser",
    version="0.1",
    author="Thomas Steeples",
    author_email="steeps@robots.ox.ac.uk",
    description="An enumerative solver for SyGuS problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thomasfsteeples/zynthesiser/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)