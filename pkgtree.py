#!/usr/bin/env python
'''
A        B     C
|\       |\   /|
| \      | \ / |
D  E     F  G  H
|  |\   /
|  | \ /
I  J  K


> uninstall A
A D E I J

> uninstall B
B F

> uninstall C
C H

> uninstall A B
A B D E F I J K

> uninstall B C
B C F G H

-----------------------------------
You may uninstall packages and dependencies like this (on windows cmd):

> for /F %a in ('pkgtree PACKAGE1 PACKAGE2 -ub') do @pip uninstall -y %a

'''

import sys
import argparse
import pkg_resources

__version__ = '0.4'

_installed = set()
_tops = set()  # {'setuptools', 'pip'}  # Installed with Python.
_depended = set()

# 'setuptools', 'pip' is installed with Python automatically,
# `wheel` will be installed in venv when using `virtualenv` to create venv,
#  so protect them from uninstall.
_protected = {'setuptools', 'pip', 'wheel'}
_packages = {}  # dict of (key, package info)


def _init():
    global _installed
    global _tops
    global _depended
    global _packages
    for p in pkg_resources.working_set:
        _packages[p.key] = p
        _installed.add(p.key)
        for dep in p.requires():
            _depended.add(dep.key)
    _tops |= (_installed - _depended)


def _print_package_info(pkg, level, specs, bare, verbose, ispreserved, ismissed):
    infos = ['  '*level, pkg.project_name]
    if not bare:
        infos.append(' == ' + pkg.version)
        if verbose:
            infos.append(' [{}]'.format(
                ','.join([op+ver for op, ver in specs]) if len(specs) else '*'))
        infos.append(' [PRESERVED]' if ispreserved else '')
        infos.append(' [MISSED]' if ismissed else '')

    print(''.join(infos))


class _DummyPkg():
    pass


def _print_package_info_recurse(key, args, level, specs):
    ispreserved = (args.preserved and key in args.preserved)
    ismissed = key not in _packages
    # When using "-u/--uninstall" with "-b/--bare" option,
    # "missed" or "preserved" packages won't be printed
    if args.uninstall and (ispreserved or ismissed) and args.bare:
        return

    if not ismissed:
        pkg = _packages[key]
        _print_package_info(pkg, level, specs, args.bare,
                            args.verbose, ispreserved, ismissed)
        for dep in pkg.requires():
            _print_package_info_recurse(dep.key, args, level+1, dep.specs)
    else:
        pkg = _DummyPkg()
        pkg.project_name = key
        pkg.version = '0'
        _print_package_info(pkg, level, specs, args.bare,
                            args.verbose, ispreserved, ismissed)


def list_packages(keys, args):
    for k in keys:
        _print_package_info_recurse(k, args, 0, [])


def _get_pkgs_incl_deps(key, exs=set()):
    ''' get package and its dependencies

    Parameter:
        pkg: key of package
        ex: set of keys of packages which should be excluded, including their dependencies

    Return: set
        set of keys
    '''
    global _packages

    if (key in exs) or (key not in _packages):
        return set()
    else:
        ret = {key}
        p = _packages[key]
        for dep in p.requires():
            ret |= _get_pkgs_incl_deps(dep.key, exs)
        return ret


def main():
    global _tops
    global _protected

    psr = argparse.ArgumentParser(fromfile_prefix_chars='@')
    ex_grp = psr.add_mutually_exclusive_group()
    ex_grp.add_argument('-b', '--bare', action='store_true',
                        help='package name only')
    ex_grp.add_argument('-v', '--verbose', action='store_true',
                        help='package == version [specs]')
    psr.add_argument('-u', '--uninstall', action='store_true',
                     help=('List the packages and their dependencies to uninstall,'
                           ' but preserving those required by other packages.'
                           ' Use `-p` to specify more preserved packages.'
                           ' *ONLY* the top-level packages can be uninstalled.'))
    psr.add_argument('-p', '--preserve', action='append', metavar='PACKAGE',
                     help=('Preserve package from `-u` option.'
                           ' This option can be used multiple times.'))
    psr.add_argument('package', nargs='*', metavar='PACKAGE',
                     help='Packages that will be listed.')
    args = psr.parse_args()

    if args.package:
        keys = sorted([k.lower() for k in args.package])
    elif args.uninstall:  # "-u" and no package, print nothing
        return
    else:  # print top-level packages
        keys = sorted(_tops)

    # prepare the "preserved" key set
    if args.uninstall:
        args.preserved = _protected
        _uns = set(keys)
        _exs = set([k.lower() for k in args.preserve] if args.preserve else [])
        # get all dependencies of top packages,
        # excluding uninstall packages and their deps
        for k in ((_tops | _exs) - _uns):
            args.preserved |= _get_pkgs_incl_deps(k)

        if args.preserve:
            args.preserved |= set([k.lower() for k in args.preserve])
    else:
        args.preserved = set()

    list_packages(keys, args)


_init()


if __name__ == '__main__':
    main()
