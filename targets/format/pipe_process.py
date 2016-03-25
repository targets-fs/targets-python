import io
import os
import signal
import subprocess
import tempfile

from targets.format.wrapped import FileWrapper


class InputPipeProcessWrapper(object):

    def __init__(self, command, input_pipe=None):
        """
        Initializes a InputPipeProcessWrapper instance.

        :param command: a subprocess.Popen instance with stdin=input_pipe and
                        stdout=subprocess.PIPE.
                        Alternatively, just its args argument as a convenience.
        """
        self._command = command

        self._input_pipe = input_pipe
        self._original_input = True

        if input_pipe is not None:
            try:
                input_pipe.fileno()
            except AttributeError:
                # subprocess require a fileno to work, if not present we copy to disk first
                self._original_input = False
                f = tempfile.NamedTemporaryFile('wb', prefix='luigi-process_tmp', delete=False)
                self._tmp_file = f.name
                while True:
                    chunk = input_pipe.read(io.DEFAULT_BUFFER_SIZE)
                    if not chunk:
                        break
                    f.write(chunk)
                input_pipe.close()
                f.close()
                self._input_pipe = FileWrapper(io.BufferedReader(io.FileIO(self._tmp_file, 'r')))

        self._process = command if isinstance(command, subprocess.Popen) else self.create_subprocess(command)
        # we want to keep a circular reference to avoid garbage collection
        # when the object is used in, e.g., pipe.read()
        self._process._selfref = self

    def create_subprocess(self, command):
        """
        http://www.chiark.greenend.org.uk/ucgi/~cjwatson/blosxom/2009-07-02-python-sigpipe.html
        """

        def subprocess_setup():
            # Python installs a SIGPIPE handler by default. This is usually not what
            # non-Python subprocesses expect.
            signal.signal(signal.SIGPIPE, signal.SIG_DFL)

        return subprocess.Popen(command,
                                stdin=self._input_pipe,
                                stdout=subprocess.PIPE,
                                preexec_fn=subprocess_setup,
                                close_fds=True)

    def _finish(self):
        # Need to close this before input_pipe to get all SIGPIPE messages correctly
        self._process.stdout.close()
        if not self._original_input and os.path.exists(self._tmp_file):
            os.remove(self._tmp_file)

        if self._input_pipe is not None:
            self._input_pipe.close()

        self._process.wait()  # deadlock?
        if self._process.returncode not in (0, 141, 128 - 141):
            # 141 == 128 + 13 == 128 + SIGPIPE - normally processes exit with 128 + {reiceived SIG}
            # 128 - 141 == -13 == -SIGPIPE, sometimes python receives -13 for some subprocesses
            raise RuntimeError('Error reading from pipe. Subcommand exited with non-zero exit status %s.' % self._process.returncode)

    def close(self):
        self._finish()

    def __del__(self):
        self._finish()

    def __enter__(self):
        return self

    def _abort(self):
        """
        Call _finish, but eat the exception (if any).
        """
        try:
            self._finish()
        except KeyboardInterrupt:
            raise
        except BaseException:
            pass

    def __exit__(self, type, value, traceback):
        if type:
            self._abort()
        else:
            self._finish()

    def __getattr__(self, name):
        if name in ['_process', '_input_pipe']:
            raise AttributeError(name)
        try:
            return getattr(self._process.stdout, name)
        except AttributeError:
            return getattr(self._input_pipe, name)

    def __iter__(self):
        for line in self._process.stdout:
            yield line
        self._finish()

    def readable(self):
        return True

    def writable(self):
        return False

    def seekable(self):
        return False


class OutputPipeProcessWrapper(object):
    WRITES_BEFORE_FLUSH = 10000

    def __init__(self, command, output_pipe=None):
        self.closed = False
        self._command = command
        self._output_pipe = output_pipe
        self._process = subprocess.Popen(command,
                                         stdin=subprocess.PIPE,
                                         stdout=output_pipe,
                                         close_fds=True)
        self._flushcount = 0

    def write(self, *args, **kwargs):
        self._process.stdin.write(*args, **kwargs)
        self._flushcount += 1
        if self._flushcount == self.WRITES_BEFORE_FLUSH:
            self._process.stdin.flush()
            self._flushcount = 0

    def writeLine(self, line):
        assert '\n' not in line
        self.write(line + '\n')

    def _finish(self):
        """
        Closes and waits for subprocess to exit.
        """
        if self._process.returncode is None:
            self._process.stdin.flush()
            self._process.stdin.close()
            self._process.wait()
            self.closed = True

    def __del__(self):
        if not self.closed:
            self.abort()

    def __exit__(self, type, value, traceback):
        if type is None:
            self.close()
        else:
            self.abort()

    def __enter__(self):
        return self

    def close(self):
        self._finish()
        if self._process.returncode == 0:
            if self._output_pipe is not None:
                self._output_pipe.close()
        else:
            raise RuntimeError('Error when executing command %s' % self._command)

    def abort(self):
        self._finish()

    def __getattr__(self, name):
        if name in ['_process', '_output_pipe']:
            raise AttributeError(name)
        try:
            return getattr(self._process.stdin, name)
        except AttributeError:
            return getattr(self._output_pipe, name)

    def readable(self):
        return False

    def writable(self):
        return True

    def seekable(self):
        return False
