from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

project="pieterraform"

setup(
    name=project,
    version="0.0.1.1a0",
    author="jingwei zhu",
    author_email="jingweizhucn@126.com",
    description="A Terraform Wrapper for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/jevyzhu/{project}",
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
