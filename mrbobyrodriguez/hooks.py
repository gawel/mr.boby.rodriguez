# -*- coding: utf-8 -*-
import os
from chut import test, git, mkdir, wget
from sphinx import quickstart

use_defaults = (
    'sep', 'dot', 'release', 'suffix', 'master', 'epub',
    'ext_doctest', 'ext_intersphinx', 'ext_todo', 'ext_coverage',
    'ext_pngmath', 'ext_mathjax', 'ext_ifconfig', 'makefile',
)


def pre_render(config):
    github_user = str(git('config github.user'))
    pkgname = os.path.basename(os.path.abspath(config.target_directory))
    pkg = pkgname.lower()
    for l in '.':
        pkg = pkg.replace(l, '')
    for l in '-':
        pkg = pkg.replace(l, '_')
    url = 'https://github.com/{0}/{1}/'.format(github_user, pkgname)
    config.variables.update({
        'package.name': pkgname,
        'package.directory': pkg,
        'project': pkgname,
        'package.version': '0.1.dev0',
        'package.url': url,

        'ext_autodoc': 'y',
        'ext_viewcode': 'y',
        'batchfile': False,
    })


def post_render(config):

    pkg = config.variables['package.directory']

    pkg_dir = os.path.join(config.target_directory, pkg)
    if not test.d(pkg_dir):
        mkdir(pkg_dir)

    bootstrap = os.path.join(config.target_directory, 'bootstrap.py')
    if not test.f(pkg_dir):
        wget('-O', bootstrap,
             ('https://github.com/buildout/buildout/raw/'
              '2/bootstrap/bootstrap.py')) > 1

    doc_root = os.path.join(os.path.abspath(config.target_directory), 'docs')
    d = dict(path=doc_root,
             **config.variables)

    quickstart_do_prompt = quickstart.do_prompt

    def do_prompt(d, key, text, default=None, validator=quickstart.nonempty):
        if key in use_defaults:
            if default == 'y':
                default = True
            elif default == 'n':
                default = False
            d[key] = default
        elif key not in d:
            quickstart_do_prompt(d, key, text, default, validator)

    quickstart.do_prompt = do_prompt

    if not os.path.isdir(doc_root):
        quickstart.ask_user(d)
        quickstart.generate(d)
        filename = os.path.join(doc_root, 'conf.py')
        with open(filename, 'wb') as fd:
            fd.write('''
import pkg_resources
version = pkg_resources.get_distribution("%s").version
release = version
''' % config.variables)
