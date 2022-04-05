import sys, importlib
import raam

def print_legend():
    print()
    print('command line: python3 sudoku_print ["string with grid to be solved of 81 characters"] [[-g gridpythonfile] [-n x]]')
    print('   only one of both options can be shown a string or a file')
    print('   example string: "......19.23....6.....24..........96....16..7..48.7......1..34.5..9..8.....6..58.."')
    print('   for strings of bigger grids like with 256 or 512 cells, use gridpythonfile input')
    print('   gridpythonfile is a filename that contains the a grids array')
    print('   -n x if -n is specified only grid i will be printed, if -n is not specified all grids will be printed')
    print()
    exit()

arg_strings = [sys.argv[i]
               for i in range(1, len(sys.argv))
               if not sys.argv[i - 1].startswith('-') and not sys.argv[i].startswith('-')]
arg_dict = dict([(sys.argv[i], None) for i in range(1, len(sys.argv)) if sys.argv[i].startswith('-')] +
                [(sys.argv[i - 1], sys.argv[i])
                 for i in range(1, len(sys.argv))
                 if sys.argv[i - 1].startswith('-') and not sys.argv[i].startswith('-')])
gridss = None
if len(arg_strings) == 1:
    if len(arg_strings[0]) == 81:
        gridss = arg_strings[0]
    else:
        print()
        print("a specified suduko grid needs to be 81 cells; for other sizes, use the gridpythonfile input")
grids = None
if '-g' in arg_dict.keys():
    if arg_dict['-g'].endswith('.py'):
        arg_dict['-g'] = arg_dict['-g'][0:len(arg_dict['-g']) - 3]
    try:
        grids = importlib.import_module(arg_dict['-g'])
        grids = grids.grids
    except:
        print()
        print(arg_dict['-g'] + ".py is not existing or does not have the correct format (refer to file grids.py)")
n = 0
if '-n' in arg_dict.keys():
    try:
        n = int(arg_dict['-n'])
    except:
        pass


if (gridss is None and grids is None) or (gridss is not None and grids is not None):
    print_legend()
if gridss is not None:
    raam.print_paper_grid(gridss)
else:
    if grids is not None:
        if n == 0:
            for g in grids:
                raam.print_paper_grid(g)
        else:
            if n <= len(grids):
                raam.print_paper_grid(grids[n - 1])
            else:
                print('error: index not available in grid array')
                print_legend()

