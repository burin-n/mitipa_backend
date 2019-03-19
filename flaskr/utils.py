import sys


def secure_filename(filename):
    return filename


def allowed_file(filename):
    return True


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def secure_filename(filename):
	return filename


def allowed_file(filename):
	return True
