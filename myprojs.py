#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os
import os.path
import sys
from subprocess import run, PIPE


parser = argparse.ArgumentParser(description="Manage my project directories")
parser.add_argument("--dirty", help="filter out dirty work directories",
                    action='store_true')
parser.add_argument("--need-push", help="filter out directory need git push",
                    action='store_true', dest='needPush')
parser.add_argument("--project-type",
                    help='Select project type, project type defined at'
                    " ~/.myprojs directory, default to 'all', combines all "
                    'project files.',
                    default='all')
parser.add_argument('Command', nargs="?",
                    help="Command run on each project directory, " +
                    "default to 'pwd'", default='pwd')

args = parser.parse_args()


def isDirty(p):
    """returns true if project p is dirty, i.e. contains changes not commit
    to git.
    """
    rv = run(["git", "status", "-s"], cwd=p, stdout=PIPE)
    if rv.returncode != 0:
        return False
    return bool(rv.stdout)


def needPush(p):
    """returns true if directory contains git commits not pushed.
    """
    rv = run(["git", "status", "-sb"], cwd=p, stdout=PIPE)
    if rv.returncode != 0:
        return False
    return 'ahead ' in str(rv.stdout)


def forEach(cmd, projs):
    """
    forEach execute shell command in each src directory.
    """
    failedDirs = []
    for p in projs:
        cp = run(cmd, cwd=p, shell=True)
        if cp.returncode != 0:
            failedDirs.append(p)

    if failedDirs:
        print("failed dirs:", "\n".join(failedDirs))


proj_set_dir = os.path.expanduser('~/.myprojs')


def load_projects(proj_set):
    """Load projects by project set.

    Project set is a file located at ~/.myprojs.

    Empty and started with '#' lines are ignored, each line should be a
    absolute path point to a git directory.

    Directory not exist are exclude, and displayed as a warning.

    Directory path should be absolute, support '~' as home directory.

    :param proj_set: project set name
    :returns: returns list of project directories.
    """

    def dir_exist(d):
        if not os.path.exists(d):
            print(d, 'not exist', file=sys.stderr)
            return False
        return True

    fn = os.path.join(proj_set_dir, proj_set)
    with open(fn) as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]
    lines = [l for l in lines if l and not l.startswith('#')]
    lines = list(set(lines))
    lines = [os.path.expanduser(l) for l in lines]
    return filter(dir_exist, lines)


def remove_dup(strs):
    """Remove string array duplicate items.

    :param strs: list of string
    :returns: sorted strings with duplicate items removed.
    """
    r = list(set(strs))
    r.sort()
    return r


def load_all():
    """Load all project files, and merge them all.

    Ignore hidden files, (files start with '.').

    Duplicate projects are merged.

    : returns: return list of all project directories.
    """
    dirs = []
    for ps in os.listdir(proj_set_dir):
        if not ps.startswith('.'):
            dirs.extend(load_projects(ps))
    return remove_dup(dirs)


if __name__ == '__main__':
    if args.project_type == 'all':
        selected = load_all()
    else:
        selected = load_projects(args.project_type)

    if args.dirty:
        selected = [x for x in selected if isDirty(x)]

    if args.needPush:
        selected = [x for x in selected if needPush(x)]

    forEach(args.Command, selected)
