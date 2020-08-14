from setuptools import setup, find_packages
from pieterraform.version import PROJECT, get_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=PROJECT,
    version=get_version(),
    author="jingwei zhu",
    author_email="jingweizhucn@126.com",
    description="A Terraform Wrapper for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/jevyzhu/{PROJECT}",
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
