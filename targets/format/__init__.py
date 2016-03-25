import os

from targets import six
from targets.format.format import Format, NopFormat
from targets.format.wrapped import TextFormat, MixedUnicodeBytesFormat, NewlineFormat
from targets.format.compression import GzipFormat, Bzip2Format

Text = TextFormat()
UTF8 = TextFormat(encoding='utf8')
Nop = NopFormat()
SysNewLine = NewlineFormat()
Gzip = GzipFormat()
Bzip2 = Bzip2Format()
MixedUnicodeBytes = MixedUnicodeBytesFormat()


def get_default_format():
    if six.PY3:
        return Text
    elif os.linesep == '\n':
        return Nop
    else:
        return SysNewLine
