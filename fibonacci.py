#!/usr/bin/env python3


def last_8(some_int):
    """Return the last 8 digits of an int

    :param int some_int: the number
    :rtype: int
    """

    return int(str(some_int)[-8:])


def optimized_fibonacci(nth_value):
    """
    This function implements the fibonacci. Its assumes the two starting elements as 0 and 1 and calculates the nth
    value.

    Example: nth_value = 6 then next_value will be 8 as the series will be 0,1,1,2,3,5,8 and 8 is the 6 element in the
    fibonacci series

    :param nth_value:
    :return:
    """

    start_value = 0
    next_value = 1

    # Return 0 for 0th position
    if nth_value == 0:
        return 0

    # Start from 1 instead of 0 as the first two values are already provided
    for i in range(1, nth_value):
        start_value, next_value = next_value, start_value + next_value

    return next_value


class SummableSequence(object):
    """
    This class implements a summable function which generalizes the fibonacci code implementation

    """
    series_list = []

    def __init__(self, *initial):
        """
        This function initializes the summable series

        :param initial:
        """
        self.series_list = list(initial)

    def __call__(self, nth_value):
        """

        :param nth_value:
        :return:
        """

        series_length = len(self.series_list)
        if nth_value < series_length:
            return self.series_list[nth_value]

        for i in range(series_length-1, nth_value):
            self.series_list, self.series_list[series_length - 1] = self.series_list[1:] + \
                                                                            self.series_list[:1], sum(self.series_list)

        return self.series_list[series_length - 1]


if __name__ == "__main__":
    print("f(100000)[-8:]", last_8(optimized_fibonacci(100000)))

    new_seq = SummableSequence(5, 7, 11)
    print("new_seq(100000)[-8:]:", last_8(new_seq(100000)))
