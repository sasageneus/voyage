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


def compare_files(file_name1, file_name2):
    print('')
    print('Compare files:\n\t%s\n\t%s' % (file_name1, file_name2))
    file1 = open(file_name1)
    file2 = open(file_name2)

    file2_iter = iter(file2)
    for line in file1:
        line2 = next(file2_iter)
        if line != line2:
            print('Compare fail:\n' + line + line2 )
            return False

    return True
    
