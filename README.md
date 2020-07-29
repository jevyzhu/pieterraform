# Python Wrapper for Terraform

> This is a wrapper for terraform to facilitate python developer to user terraform in nature way.

**Note**: it is still in development and only `python>=3.7` supported.

# Install

```bash
pip install pyrraform
```
or

```bash
pip install --index-url https://test.pypi.org/simple/ pyrraform
```

# Quick start
```py
from pyrraform.tf_cmder import Terraform
# run 'terraform init', 'terraform plan' and 'terraform apply' in order
Terraform().init().run().plan().run().apply().run()
```
Just one line code!

# Source Code
## Run test
```bash
make test-docker
```
## Start development docker container
```
make start-dev-docker
```