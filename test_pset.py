import signal
import sys
from contextlib import contextmanager
from io import StringIO
from time import sleep, time
from unittest import TestCase, main

from fibonacci import SummableSequence, last_8, optimized_fibonacci
from pyramid import print_pyramid

try:
    # Absent on Windows, trigger AttributeError
    signal.alarm

    def _timeout(signum, frame):
        raise TimeoutError()

    signal.signal(signal.SIGALRM, _timeout)

    @contextmanager
    def timeout(seconds=1, message="Timeout!"):
        # NB: doesn't work on windows
        signal.alarm(seconds)
        try:
            yield
        except TimeoutError:
            raise TimeoutError(message)
        finally:
            signal.alarm(0)


except AttributeError:

    @contextmanager
    def timeout(seconds=1, message="Timeout!"):
        t0 = time()
        yield
        if time() - t0 > seconds:
            raise TimeoutError(message)


@contextmanager
def capture_print():
    _stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        yield sys.stdout
    finally:
        sys.stdout = _stdout


class FibTests(TestCase):

    test_scenario = [
            # Check progressively more complex values, see if time out
            (0, 0),
            (1, 1),
            (6, 8),
            (10, 55),
            (15, 610),
            (20, 6765),
            (30, 832040),
            (40, 102334155),
            (100, 354224848179261915075),
        ]

    def test_fibonnacci(self):
        for n, expected in self.test_scenario:
            with timeout(message="Timeout running f({})".format(n)):
                self.assertEqual(optimized_fibonacci(n), expected)

    def test_summable(self):
        for n, expected in self.test_scenario:
            with timeout(message="Timeout running f({})".format(n)):
                ss = SummableSequence(0, 1)
                self.assertEqual(ss(n), expected)

        for n, expected in [
                    # Check progressively more complex values, see if time out
                    (0, 5),
                    (1, 7),
                    (2, 11),
                    (3, 23),
                    (4, 41),
                ]:
                    with timeout(message="Timeout running f({})".format(n)):
                        ss = SummableSequence(5, 7, 11)
                        self.assertEqual(ss(n), expected)


class TestTimeout(TestCase):
    def test_timeout(self):
        with self.assertRaises(TimeoutError):
            with timeout():
                sleep(2)


class MiscTests(TestCase):
    def test_8(self):
        self.assertEqual(123, last_8(123))
        self.assertEqual(last_8(123456789), 23456789)


class PyramidTests(TestCase):
    def _assert_expected(self, rows, expected):
        with capture_print() as std:
            print_pyramid(rows)

        std.seek(0)
        captured = std.read()

        self.assertEqual(captured, expected)

    def test_pyramid_char(self):
        self._assert_expected("a", "Please enter number greater than 0\n")

    def test_pyramid_negetative(self):
        self._assert_expected(-1, "Please enter number greater than 0\n")

    def test_pyramid_zero(self):
        self._assert_expected(0, "Please enter number greater than 0\n")

    def test_pyramid_one(self):
        self._assert_expected(1, "=\n")

    def test_pyramid_two(self):
        self._assert_expected(2, "-=-\n" + "===\n")

    def test_pyramid_five(self):
        self._assert_expected(5, "----=----\n" + "---===---\n"+"--=====--\n"+"-=======-\n"+"=========\n")


if __name__ == "__main__":
    main()
