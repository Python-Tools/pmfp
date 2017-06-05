# project management

## init

### init a new project

init subcommand can build a project Automatically.

#### choose virtual env

The project will build a virtual environment. And use the virtual environment as default python environment if there is a folder named `env`.

`pmfp` will build the environment by `venv`. you can choose `conda` to build the env by use the flag `-C`



#### templates

init subcommand can build a basic template for different kinds of situations.

There are several choices:

+ script `-s`
+ model  `-m`
+ command line tools `-c`
+ gui `-g` gui with `tk`
+ web `-w` you can choose a parameter from `sanic`, `flask`, `zerorpc`

#### with scientific calculation tools

you can use the flag `-M` to install `numpy`,`scipy`,`sklearn` Automatically.



### init a exist project

If you want to init a exist project with some code ,requirements and `.ppmrc`.
you can just run `ppm init`, and then follow the questions.


## project clean

subcommand `clean` can clean the project. if use the flag `-a`,`apidoc`, `docs`, `env`, `test`, `.ppmrc`, `requirements`, `setup.py` will be removed. if use the flag `-s`, `docs`, `env`, `.ppmrc`  will be removed.

## project status

subcommand `status` can show the project's status.

## project rename

subcommand `rename` can rename the project.

## project update version_info

subcommand `update` can update the project's version information

## use the virtual environment to run the script

subcommand `run` can run the project's script in the virtual environment

## test management

subcommand `test` can run the tests esaily.

if there is a `-t` flag, pmfp will use mypy to check the typehint.

if there is a `-c` flag, pmfp will show the coverage, args html or report will fix the exhibition form.

else, it will run the unit test.

## document management

subcommand `doc` can easily deal with the sphinx document. flag `-b` will build html the document to `docs` fold with a file `.nojekyll`.

flag `-s` will run a simple http server for the `docs`