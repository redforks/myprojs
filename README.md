# myprojs

`myprojs` is a python script manages git directories.

If you like me have many projects use `git` as source repository, you'll know the pain of forget to `push` your source code.

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

## Project Types

Project type is a file located at `~/.myprojs`, file is a text file each line
is a project directory. Lines start with `'#'` are comments and ignored. Such as:

```
cat ~/.myprojs/chat

# ~/chat/client.old
~/chat/server
~/chat/client
# db and other useful scripts
~/chat/scripts

cat ~/myprojs/bbs

~/bbs/*
-~/bbs/try-server
```

Project type selected by `--project-type` command argument, to run
tests on `'chat'` projects:

```
myprojs.py --project-type chat -- yarn test
```

`'all'` is a special project type, combines all project types, and is the default value of `'--project-type'` argument.

## Note

1. Duplicate directories are ignored, especially useful for `all` project type.
1. Non-git directories are ignored
1. Support '\*' glob,
1. Directories prefixed with '-' are exclude, use it to excludes globed directory.

## Install

`myproj.py` is a simple python script, download and mark it as executable, put it into one of your `PATH` directories.
