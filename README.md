
# `totalrecall` [![PyPI version](https://badge.fury.io/py/totalrecall.svg)](https://badge.fury.io/py/totalrecall) [![Build Status](https://travis-ci.com/grimen/python-totalrecall.svg?branch=master)](https://travis-ci.com/grimen/python-totalrecall) [![Coverage Status](https://codecov.io/gh/grimen/python-totalrecall/branch/master/graph/badge.svg)](https://codecov.io/gh/grimen/python-totalrecall)

*A runtime step profiler - for Python.*

## Introduction

Aggregating runtime statistics and/or finding bottlenecks in code is one of the most common challenges as a software engineer. This is a library to aid that. In comparison to most existing libraries this one is focused on **step profiling**; aggregation of runtime information in steps marked by keys/tags/labels and optional meta data, which is used to create a summary of all steps in form of a transaction. As a bonus it also supports decorating code **contexts** and **functions**.

This is an **MVP** that most likely will be extended with more profiling features.


## Install

Install using **pip**:

```sh
$ pip install totalrecall
```


## Use

Very basic **[example](https://github.com/grimen/python-totalrecall/tree/master/examples/basic.py)**:

```python
import totalrecall

from time import sleep

# ---------------------------------------------------
#   EXAMPLE: runtime step profiler
# ------------------------------------------------

profiler = totalrecall.timer('profile something - using timer', begin = False)

profiler.begin('task 1')

sleep(0.1)

profiler.begin('task 2')

sleep(0.2)

profiler.begin('task 3')

sleep(0.3)

profiler.end()

print('[profiler.time / basic]: TIME: {0}'.format(profiler.time))
print('[profiler.time / basic]: STEPS: {0}'.format(profiler.steps))

# ---------------------------------------------------
#   EXAMPLE: runtime step profiler (detailed)
# ------------------------------------------------

profiler = totalrecall.timer('profile something - using timer',
    begin = False,
    enabled = True,
    verbose = True,
    colors = True,
)

profiler.begin('task 1')

sleep(0.1)

profiler.begin('task 2')

sleep(0.2)

profiler.begin('task 3')

sleep(0.3)

profiler.end()

print('[profiler.time / detailed]: TIME: {0}'.format(profiler.time))
print('[profiler.time / detailed]: STEPS: {0}'.format(profiler.steps))


# ---------------------------------------------------
#   EXAMPLE: runtime context profiler
# ------------------------------------------------

profiler = totalrecall.context('profile something 2 - using context')

with profiler:
    sleep(1)

print('[profiler.context / basic]: TIME: {0}'.format(profiler.time))
print('[profiler.context / basic]: STEPS: {0}'.format(profiler.steps))


# ---------------------------------------------------
#   EXAMPLE: runtime function profiler
# ------------------------------------------------

profiler = totalrecall.function('profile something 2 - using context')

@profiler
def foo():
    sleep(1)

print('[profiler.function / basic]: TIME: {0}'.format(profiler.time))
print('[profiler.function / basic]: STEPS: {0}'.format(profiler.steps))

```


## Test

Clone down source code:

```sh
$ make install
```

Run **colorful tests**, with only native environment (dependency sandboxing up to you):

```sh
$ make test
```

Run **less colorful tests**, with **multi-environment** (using **tox**):

```sh
$ make test-tox
```


## About

This project was mainly initiated - in lack of solid existing alternatives - to be used at our work at **[Markable.ai](https://markable.ai)** to have common code conventions between various programming environments where **Python** (research, CV, AI) is heavily used.


## Credits

Thanks to **[op-bk](https://github.com/op-bk)** for creative help with naming this library.


## License

Released under the MIT license.
