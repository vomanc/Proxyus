# This is the main function that runs the script.
# installation and launch are described in file README.
# It is a freeware program that anyone can use !
# author: @vomanc
# version 3.0
import argparse
import asyncio
import logging
from extension import BANNER
from searcher import search
from checker import checker_results


def init_logger():
    # Set logger
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='Proxyus.log', mode='a')
    filt = [
        '%(asctime)s', '%(levelname)s', '%(filename)s', '%(lineno)s',
        '%(name)s', '%(module)s', '%(message)s'
        ]
    forma = ' - '.join(filt)
    formatter = logging.Formatter(forma)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def save_file(file_name, data):
    # For save results in file
    with open(file_name, 'w') as f:
        f.write(str(data))


def argument_parser():
    # Setting options for the program
    parser = argparse.ArgumentParser(
        prog=f'proxyus, version: {VERSION}',
        description='Script to interact with shodan.',
        add_help=True
    )
    parser.add_argument(
        '-d',
        type=int,
        help='Deep mode [-d: 1 || 2]'
    )
    parser.add_argument(
        '-o',
        type=str,
        help='Save in file (-o my_files.json)'
    )
    parser.add_argument(
        '--tor',
        action='store_true',
        help='Use TOR when searching (required: apt install tor)'
    )
    parser.add_argument(
        '-c',
        action='store_true',
        help='Check proxy after collection'
    )
    parser.add_argument(
        '-v', '-version',
        action='version', version=f'Proxyus, version: {VERSION}',
        help='Print version number'
    )
    return parser


async def main(parser):
    # Main function that starts the program
    args = parser.parse_args()
    results = await search(args)
    print(f'[+] Found {len(results)} pieces')
    if args.o is not None:
        save_file(args.o, results)
    if args.c is True:
        print('[*] Please wait, proxy checking in progress ...')
        print('_' * 40)
        print('Status | Country | Type | Proxy')
        print('_' * 40)
        checker_results(results)
    if args.c is False and args.o is None:
        print(results)


if __name__ == "__main__":
    VERSION = '3.0'
    logger = logging.getLogger('app')
    print(BANNER)
    init_logger()
    logger.debug('start')
    try:
        asyncio.run(main(argument_parser()))
        logger.debug('Successfully wrote')
    except Exception:
        logger.exception("Error message")
