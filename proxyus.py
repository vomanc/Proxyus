# This is the main function that runs the script.
# installation and launch are described in file README.
# It is a freeware program that anyone can use !
# author: @vomanc
# version 4.0
# https://github.com/vomanc/Proxyus
import argparse
import asyncio
import logging
from extension import BANNER
from searcher import SearchProxies
from checker import ProxyChecker


def init_logger():
    """ Set logger """
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
    """ For save results in file """
    with open(file_name, 'w', encoding='utf-8') as my_file:
        my_file.write(str(data))


def argument_parser():
    """ Setting options for the program """
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
    return parser.parse_args()


async def main():
    """ Main function that starts the program """
    args = argument_parser()
    results = SearchProxies(args.d, args.tor)
    await results.run_parser()

    print(f'[+] Found {len(results.proxy_lists)} pieces')
    if args.o:
        save_file(args.o, results.proxy_lists)
    if args.c:
        print(f'[*] Please wait, proxy checking in progress ... \n{"_" * 45} \n',
              f'Status | Country | Type | Proxy\n{"_" * 45}')
        checker_run = ProxyChecker()
        checker_run.results(results.proxy_lists)
    if args.c is False and args.o is None:
        print(results.proxy_lists)


if __name__ == "__main__":
    VERSION = '4.0'
    logger = logging.getLogger('app')
    print(BANNER)
    init_logger()
    logger.debug('start')
    try:
        asyncio.run(main())
        logger.debug('Successfully wrote')
    except Exception:
        logger.exception("Error message")
    print('\n')
