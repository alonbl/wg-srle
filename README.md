# SRLE implementation

## Overview

Encoded format:

```
[<separator><byte><number>]*
```

Separator must be printable graph ASCII but not a digit.

Non printable bytes are escaped using `\x` followed by 2 hex digits.

Number is decimal occurrences of the byte.

Input is binary byte sequence, output is ASCII printable string.

### Examples

Assuming separator is `|`.

```
aaaabbbcc       |a4|b3|c2
aaaa\n\n\ncc    |a4|\x0a2|c2
a||b            |a1|\x7c2|b1
```

## Usage

```sh
wg-srle --help
```

### Examples

```sh
wg-srle encode file1.in file1.out
wg-srle decode file1.out file1.in2
cmp file1.in file1.in2
```

## Build

Standard setuptools packaging:

```sh
$ ./setup build test install
```

Supported environment variables for CI to generate build information:

|Name           |Default|Description      |
|---------------|-------|-----------------|
|PACKAGE_VERSION|master |Package version  |

Example:

```sh
$ PACKAGE_VERSION=1.2.3 ./setup sdist
```

## Concerns

Tested to work with both python2 and python3.

Provide both command-line and library interfaces.

Packaged as standard python packaging.

Manages version information as input for packaging to avoid tag commit in CI
when publishing a new version.

Attempt to provide decent coverage of unit tests.

pyflakes and pycodestyle compliant.
