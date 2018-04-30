# myprojs

`myprojs` is a python script manages git directories.

If you like me have many projects use `git` as source repository, you'll known the pain of forget to `push` your source code.

Use `myprojs` to cure the pain:

```bash
myprojs.py --need-push -- git push
```

## Basic Usage

To list your project directories:

```bash
myprojs.py
```

To list dirty projects, i.e. contains changes not committed.

```bash
myprojs.py --dirty
```

To list not pushed projects:

```bash
myprojs.py --need-push
```

Execute command on your projects, such as unit tests:

```bash
myprojs.py -- jest
```

`jest` or other unit tests tool, will execute at each project's directory.

## Project Type

Project directory list stored in `~/.myprojs` directory, file is
a text file, each line is a project directory. Ignore lines starts
with `'#'`. Each file defines a project type, such as:

```
cat ~/.myprojs/chat

~/chat/server
~/chat/client
~/chat/scripts

cat ~/myprojs/bbs

~/bbs/list
~/bbs/article
~/bbs/backend

```

Define your projects, run command on specified project group:

```
myprojs.py --project-type chat --dirty --push
```

A special project type is `'all'`, include project directory of all
project types. `'all'` is default.

Duplicate directories are ignored, especially useful for `all` project type.

## Install

`myproj.py` is a simple python script, download and mark it as executable, put it into one of `PATH` directory.
