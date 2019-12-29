#!/usr/bin/env python3
"""Print a pyramid to the terminal

A pyramid of height 3 would look like:

--=--
-===-
=====

"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter


def print_pyramid(rows):
    """Print a pyramid of a given height

    Args: number of rows to print
    Output: prints the pyramid

    Example : input rows = 2
              output = -=-
                       ===

    :param int rows: total height
    """
    if (isinstance(rows, int) is False) or (rows <= 0):
        print('Please enter number greater than 0')
        return

    for repeat_stars in range(1, rows + 1):
        repeat_dashes = rows - repeat_stars
        print("-" * repeat_dashes + "=" * (2 * repeat_stars - 1) + "-" * repeat_dashes)


if __name__ == "__main__":
    parser = ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument("-r", "--rows", default=10, type=int, help="Number of rows")

    args = parser.parse_args()
    print_pyramid(args.rows)
