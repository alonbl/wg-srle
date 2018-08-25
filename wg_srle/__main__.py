# -*- coding: utf-8 -*-
"SRLE implementation main"


import argparse
import sys


from . import __version__, SRLE


def parse_args(argv):
    """Argument parsing"""

    parser = argparse.ArgumentParser(
        prog=argv[0],
        description='SRLE',
    )

    parser.add_argument(
        '--version',
        action='version',
        version=__version__,
    )

    subparsers = parser.add_subparsers(
        dest='command',
        title='commands',
        description='valid command',
        help='command help',
    )

    encode_parser = subparsers.add_parser(
        'encode',
        help='encode help',
    )

    # encode

    encode_parser.add_argument(
        '--separator',
        metavar='CHAR',
        default='|',
        help="separator, default '%(default)s'",
    )

    encode_parser.add_argument(
        'input_file',
        metavar='INPUT-FILE',
        help='input file',
    )

    encode_parser.add_argument(
        'output_file',
        metavar='OUTPUT-FILE',
        help='output file',
    )

    # decode

    decode_parser = subparsers.add_parser(
        'decode',
        help='decode help',
    )

    decode_parser.add_argument(
        '--separator',
        metavar='CHAR',
        default=None,
        help='separator, guess if not provided',
    )

    decode_parser.add_argument(
        'input_file',
        metavar='INPUT-FILE',
        help='input file',
    )

    decode_parser.add_argument(
        'output_file',
        metavar='OUTPUT-FILE',
        help='output file',
    )

    args = parser.parse_args(argv[1:])

    try:
        if args.separator is not None:
            SRLE.validate_separator(args.separator)
    except Exception as e:
        parser.error(e)

    return args


def main(argv=sys.argv):
    """Main program"""

    args = parse_args(argv)

    with open(args.input_file, 'rb') as fin:
        with open(args.output_file, 'wb') as fout:
            srle = SRLE(separator=args.separator)
            getattr(srle, args.command)(fin, fout)


if __name__ == '__main__':
    main()
