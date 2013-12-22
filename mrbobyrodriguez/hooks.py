# -*- coding: utf-8 -*-
import os
from chut import test, git, cd, mkdir, chmod, sh, wget
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
        'github.user': github_user,
        'package.name': pkgname,
        'package.directory': pkg,
        'project': pkgname,
        'package.version': '0.1.dev0',
        'package.url': url,

    })


def post_render(config):

    target_directory = os.path.abspath(config.target_directory)
    pkg = config.variables['package.directory']

    pkg_dir = os.path.join(target_directory, pkg)
    if not test.d(pkg_dir):
        mkdir(pkg_dir)
        with open(os.path.join(pkg_dir, '__init__.py'), 'wb') as fd:
            fd.write('#  package\n')

    doc_root = os.path.join(target_directory, 'docs')
    vars = config.variables
    d = dict(path=doc_root, author=vars['author.name'],
             project=vars['package.name'],
             version='', ext_autodoc='y', ext_viewcode='y',
             batchfile=False)

    quickstart_do_prompt = quickstart.do_prompt

    def do_prompt(d, key, text, default=None, validator=quickstart.nonempty):
        print(key)
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
        # launch sphinx
        quickstart.ask_user(d)
        quickstart.generate(d)
        filename = os.path.join(doc_root, 'conf.py')

        # patch some files
        with open(filename, 'ab') as fd:
            fd.write('''
html_theme = 'nature'
import pkg_resources
version = pkg_resources.get_distribution("%s").version
release = version
''' % vars['package.name'])
        filename = os.path.join(doc_root, 'Makefile')
        with open(filename, 'rb') as fd:
            data = fd.read()
        data = data.replace('sphinx-build', '../bin/sphinx-build')
        with open(filename, 'wb') as fd:
            fd.write(data)

    # launch buildout
    cd(target_directory)
    if not test.f('bootstrap.py'):
        wget('-O bootstrap.py',
             ('https://github.com/buildout/buildout/raw/'
              'master/bootstrap/bootstrap.py')) > 1
        chmod('+x bootstrap.py')

    sh.python('bootstrap.py --allow-site-packages') > 1
    if test.f('bin/buildout'):
        sh.python('bin/buildout') > 1
