#!/usr/bin/env python3

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from copy import deepcopy
from pathlib import Path
import re
import shutil

import jupytext

_JL_JSON_FMT = r'''\
{{
  "jupyter-lite-schema-version": 0,
  "jupyter-config-data": {{
    "contentsStorageName": "rss-{language}"
  }}
}}
'''

# Find data read.
_READ_FMT = r'''^(?P<indent>\s*)
(?P<equals>\w+\s*{equal_re}\s*)
(?P<read_func>{read_re}\w+\(
['"])
(?P<fname>.*?)
(?P<closequote>['"]
\))
'''

PY_READ_RE = re.compile(
    _READ_FMT.format(equal_re='=', read_re=r'pd\.read_'),
    flags=re.MULTILINE | re.VERBOSE)

R_READ_RE = re.compile(
    _READ_FMT.format(equal_re='<-', read_re=r'read\.'),
    flags=re.MULTILINE | re.VERBOSE)


def path_to_url(nb, root_url, regex):
    out_nb = deepcopy(nb)

    def _read_re_replace(m):
        d = m.groupdict()
        d['fname'] = Path(d['fname']).name
        return ('''\
{indent}# Read data from web URL instead of local data directory
{indent}# (so that notebook works in online version).
{indent}{equals}{read_func}{root_url}/{fname}{closequote}'''
                .format(**d, root_url=root_url))

    for cell in out_nb['cells']:
        if cell['cell_type'] != 'code':
            continue
        cell['source'] = regex.sub(_read_re_replace, cell['source'])
    return out_nb


def process_dir(input_dir, output_dir, language, in_nb_suffix, kernel_name,
                kernel_dname, url_root=None,
                out_nb_suffix='.ipynb'
               ):
    output_dir.mkdir(exist_ok=True, parents=True)
    for path in input_dir.glob('*'):
        if path.is_dir() and input_dir != output_dir:
            shutil.copytree(path, output_dir / path.name, dirs_exist_ok=True)
            continue
        if path.suffix != in_nb_suffix:
            continue
        nb = jupytext.read(path)
        nb['metadata']['kernelspec'] = {
            'name': kernel_name,
            'display_name': kernel_dname}
        regex = PY_READ_RE if language == 'python' else R_READ_RE
        if url_root:
            nb = path_to_url(nb, url_root, regex)
        jupytext.write(nb, output_dir / (path.stem + out_nb_suffix))


def get_parser():
    parser = ArgumentParser(description=__doc__,  # Usage from docstring
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('source_path',
                        help='Directory with input notebooks')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    source_path = Path(args.source_path)
    process_dir(source_path,
                source_path,
                'python',
                '.ipynb',
                'python',
                "Python (Pyodide)",
                None)
    (source_path / 'jupyter-lite.json').write_text(
        _JL_JSON_FMT.format(language='python'))


if __name__ == '__main__':
    main()
