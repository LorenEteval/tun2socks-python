# tun2socks-python

[![Deploy PyPI](https://github.com/LorenEteval/tun2socks-python/actions/workflows/deploy-pypi.yml/badge.svg?branch=main)](https://github.com/LorenEteval/tun2socks-python/actions/workflows/deploy-pypi.yml)

Python bindings for [tun2socks](https://github.com/xjasonlyu/tun2socks).

## Installation

Install the package from PyPI:

```console
pip install tun2socks
```

The published binary wheels include the compiled Go backend and native Python binding. A compatible wheel is selected
automatically, so installing on a supported platform does not require Go, CMake, or a C/C++ compiler.

### Binary Wheel Support

| Platform | Architecture | CPython versions |
|----------|--------------|------------------|
| Linux (manylinux2014) | x86_64 | 3.8-3.14, 3.13t, 3.14t |
| Linux (manylinux2014) | ARM64 | 3.8-3.14, 3.13t, 3.14t |
| Windows | x86_64 | 3.8-3.14, 3.13t, 3.14t |
| Windows | ARM64 | 3.9-3.14, 3.13t, 3.14t |
| macOS | Intel | 3.8-3.14, 3.13t, 3.14t |
| macOS | Apple Silicon | 3.8-3.14, 3.13t, 3.14t |

Windows ARM64 starts at Python 3.9 because cibuildwheel does not provide a CPython 3.8 Windows ARM64 build.

### Building from Source

Building from source is only necessary for contributors or when no compatible wheel is available. It requires:

- [Go](https://go.dev/doc/install)
- [CMake](https://cmake.org/download/) 3.15 or newer
- A C/C++ toolchain: GCC on Linux, Apple Clang on macOS, MinGW-w64 on Windows x86_64, or LLVM-MinGW on Windows ARM64

## API

```pycon
>>> import tun2socks
>>> help(tun2socks) 
Help on package tun2socks:                                                                                                                                                                                    

NAME
    tun2socks

PACKAGE CONTENTS
    tun2socks

FUNCTIONS
    startFromArgs(...) method of builtins.PyCapsule instance
        startFromArgs(device: str, networkInterface: str, logLevel: str,
                      proxy: str, restAPI: str, tcpSendBufferSize: str = '',
                      tcpReceiveBufferSize: str = '', tcpAutoTuning: bool = False) -> None

        Start tun2socks with custom arguments

VERSION
    2.7.0
```

## Source Code Modification

This repository, including the package that distributes to pypi,
contains [tun2socks](https://github.com/xjasonlyu/tun2socks) source code that's been
modified to build the binding and specific API. If without explicitly remark, the version of this package corresponds to
the version of the origin source code tag, so the binding will have full features as the original go distribution will
have. And due to its backward compatibility, there's no plan to generate bindings for older release of tun2socks.

To make installation of this package easier, I didn't add the
original [tun2socks](https://github.com/xjasonlyu/tun2socks)
source code as a submodule. To track what modifications have been made to the source code, you can compare it with the
same version under Python binding and corresponding go repository.

## License

The license for this project follows its original go repository [tun2socks](https://github.com/xjasonlyu/tun2socks) and
is under [MIT](https://github.com/LorenEteval/tun2socks-python/blob/main/LICENSE).

(Upstream project relicensed, see [tun2socks#460](https://github.com/xjasonlyu/tun2socks/issues/460))
