# PieTerraform

> This is a wrapper for terraform to facilitate python developer to call terraform.
> It is designed to invoke terraform commands in **"Functional Chaining"** style

**Note**: Only `python>=3.7` is supported.

# Features

* Builder pattern. One line code can call multiple terraform commands
* Terraform commands' arguments are encapsulated as functions so code completion supported
* No need to worry about the sequence of arguments


# Usage

Make sure have **terraform in $PATH**

```bash
terraform version
```

## Install

```bash
pip install pieterraform
```

## Quick start

```py

from pieterraform import Terraform

# suppose you have terraform files in ./tf
Terraform().workdir('./tf')
    .init().run()           # 'terraform init'
    .plan().run()           # 'terraform plan'
    .apply().run()          # 'terraform apply'

# suppose you have terraform files in ./tf/prod
Terraform().workdir('./tf')
    .init().dir('prod').run()
    .plan().dir('prod').run()
    .apply().dir('prod').run()

# suppose you have terraform files in ./tf/prod
Terraform().workdir()
    .init().dir('tf/prod').run()
    .plan().dir('tf/prod').run()
    .apply().dir('tf/prod').run()

```
Just **ONE LINE** code!

## With Paramers

```py

from pieterraform import Terraform

# suppose you have terraform files in ./tf
Terraform().workdir('./tf')
    # 'terraform init -no-color -upgrade=false'
    .init().no_upgrade().no_color().run()
    # 'terraform plan -state mystate.json -no-color'
    .plan().state_file('mystate.json').no_color().out('myplan').run()
    # 'terraform apply myplan'
    .apply().use_plan('myplan').run()
    # 'terraform destroy -auto-approve -state mystate.json'
    .destroy().auto_approve().state('mystate.json').run()

```

## With Custome Log
By default it prints log in screen.
But you can cusomize it to use any logger

```py

import logging
from pieterraform import Terraform

# output log to file
logFormatter = logging.Formatter('%(asctime)s [%(levelname)-5.5s] %(message)s')
log_file = 'log.txt'
f_handler = logging.FileHandler(log_file)
f_handler.setFormatter(logFormatter)
f_handler.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(f_handler)

# suppose you have terraform files in ./tf
Terraform(logger=logger) # this will output log to file 'log.txt'
    .workdir('./tf')
    .init().run()
    .plan().run()
    .apply().run()

```

## Traditional calls rather than functions chain

```py

from pieterraform import Terraform

tf = Terraform().workdir('./tf')
initer = tf.init()
initer.no_upgrade()
initer.no_color().run()
planer = tf.plan()
planer.state_file('mystate.json')
planer.no_color()
planer.out('myplan').run()
applyer = tf.apply()
applyer.use_plan('myplan')
applyer.run()

```

## Check result
```py

from pieterraform import Terraform

a_run = Terraform().workdir('./tf')
    .init().run()
    .plan().run()
    .apply().run()

for r in a_run.results:
    print(r.output)
    print(r.command)

```



# Source Code

This project is fully using docker as dev environment.

## Prerequisition
* docker: ">= 17.06"
* docker-compose: ">= 1.26"

**No python** needed.

## Build
```bash
make
```
## Install to local
```bash
make install
```
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
