import sys


def print_help(args) -> None:
    """
    Prints help message
    """
    help_messages = \
        {'': '''usage: python -m gradetools <command>

These are commands available:

    grade   Run unittests for specified files
    diff    Find diff for specified files
    
    show    Prints out the result of grading

    help    Prints out this help message
        ''',
         'grade': '''
usage: gradetools.py grade NAME "PATTERN"

required arguments:
  NAME              Name to assign to report
  "PATTERN"         Pattern to match files relative to assets/submissions,
                    e.g. "code17262/<id>/a17262.py"
                    <id> matches to all ids from assets/students.csv
        ''',
         'diff': '''
usage: gradetools.py diff NAME "PATTERN"

required arguments:
  NAME              Name to assign to report
  "PATTERN"         Pattern to match files relative to assets/submissions,
                    e.g. "code17262/<id>/a17262.py"
                    <id> matches to all ids from assets/students.csv
        ''',
         'show': '''         
usage: gradetools.py show (grade | diff | ls) NAME
                     [--sort {firstname, lastname, id} [-r]]
                     [--detail ID[, ID]]
                     [-v VERBOSITY]

options:
  grade             Shows grade report
  diff              Shows diff report
  ls                Lists available reports name

required arguments:
  NAME              Name assigned to report

optional arguments:
  --sort            Sort output according to parameter specified
                    (firstname OR lastname OR id)
    -r              Reverse the sort order
  --detail          Shows detailed output:
                     - detailed comparison (diff) (requires 2 ids)
                     - detailed unittest report (grade)
  -v                Specify the verbosity of the output
                    (0-2)(default=1)
        ''',
        }
    try:
        print(help_messages[args[0]], end='')
    except IndexError:
        print(help_messages[''], end='')
    except KeyError:
        print(help_messages[''], end='')


if __name__ == '__main__':
    print_help(sys.argv[1:])
