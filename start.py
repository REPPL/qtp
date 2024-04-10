import argparse

from app.textplot import QuickTextPlot


NAME = 'start.py'
DESCRIPTION = '''
A Python script to visualise text highlights.
'''
EPILOG = '''
This programme remains work in progress.
'''


def main():
    '''Using `argparse` to initialise project.

    For `argparse`, see:
    https://docs.python.org/3/library/argparse.html
    '''

    parser = argparse.ArgumentParser(
        prog=NAME,
        description=DESCRIPTION.strip(),
        epilog=EPILOG.strip(),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'name',
        help='Unique project name required')
    parser.add_argument(
        '-a', '--anonymise',
        action='store_const',
        const='#',
        default=None,
        required=False,
        dest='anonymise',
        help='Overwrite alphanumerical characters with given value'),
    parser.add_argument(
        '-m', '--mix_colours',
        action='store_true',
        default=False,
        required=False,
        dest='mix_colours',
        help='Mix colours of multiple highlights (experimental!)'),
    parser.add_argument(
        '-s', '--show',
        action='store_true',
        required=False,
        dest='show',
        help='Show plot in a separate window'),
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        required=False,
        dest='verbose',
        help='Print status messages to console'),
    _ = QuickTextPlot(parser.parse_args())


if __name__ == '__main__':
    main()
