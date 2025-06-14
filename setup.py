from setuptools import setup, find_packages
from setuptools.command.install import install

import pathlib
import platform
import subprocess


PLATFORM = platform.system()
ROOT_DIR = pathlib.Path().resolve()
PACKAGE_NAME = 'tun2socks'
BINDING_NAME = 'tun2socks'
CMAKE_BUILD_CACHE = 'CMakeBuildCache'


def runCommand(command):
    subprocess.run(command, check=True)


def buildTun2socks():
    output = f'{BINDING_NAME}.lib' if PLATFORM == 'Windows' else f'{BINDING_NAME}.a'

    runCommand(
        [
            'go',
            'build',
            '-C',
            'tun2socks-go',
            '-o',
            f'{ROOT_DIR / "gobuild" / output}',
            '-buildmode=c-archive',
            '-trimpath',
            '-ldflags',
            '-s -w -buildid=',
        ]
    )


def buildBindings():
    configureCache = [
        'cmake',
        '-S',
        '.',
        '-B',
        CMAKE_BUILD_CACHE,
        '-DCMAKE_BUILD_TYPE=Release',
    ]

    if PLATFORM == 'Windows':
        configureCache += ['-G', 'MinGW Makefiles']

    runCommand(configureCache)

    runCommand(
        [
            'cmake',
            '--build',
            CMAKE_BUILD_CACHE,
            '--target',
            BINDING_NAME,
        ]
    )


class InstallTun2socks(install):
    def run(self):
        buildTun2socks()
        buildBindings()

        install.run(self)


with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()


setup(
    name=PACKAGE_NAME,
    version='2.6.0',
    license='GPL v3.0',
    description='Python bindings for go tun2socks.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Loren Eteval',
    author_email='loren.eteval@proton.me',
    url='https://github.com/LorenEteval/tun2socks-python',
    cmdclass={'install': InstallTun2socks},
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
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
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Topic :: Internet :: Proxy Servers',
    ],
    zip_safe=False,
)
