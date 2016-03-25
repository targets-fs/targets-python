import io
import os
import random
import tempfile


class AtomicLocalFile(io.BufferedWriter):
    """Abstract class to create Target that create
    a tempoprary file in the local filesystem before
    moving it to there final destination

    This class is just for the writing part of the Target. See
    :class:`luigi.file.LocalTarget` for example
    """

    def __init__(self, path):
        self.__tmp_path = self.generate_tmp_path(path)
        self.path = path
        super(AtomicLocalFile, self).__init__(io.FileIO(self.__tmp_path, 'w'))

    def close(self):
        super(AtomicLocalFile, self).close()
        self.move_to_final_destination()

    def generate_tmp_path(self, path):
        return os.path.join(tempfile.gettempdir(), 'luigi-s3-tmp-%09d' % random.randrange(0, 1e10))

    def move_to_final_destination(self):
        raise NotImplementedError()

    def __del__(self):
        if os.path.exists(self.tmp_path):
            os.remove(self.tmp_path)

    @property
    def tmp_path(self):
        return self.__tmp_path

    def __exit__(self, exc_type, exc, traceback):
        " Close/commit the file if there are no exception "
        if exc_type:
            return
        return super(AtomicLocalFile, self).__exit__(exc_type, exc, traceback)
