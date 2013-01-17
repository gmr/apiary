"""
Core apiary command line application, wraps multiple modules worth of
functionality.

"""
import argparse
import logging

import apiary

LOGGER = logging.getLogger(__name__)

CONFIG_FILE = 'etc/apiary.yaml'
DISTRIBUTION = 'distribution'
IMPORT = 'import'
EXPORT = 'export'

def main():
    """Main application call"""
    args = process_cli_arguments()
    logging.basicConfig(level=logging.INFO if not args.verbose else
                        logging.DEBUG)
    print args





def process_cli_arguments():
    parser = argparse.ArgumentParser(description=apiary.__doc__.strip())

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--import', action='store_const', dest='command',
                       const=IMPORT, help='Import items into Apiary')
    group.add_argument('--export', action='store_const', dest='command',
                       const=EXPORT, help='Export strings from Apiary')

    import_items = parser.add_subparsers(title='Import Items',
                                         description='Available import items')

    distribution = import_items.add_parser('distribution',
                                           help=('Import a distribution from '
                                                 'an ISO file.'))
    distribution.add_argument(dest='name', help='Name of the distribution')
    distribution.add_argument(dest='path', help='Path to the ISO file')

    parser.add_argument('-c', dest='config_file', default=CONFIG_FILE,
                        help='Specify the configuration file.\n'
                             'Default: %s' % CONFIG_FILE)

    parser.add_argument('-u', action='store', dest='username',
                        help='Username to connect as')

    parser.add_argument('-p', action='store', dest='password',
                        help='Password to authenticate with')

    parser.add_argument('--verbose', action='store_true', dest='verbose')

    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
