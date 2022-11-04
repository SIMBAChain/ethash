#!/usr/bin/env python
from distutils.dist import Distribution
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
import os
from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
import shutil
from typing import Any, Dict

sources = [
    'src/python/core.c',
    'src/libethash/io.c',
    'src/libethash/internal.c',
    'src/libethash/sha3.c']
if os.name == 'nt':
    sources += [
        'src/libethash/util_win32.c',
        'src/libethash/io_win32.c',
        'src/libethash/mmap_win32.c',
    ]
else:
    sources += [
        'src/libethash/io_posix.c'
    ]
depends = [
    'src/libethash/ethash.h',
    'src/libethash/compiler.h',
    'src/libethash/data_sizes.h',
    'src/libethash/endian.h',
    'src/libethash/ethash.h',
    'src/libethash/io.h',
    'src/libethash/fnv.h',
    'src/libethash/internal.h',
    'src/libethash/sha3.h',
    'src/libethash/util.h',
]
pyethash = Extension('pyethash',
                     sources=sources,
                     depends=depends,
                     extra_compile_args=["-Isrc/", "-std=gnu99", "-Wall"])


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    distribution = Distribution({"name": "pyethash", "ext_modules": [pyethash]})
    distribution.package_dir = "pyethash"

    cmd = build_ext(distribution)
    cmd.ensure_finalized()
    cmd.run()

    # Copy built extensions back to the project
    for output in cmd.get_outputs():
        relative_extension = os.path.relpath(output, cmd.build_lib)
        if not os.path.exists(output):
            continue

        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)

    return setup_kwargs

if __name__ == "__main__":
    build({})