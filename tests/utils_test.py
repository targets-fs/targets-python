import os
import unittest


def skipOnTravis(reason):
    return unittest.skipIf(os.getenv('TRAVIS') == 'true', reason)


def with_config(config, replace_sections=False):
    return unittest.skipIf(True, "We do not support configuration for now")
