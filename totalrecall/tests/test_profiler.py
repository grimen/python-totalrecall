
# encoding: utf-8

# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()

from totalrecall.tests import helper

import totalrecall
import math

from os import environ
from time import sleep


# =========================================
#       HELPERS
# --------------------------------------

def significant_decimal(value):
    return float('%.1g' % value)


# =========================================
#       TEST
# --------------------------------------

class TestCase(helper.TestCase):

    # NOTE: quite basic test right now, should add more advanced error message formatting assertions

    def test__import(self):
        self.assertModule(totalrecall)

    def test_timer(self):
        self.assertTrue(hasattr(totalrecall, 'timer'))
        self.assertTrue(callable(totalrecall.timer))

        timer = totalrecall.timer('profile something - using timer', begin = False, enabled = True, verbose = True, colors = True)

        self.assertTrue(isinstance(timer, totalrecall.RuntimeProfilerTimer))

        self.assertTrue(callable(timer.begin))
        self.assertTrue(callable(timer.end))

        sleep(1) # should not have any affect

        timer.begin('task 1')

        sleep(0.1)

        timer.begin('task 2')

        sleep(0.2)

        timer.begin('task 3')

        sleep(0.3)

        timer.end()

        self.assertEquals(significant_decimal(timer.time), 0.6)

        self.assertTrue(isinstance(timer.steps, list))
        self.assertEqual(len(timer.steps), 3)

        self.assertEqual(timer.steps[0].label, 'task 1')
        self.assertEqual(significant_decimal(timer.steps[0].time), 0.1)

        self.assertEqual(timer.steps[1].label, 'task 2')
        self.assertEqual(significant_decimal(timer.steps[1].time), 0.2)

        self.assertEqual(timer.steps[2].label, 'task 3')
        self.assertEqual(significant_decimal(timer.steps[2].time), 0.3)

    def test_context(self):
        self.assertTrue(hasattr(totalrecall, 'context'))
        self.assertTrue(callable(totalrecall.context))

        timer = totalrecall.context('profile something 2 - using context')

        with timer: # for testing mainly, in real code would be `with totalrecall.context('profile something 2 - using context'):`
            sleep(0.001)

        self.assertEquals(math.floor(timer.time * 1000) / 1000, 1.0 / 1000)

    def test_function(self):
        pass
        # self.assertTrue(hasattr(totalrecall, 'function'))
        # self.assertTrue(callable(totalrecall.function))

        # timer = totalrecall.function('profile something 3 - using function')

        # @timer
        # def foo():
        #     sleep(0.001)

        # foo()

        # self.assertEquals(math.floor(timer.time * 1000) / 1000, 1.0 / 1000)


# =========================================
#       MAIN
# --------------------------------------

if __name__ == '__main__':
    helper.run(TestCase)
