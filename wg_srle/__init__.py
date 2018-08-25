# -*- coding: utf-8 -*-
"SRLE implementation"


import pkg_resources
import string


__version__ = 'master'
try:
    __version__ = pkg_resources.get_distribution('wg_srle').version
except pkg_resources.DistributionNotFound:
    pass


class SRLE(object):
    """SRLE implementation"""

    ESCAPE = '\\'
    _ESCAPE_BYTE = ESCAPE.encode('ascii')
    _DIGITS_BYTE_SET = {s.encode('ascii') for s in string.digits}

    @property
    def separator(self):
        return self._separator

    def __init__(self, separator='|'):
        """Constructor"""

        self.validate_separator(separator)

        self._separator = separator

        printable = (
            set(string.digits + string.ascii_letters + string.punctuation) -
            {self.ESCAPE}
        )

        #
        # We escape also separator although not required for readability
        # and to avoid bugs if reader use split()
        #
        if separator is not None:
            printable -= set((separator,))

        #
        # Let's create set to optimize search
        #
        self._printable = {c.encode('ascii') for c in printable}

    def _canonilize(self, c):
        """Ensure c is printable and valid"""

        return (
            c.decode('ascii') if c in self._printable
            else '%sx%02x' % (self.ESCAPE, ord(c))
        )

    @staticmethod
    def validate_separator(separator):
        """Validate separator

        It must not be a digit as otherwise we cannot know when next
        entry begins
        """

        if separator is not None:
            if len(separator) != 1:
                raise ValueError('Separator must be a single character')
            if separator not in string.ascii_letters + string.punctuation:
                raise ValueError(
                    'Separator must be be letter but not numeric'
                )

    def encode(self, sin, sout):
        """Encode SRLE from input file into output file"""

        if self._separator is None:
            raise ValueError('Expected explicit separator')

        last = None
        n = None
        while True:
            c = sin.read(1)

            if last != c:
                if last is not None:
                    sout.write(
                        ('%s%s%d' % (
                            self._separator,
                            self._canonilize(last),
                            n,
                        )).encode('ascii')
                    )
                last = c
                n = 1
            else:
                n += 1

            # python does not have do while
            if not c:
                break

    def decode(self, sin, sout):
        """Decode SRLE from input file into output file"""

        # python < 3 does not support nonlocal let's use list
        index = [0]

        def sinread(n):
            r = sin.read(n)
            index[0] += len(r)
            return r

        c = sinread(1)

        if self._separator is not None:
            separator = self._separator.encode('ascii')
        else:
            #
            # guess that 1st char is separator
            #
            try:
                self.validate_separator(c.decode('ascii'))
                separator = c
            except UnicodeDecodeError:
                raise RuntimeError('Unsupported separator %s' % c)

        while c:

            if c != separator:
                raise RuntimeError(
                    "Unexpected '%s' as separator at index %d" % (
                        c,
                        index[0],
                    )
                )

            char = sinread(1)
            if not char:
                raise RuntimeError('Expected character at index %d' % index[0])

            if char == self._ESCAPE_BYTE:
                if sinread(1) != b'x':
                    raise RuntimeError(
                        "Expected 'x' for escape at index %d" % index[0]
                    )
                nbytes = sinread(2)
                if len(nbytes) != 2:
                    raise RuntimeError(
                        "Expected two digits at index %d" % index[0]
                    )
                try:
                    char = bytearray((int(nbytes, 16),))
                except ValueError:
                    raise RuntimeError(
                        'Invalid hex %s at index %d' % (
                            nbytes,
                            index[0],
                        )
                    )

            num = ''
            while True:
                c = sinread(1)
                if not c or c not in self._DIGITS_BYTE_SET:
                    break

                num += c.decode('ascii')

            if not num:
                raise RuntimeError(
                    'Expected numeric value at index %d' % index[0]
                )

            sout.write(char * int(num))
