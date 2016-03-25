# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


class Format(object):
    """
    Interface for format specifications.
    """

    @classmethod
    def pipe_reader(cls, input_pipe):
        raise NotImplementedError()

    @classmethod
    def pipe_writer(cls, output_pipe):
        raise NotImplementedError()

    def __rshift__(a, b):
        return ChainFormat(a, b)


class ChainFormat(Format):

    def __init__(self, *args, **kwargs):
        self.args = args
        try:
            self.input = args[0].input
        except AttributeError:
            pass
        try:
            self.output = args[-1].output
        except AttributeError:
            pass
        if not kwargs.get('check_consistency', True):
            return
        for x in range(len(args) - 1):
            try:
                if args[x].output != args[x + 1].input:
                    raise TypeError(
                        'The format chaining is not valid, %s expect %s'
                        'but %s provide %s' % (
                            args[x].__class__.__name__,
                            args[x].input,
                            args[x + 1].__class__.__name__,
                            args[x + 1].output,
                        )
                    )
            except AttributeError:
                pass

    def pipe_reader(self, input_pipe):
        for x in reversed(self.args):
            input_pipe = x.pipe_reader(input_pipe)
        return input_pipe

    def pipe_writer(self, output_pipe):
        for x in reversed(self.args):
            output_pipe = x.pipe_writer(output_pipe)
        return output_pipe


class NopFormat(Format):
    def pipe_reader(self, input_pipe):
        return input_pipe

    def pipe_writer(self, output_pipe):
        return output_pipe
