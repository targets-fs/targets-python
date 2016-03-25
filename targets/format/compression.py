from targets.format.format import Format
from targets.format.pipe_process import InputPipeProcessWrapper, OutputPipeProcessWrapper


class GzipFormat(Format):

    input = 'bytes'
    output = 'bytes'

    def __init__(self, compression_level=None):
        self.compression_level = compression_level

    def pipe_reader(self, input_pipe):
        return InputPipeProcessWrapper(['gunzip'], input_pipe)

    def pipe_writer(self, output_pipe):
        args = ['gzip']
        if self.compression_level is not None:
            args.append('-' + str(int(self.compression_level)))
        return OutputPipeProcessWrapper(args, output_pipe)


class Bzip2Format(Format):

    input = 'bytes'
    output = 'bytes'

    def pipe_reader(self, input_pipe):
        return InputPipeProcessWrapper(['bzcat'], input_pipe)

    def pipe_writer(self, output_pipe):
        return OutputPipeProcessWrapper(['bzip2'], output_pipe)
