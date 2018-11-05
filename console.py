import sys
from contextlib import redirect_stdout
from contextlib import contextmanager


@contextmanager
def redirect_stdin(file):
    prev_stdin = sys.stdin
    sys.stdin = file
    try:
        yield
    finally:
        sys.stdin = prev_stdin


def to_file(file_name, print_func):
    with open(file_name, 'w') as file:
        with redirect_stdout(file):
            return print_func()


def from_file(file_name, input_func):
    with open(file_name, 'r') as file:
        with redirect_stdin(file):
            return input_func()
