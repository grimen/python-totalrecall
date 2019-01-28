
# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()


# =========================================
#       EXAMPLE
# --------------------------------------

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

foo()

print('[profiler.function / basic]: TIME: {0}'.format(profiler.time))
print('[profiler.function / basic]: STEPS: {0}'.format(profiler.steps))
