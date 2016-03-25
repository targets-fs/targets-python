import io
import locale
import os
import re
import warnings

from targets import six
from targets.format.format import Format


class BaseWrapper(object):

    def __init__(self, stream, *args, **kwargs):
        self._stream = stream
        try:
            super(BaseWrapper, self).__init__(stream, *args, **kwargs)
        except TypeError:
            pass

    def __getattr__(self, name):
        if name == '_stream':
            raise AttributeError(name)
        return getattr(self._stream, name)

    def __enter__(self):
        self._stream.__enter__()
        return self

    def __exit__(self, *args):
        self._stream.__exit__(*args)

    def __iter__(self):
        try:
            for line in self._stream:
                yield line
        finally:
            self.close()


class MixedUnicodeBytesWrapper(BaseWrapper):
    """
    """

    def __init__(self, stream, encoding=None):
        if encoding is None:
            encoding = locale.getpreferredencoding()
        self.encoding = encoding
        super(MixedUnicodeBytesWrapper, self).__init__(stream)

    def write(self, b):
        self._stream.write(self._convert(b))

    def writelines(self, lines):
        self._stream.writelines((self._convert(line) for line in lines))

    def _convert(self, b):
        if isinstance(b, six.text_type):
            b = b.encode(self.encoding)
            warnings.warn('Writing unicode to byte stream', stacklevel=2)
        return b


class FileWrapper(object):
    """
    Wrap `file` in a "real" so stuff can be added to it after creation.
    """

    def __init__(self, file_object):
        self._subpipe = file_object

    def __getattr__(self, name):
        # forward calls to 'write', 'close' and other methods not defined below
        return getattr(self._subpipe, name)

    def __enter__(self, *args, **kwargs):
        # instead of returning whatever is returned by __enter__ on the subpipe
        # this returns self, so whatever custom injected methods are still available
        # this might cause problems with custom file_objects, but seems to work
        # fine with standard python `file` objects which is the only default use
        return self

    def __exit__(self, *args, **kwargs):
        return self._subpipe.__exit__(*args, **kwargs)

    def __iter__(self):
        return iter(self._subpipe)


class NewlineWrapper(BaseWrapper):

    def __init__(self, stream, newline=None):
        if newline is None:
            self.newline = newline
        else:
            self.newline = newline.encode('ascii')

        if self.newline not in (b'', b'\r\n', b'\n', b'\r', None):
            raise ValueError("newline need to be one of {b'', b'\r\n', b'\n', b'\r', None}")
        super(NewlineWrapper, self).__init__(stream)

    def read(self, n=-1):
        b = self._stream.read(n)

        if self.newline == b'':
            return b

        if self.newline is None:
            newline = b'\n'

        return re.sub(b'(\n|\r\n|\r)', newline, b)

    def writelines(self, lines):
        if self.newline is None or self.newline == '':
            newline = os.linesep.encode('ascii')
        else:
            newline = self.newline

        self._stream.writelines(
            (re.sub(b'(\n|\r\n|\r)', newline, line) for line in lines)
        )

    def write(self, b):
        if self.newline is None or self.newline == '':
            newline = os.linesep.encode('ascii')
        else:
            newline = self.newline

        self._stream.write(re.sub(b'(\n|\r\n|\r)', newline, b))


class TextWrapper(io.TextIOWrapper):

    def __exit__(self, *args):
        # io.TextIOWrapper close the file on __exit__, let the underlying file decide
        if not self.closed and self.writable():
            super(TextWrapper, self).flush()

        self._stream.__exit__(*args)

    def __del__(self, *args):
        # io.TextIOWrapper close the file on __del__, let the underlying file decide
        if not self.closed and self.writable():
            super(TextWrapper, self).flush()

        try:
            self._stream.__del__(*args)
        except AttributeError:
            pass

    def __init__(self, stream, *args, **kwargs):
        self._stream = stream
        try:
            super(TextWrapper, self).__init__(stream, *args, **kwargs)
        except TypeError:
            pass

    def __getattr__(self, name):
        if name == '_stream':
            raise AttributeError(name)
        return getattr(self._stream, name)

    def __enter__(self):
        self._stream.__enter__()
        return self


class WrappedFormat(Format):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def pipe_reader(self, input_pipe):
        return self.wrapper_cls(input_pipe, *self.args, **self.kwargs)

    def pipe_writer(self, output_pipe):
        return self.wrapper_cls(output_pipe, *self.args, **self.kwargs)


class TextFormat(WrappedFormat):

    input = 'unicode'
    output = 'bytes'
    wrapper_cls = TextWrapper


class MixedUnicodeBytesFormat(WrappedFormat):

    output = 'bytes'
    wrapper_cls = MixedUnicodeBytesWrapper


class NewlineFormat(WrappedFormat):

    input = 'bytes'
    output = 'bytes'
    wrapper_cls = NewlineWrapper
