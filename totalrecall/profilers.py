
# encoding: utf-8

# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()

import sys
import time
import datetime
import re
import inspecta
import uuid

import mybad
import mybase

from attributedict.collections import AttributeDict


# =========================================
#       CONSTANTS
# --------------------------------------

# DEFAULT_NAME = environ.get('NAME', 'default')
# DEFAULT_HOST_NAME = environ.get('HOSTNAME', 'localhost')

# DEFAULT_TMP_PATH = environ.get('TMP', '/tmp')

# DEFAULT_PROFILER_PATH = environ.get('PROFILER_PATH', path.join(DEFAULT_TMP_PATH, 'log'))
# DEFAULT_PROFILER_FILE_EXTENSION = '.log'

# DEFAULT_PROFILER_ID_PREFIX = 'instance'
# DEFAULT_PROFILER_LEVEL = logging.INFO
# DEFAULT_PROFILER_FORMAT = '%(name)s %(asctime)s %(message)s'

DEFAULT_PROFILER_BEGIN = False
DEFAULT_PROFILER_ENABLED = True
DEFAULT_PROFILER_VERBOSE = False
DEFAULT_PROFILER_COLORS = True
DEFAULT_PROFILER_LOGGER = False


# =========================================
#       ERRORS
# --------------------------------------

class ProfilerError(mybad.Error):
    pass


# =========================================
#       CLASSES
# --------------------------------------

class Profiler(mybase.Base):

    @classmethod
    def default(klass):
        if not hasattr(klass, 'instance') or klass.instance is None:
            klass.instance = klass()

        return klass.instance

class RuntimeProfilerTimer(Profiler):

    """
    A timer
    """

    def __init__(self,
        key = None,
        label = None,
        details = None,
        begin = False,
        logger = None,
        enabled = None,
        verbose = None,
        colors = None,
    ):
        super(RuntimeProfilerTimer, self).__init__(
            logger = logger,
        )

        if ' ' in (key or ''):
            label = key
            key = None

        if key is None and label:
            key = re.sub(r'[^\w\d]', '_', label)
            key = re.sub(r'\_{2,}', '_', key)

        self._id = str(uuid.uuid4()).replace('-', '')
        self._label = label
        self._key = key
        self._details = details or {}

        if begin == False:
            begin = False
        else:
            begin = begin or DEFAULT_PROFILER_BEGIN

        if enabled == False:
            enabled = False
        else:
            enabled = enabled or DEFAULT_PROFILER_ENABLED

        if verbose == False:
            verbose = False
        else:
            verbose = verbose or DEFAULT_PROFILER_VERBOSE

        if colors == False:
            colors = False
        else:
            colors = colors or DEFAULT_PROFILER_COLORS

        self._enabled = enabled
        self._verbose = verbose
        self._colors = colors

        self._step = None
        self._steps = []

        if begin:
            self.begin()

    def begin(self,
        key = None,
        label = None,
        details = None,
    ):
        if ' ' in (key or ''):
            label = key
            key = None

        if key is None and label:
            key = re.sub(r'[^\w\d]', '_', label)
            key = re.sub(r'\_{2,}', '_', key)

        details = details or {}

        now = time.time()

        if self._step:
            runtime = now - self._step['begin_at']

            if runtime < 0:
                runtime = 0

            self._step['end_at'] = now
            self._step['time'] = runtime

        _id = self._id
        _index = len(self._steps)

        _begin_at = now
        _end_at = None

        key = key or 'step-{0}'.format(_index)

        self._step = AttributeDict({
            'id': _id,
            'index': _index,

            'begin_at': _begin_at,
            'end_at': _end_at,

            'label': label,
            'key': key,
            'details': details,
        })

        self._steps.append(self._step)

        return self

    def end(self):
        if self._step:
            now = time.time()

            runtime = now - self._step['begin_at']

            self._step['end_at'] = now
            self._step['time'] = runtime

        if self.verbose:
            stats = inspecta.inspect(self.stats,
                colors = self.colors,
            )

        else:
            stats = map(lambda step: {
                (step.key or 'step-{0}'.format(step.index)): step.time
            }, self.stats.steps)
            stats = list(stats)
            stats = inspecta.inspect(stats)

        self._log('{}'.format(stats))

        return self

    def _log(self, *args, **kwargs):
        if self.logger and self.enabled:
            self.logger.info(*args, **kwargs)

    @property
    def enabled(self):
        return self._enabled

    @property
    def verbose(self):
        return self._verbose

    @property
    def colors(self):
        return self._colors

    @property
    def id(self):
        return self._id

    @property
    def label(self):
        return self._label

    @property
    def key(self):
        return self._key

    @property
    def details(self):
        return self._details

    @property
    def begin_at(self):
        if len(self._steps):
            first_step = self._steps[0]

            return first_step['begin_at']

        else:
            return None

    @property
    def end_at(self):
        if len(self._steps):
            last_step = self._steps[-1]

            return last_step['end_at']

        else:
            return None

    @property
    def time(self):
        return (self.end_at or time.time()) - (self.begin_at or time.time())

    @property
    def step(self):
        return self._step

    @property
    def steps(self):
        return self._steps

    @property
    def stats(self):
        return AttributeDict({
            'type': 'Time',

            'id': self.id,
            'key': self.key,
            'label': self.label,

            'begin_at': self.begin_at,
            'end_at': self.end_at,
            'time': self.time,

            'details': self.details,

            'steps': self.steps,

            'enabled': self.enabled,
        })

    @property
    def info(self):
        return self.stats

