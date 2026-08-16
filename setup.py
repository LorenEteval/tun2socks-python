import os
import pathlib
import platform
import re
import subprocess
import sys
from importlib import metadata

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


PLATFORM = platform.system()
ROOT_DIR = pathlib.Path(__file__).parent.resolve()
PACKAGE_NAME = 'tun2socks'
BINDING_NAME = 'tun2socks'


def run_command(command, **kwargs):
    subprocess.run(command, check=True, **kwargs)


def macos_architectures():
    return re.findall(r'-arch\s+(\S+)', os.environ.get('ARCHFLAGS', ''))


def pybind11_cmake_dir():
    # Resolve the PEP 517 build dependency by distribution metadata. Importing
    # pybind11 here would be ambiguous in a checkout that still contains the
    # project's older vendored pybind11/ source directory.
    distribution = metadata.distribution('pybind11')
    return distribution.locate_file('pybind11/share/cmake/pybind11')


def build_tun2socks(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    output = f'{BINDING_NAME}.lib' if PLATFORM == 'Windows' else f'{BINDING_NAME}.a'
    environment = os.environ.copy()

    # cibuildwheel sets ARCHFLAGS for its requested macOS architecture. Go's
    # architecture names differ from Apple's, so keep the Go archive aligned
    # with the CMake extension when CPython itself runs under Rosetta (3.8).
    if PLATFORM == 'Darwin':
        architectures = macos_architectures()
        if len(architectures) == 1:
            environment['GOARCH'] = {'x86_64': 'amd64', 'arm64': 'arm64'}[
                architectures[0]
            ]

    run_command(
        [
            'go',
            'build',
            '-C',
            str(ROOT_DIR / 'tun2socks-go'),
            '-o',
            str(output_dir / output),
            '-buildmode=c-archive',
            '-trimpath',
            '-ldflags',
            '-s -w -buildid=',
        ],
        env=environment,
    )


class CMakeExtension(Extension):
    def __init__(self, name):
        # The sources are built by CMake, but declaring an Extension is what
        # tells setuptools and wheel that this distribution is not pure Python.
        super().__init__(name, sources=[])


class BuildTun2socks(build_ext):
    def build_extension(self, extension):
        extension_path = pathlib.Path(self.get_ext_fullpath(extension.name)).resolve()
        extension_dir = extension_path.parent
        build_root = pathlib.Path(self.build_temp).resolve() / extension.name.replace(
            '.', '_'
        )
        go_build_dir = build_root / 'go'
        cmake_build_dir = build_root / 'cmake'

        extension_dir.mkdir(parents=True, exist_ok=True)
        cmake_build_dir.mkdir(parents=True, exist_ok=True)
        build_tun2socks(go_build_dir)

        configure_command = [
            'cmake',
            '-S',
            str(ROOT_DIR),
            '-B',
            str(cmake_build_dir),
            '-DCMAKE_BUILD_TYPE=Release',
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extension_dir}',
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE={extension_dir}',
            '-DPYBIND11_FINDPYTHON=ON',
            f'-DPython_EXECUTABLE={sys.executable}',
            f'-Dpybind11_DIR={pybind11_cmake_dir()}',
            f'-DTUN2SOCKS_GO_BUILD_DIR={go_build_dir}',
        ]

        if PLATFORM == 'Windows':
            configure_command += [
                '-G',
                'MinGW Makefiles',
                '-DCMAKE_C_COMPILER=gcc',
                '-DCMAKE_CXX_COMPILER=g++',
            ]
        elif PLATFORM == 'Darwin':
            architectures = macos_architectures()
            if architectures:
                architecture_list = ';'.join(architectures)
                configure_command.append(
                    f'-DCMAKE_OSX_ARCHITECTURES={architecture_list}'
                )

        run_command(configure_command)
        run_command(
            [
                'cmake',
                '--build',
                str(cmake_build_dir),
                '--config',
                'Release',
                '--target',
                BINDING_NAME,
            ]
        )

        if not extension_path.is_file():
            raise RuntimeError(
                'CMake did not create the extension at the path expected by '
                f'setuptools: {extension_path}'
            )


with open(ROOT_DIR / 'README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()


setup(
    name=PACKAGE_NAME,
    version='2.7.0',
    license='MIT',
    description='Python bindings for go tun2socks.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Loren Eteval',
    author_email='loren.eteval@proton.me',
    url='https://github.com/LorenEteval/tun2socks-python',
    cmdclass={'build_ext': BuildTun2socks},
    ext_modules=[CMakeExtension('tun2socks.tun2socks')],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Internet',
        'Topic :: Internet :: Proxy Servers',
    ],
    zip_safe=False,
)
