# PieTerraform 

> This is a wrapper for terraform to facilitate python developer to call terraform in very nature way.

**Note**: it is still in development and only `python>=3.7` supported.

# Features

* Builder mode: just one line code to call multiple terraform commands
* Terraform commands' arguments are encapsulated as functions so code completion supported
* No need to worry about the sequence of arguments 


# Usage

## Install from PyPi

```bash
pip install pieterraform
```

## Quick start
```py
from pieterraform import Terraform

# suppose you have terraform files in ./tf
# run 'terraform init', 'terraform plan' and 'terraform apply'
Terraform().workdir('./tf').init().run().plan().run().apply().run()
```
Just **ONE LINE** code!

## With terraform paramers
```py
from pieterraform import Terraform

# suppose you have terraform files in ./tf
# to run following commands in order:
# 'terraform init -no-color -upgrade=false'
# 'terraform plan -state mystate.json -no-color' 
# 'terraform apply myplan' 
# 'terraform destroy -auto-approve -state mystate.json'

Terraform().workdir('./tf')
    .init().no_upgrade().no_color().run()
    .plan().state_file('mystate.json').no_color().out('myplan').run()
    .apply().use_plan('myplan').run()
    .destroy().auto_approve().state('mystate.json').run()
```

## With log output
```py
import logging
from pieterraform import Terraform

# create a logger connect to console
logFormatter = logging.Formatter('%(asctime)s [%(levelname)-5.5s] %(message)s')
logger = logging.getLogger('fool_log')
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
c_handler.setFormatter(logFormatter)
c_handler.setLevel(logging.DEBUG)
logger.addHandler(c_handler)

# suppose you have terraform files in ./tf
# run 'terraform init', 'terraform plan' and 'terraform apply'
# this will print log out in screen
Terraform(logger=logger).workdir('./tf').init().run().plan().run().apply().run()
```

# Source Code

This project is fully using docker as dev environment

## Prerequisition
* docker: ">= 17.06"
* docker-compose: ">= 1.26"

**No python** needed.

## Run test
```bash
make test
```
## Distribution
```bash
make dist
```

## Development

### Start dev docker
```
make docker-dev
```
this will start a container named pieterraform-devenv

### Use VSCode
Open your vscode, attach to above container to do remote development