class RuntimeProfilerContext(Profiler):

    """
    A block timer (context manager)
    """

    def __init__(self,
        key = None,
        label = None,
        details = None,
        logger = None,
        enabled = None,
        verbose = None,
        colors = None,
    ):
        super(RuntimeProfilerContext, self).__init__(
            logger = logger,
        )

        if ' ' in (key or ''):
            label = key
            key = None

        self._key = key
        self._label = label
        self._details = details or {}

        self._logger = logger
        self._enabled = enabled
        self._verbose = verbose
        self._colors = colors

        self._timer = RuntimeProfilerTimer(
            label = self._label,
            key = self._key,
            details = self._details,
            logger = self._logger,
            enabled = self._enabled,
            verbose = self._verbose,
            colors = self._colors,
        )

    def __enter__(self):
        self._timer.begin()

    def __exit__(self, exception_type, exception_value, traceback):
        self._timer.end()

    @property
    def timer(self):
        return self._timer

    @property
    def id(self):
        return self.timer.id

    @property
    def begin_at(self):
        return self.timer.begin_at

    @property
    def end_at(self):
        return self.timer.end_at

    @property
    def time(self):
        return self.timer.time

    @property
    def steps(self):
        return self.timer.steps

    @property
    def stats(self):
        return self.timer.stats

    @property
    def info(self):
        return self.stats

class RuntimeProfilerDecorator(Profiler):

    """
    A function timer (decorator)
    """

    def __init__(self,
        key = None,
        label = None,
        details = None,
        logger = None,
        enabled = None,
        verbose = None,
        colors = None,
    ):
        super(RuntimeProfilerDecorator, self).__init__(
            logger = logger,
        )

        if ' ' in (key or ''):
            label = key
            key = None

        self._key = key
        self._label = label
        self._details = details or {}

        self._logger = logger
        self._enabled = enabled
        self._verbose = verbose
        self._colors = colors

        self._timer = RuntimeProfilerTimer(
            label = self._label,
            key = self._key,
            details = self._details,
            logger = self._logger,
            enabled = self._enabled,
            verbose = self._verbose,
            colors = self._colors,
        )

    def __call__(self, fn):
        try:
            self.key = self.key or fn.__name__
        except:
            pass

        def _function(*args, **kwargs):
            self._timer.begin()

            result = fn(*args, **kwargs)

            self._timer.end()

            return self

        return _function

    @property
    def timer(self):
        return self._timer

    @property
    def id(self):
        return self.timer.id

    @property
    def begin_at(self):
        return self.timer.begin_at

    @property
    def end_at(self):
        return self.timer.end_at

    @property
    def time(self):
        return self.timer.time

    @property
    def steps(self):
        return self.timer.steps

    @property
    def stats(self):
        return self.timer.stats

    @property
    def info(self):
        return self.stats

class RuntimeProfiler(Profiler):

    """
    The actual profiler API - exposes the various profiling helpers.
    """

    def __init__(self, logger = None):
        super(RuntimeProfiler, self).__init__(
            logger = logger,
        )

    @property
    def key(self):
        return 'runtime'

    def function(self, *args, **kwargs):
        return RuntimeProfilerDecorator(*args, **kwargs)

    def context(self, *args, **kwargs):
        return RuntimeProfilerContext(*args, **kwargs)

    def timer(self, *args, **kwargs):
        return RuntimeProfilerTimer(*args, **kwargs)



# =========================================
#       EXPORTS
# --------------------------------------

Profiler = RuntimeProfiler


# =========================================
#       FUNCTIONS
# --------------------------------------

def function(*args, **kwargs):
    return RuntimeProfiler.default().function(*args, **kwargs)

def context(*args, **kwargs):
    return RuntimeProfiler.default().context(*args, **kwargs)

def timer(*args, **kwargs):
    return RuntimeProfiler.default().timer(*args, **kwargs)
