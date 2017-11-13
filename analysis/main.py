
import sys
import getopt

from storage import Storage


def main_args(argv):
    main()


def main():
    storage = Storage()

if __name__ == "__main__":
    main_args(sys.argv[1:])
