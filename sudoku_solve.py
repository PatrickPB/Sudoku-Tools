import sys, math, time, importlib

debug = False

arg_strings = [sys.argv[i]
               for i in range(1, len(sys.argv))
               if not sys.argv[i - 1].startswith('-') and not sys.argv[i].startswith('-')]
arg_dict = dict([(sys.argv[i], None) for i in range(1, len(sys.argv)) if sys.argv[i].startswith('-')] +
                [(sys.argv[i - 1], sys.argv[i])
                 for i in range(1, len(sys.argv))
                 if sys.argv[i - 1].startswith('-') and not sys.argv[i].startswith('-')])
grids = None
if len(arg_strings) == 1:
    if len(arg_strings[0]) == 81:
        grids = [arg_strings[0]]
        digits = '123456789'
    else:
        print()
        print("a specified suduko grid needs to be 81 cells; for other sizes, use the gridpythonfile input")
if '-g' in arg_dict.keys():
    if arg_dict['-g'].endswith('.py'):
        arg_dict['-g'] = arg_dict['-g'][0:len(arg_dict['-g']) - 3]
    try:
        grids = importlib.import_module(arg_dict['-g'])
        digits = grids.digits
        grids = grids.grids
    except:
        print()
        print(arg_dict['-g'] + ".py is not existing or does not have the correct format (refer to file grids.py)")
if grids is None:
    print()
    print('command line: python3 sudoku_solve ["string with grid to be solved of 81 characters"] [-d] [-g gridpythonfile]"')
    print('   example string: "......19.23....6.....24..........96....16..7..48.7......1..34.5..9..8.....6..58.."')
    print('   for strings of bigger grids like with 256 or 512 cells, use gridpythonfile input')
    print('   gridpythonfile is a filename that contains the digits var & and array of grids')
    print('   -d when using -d option, then grids will not be solved but just printed for easy sudoku user solving')
    print()
    exit()


# the sudoku grid is now a table of 81 cells with each a max 9 character string
# in the table the (row, col) element is represented by cell values[row * 9 + col]
# row & col are numbers <= 8, values[] index be at max 80

mrows, mcols, msqrs = len(digits), len(digits), len(digits)
mcells = mrows * mcols
sqr_width = int(math.sqrt(mrows))
range_all_cells = range(0, mrows * mcols)


def range_row(row_number):
    return list(range(int(row_number * mcols), int((row_number + 1) * mcols)))


def range_column(column_number):
    return list(range(column_number, (mrows * mcols) + column_number, mrows))


def range_square(sqr_number):
    return [
        int(int(int(sqr_number / sqr_width) * (sqr_width * mcols) + int(sqr_number % sqr_width) * sqr_width + z + w))
        for w in list(range(0, (sqr_width * mcols), mcols)) for z in list(range(0, sqr_width))]


def ranges_units(z):
    return [range_row(int(z / mcols)), range_column(int(z % mrows)),
            range_square(int(z / (sqr_width * mcols)) * sqr_width + int(z % mcols) / sqr_width)]


all_rows = [range_row(v) for v in range(0, mrows)]
all_columns = [range_column(v) for v in range(0, mrows)]
all_squares = [range_square(v) for v in range(0, msqrs)]
all_rcs = all_columns + all_rows + all_squares
peers = [list(
    set(range_row(int(v / mcols)) + range_column(v % mrows) + range_square(
        int(v / (sqr_width * mcols)) * sqr_width + int((v % mcols) / sqr_width))) - {v})
    for v in range_all_cells]
all_units = [ranges_units(v) for v in range_all_cells]

#assert (range_row(8) == [72, 73, 74, 75, 76, 77, 78, 79, 80])
#assert (range_column(5) == [5, 14, 23, 32, 41, 50, 59, 68, 77])
#assert (range_square(8) == [60, 61, 62, 69, 70, 71, 78, 79, 80])
#t = 80
#assert (range_row(int(t / 9)) == [72, 73, 74, 75, 76, 77, 78, 79, 80])
#assert (range_column(t % 9) == [8, 17, 26, 35, 44, 53, 62, 71, 80])
#assert (range_square(int(t / 27) * 3 + int(t % 9) / 3) == [60, 61, 62, 69, 70, 71, 78, 79, 80])
#assert (ranges_units(80) == [[72, 73, 74, 75, 76, 77, 78, 79, 80], [8, 17, 26, 35, 44, 53, 62, 71, 80],
#                             [60, 61, 62, 69, 70, 71, 78, 79, 80]])


def intersection_lists(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


assert (intersection_lists(['A', 'B', 'D'], ['A', 'D', 'C']) == ['A', 'D'])
assert (intersection_lists('abcdf', 'abfg') == ['a', 'b', 'f'])
assert (intersection_lists(['a', 'b', 'c', 'd', 'f'], ['a', 'b', 'f', 'g']) == ['a', 'b', 'f'])
assert (intersection_lists([['a', 'b'], ['c', 'd'], ['f']], [['a', 'b', 'c'], ['f'], ['g']]) == [['f']])


def solved(mvalues, msingles):
    if msingles is None:
        return False
    return all(msingles) and \
           all([(''.join(sorted(''.join(mvalues[i] for i in rcs))) == digits) for rcs in all_rcs])


def first_non_single(mvalues):
    for i in range_all_cells:
        if len(mvalues[i]) > 1:
            return i
    return -1


def print_first_fail(mvalues, msingles):
    if msingles is None:
        return 0
    if not all(msingles):
        print("not all single values")
    else:
        for unit in all_rcs:
            if ''.join(sorted(''.join(mvalues[i] for i in unit))) != digits:
                print("failing unit: " + str(unit))
                return
    return


def simple_parse_grid(grid):
    mvalues = [grid[i] if grid[i] in digits else '.' for i in range_all_cells]
    return mvalues


def parse_grid(grid):
    assert(len(grid) == mcells)
    mvalues = [grid[i] if grid[i] in digits else digits for i in range_all_cells]
    msingles = [(len(mvalues[i]) == 1) for i in range_all_cells]
    for i in range_all_cells:
        if msingles[i]:
            mvalues, msingles = propagate(mvalues, msingles, i)
            if not mvalues:
                return None, None
    return mvalues, msingles


def display(mvalues):
    if mvalues is None:
        return
    width = 1 + max(len(mvalues[i]) for i in range_all_cells)
    line_width = width * sqr_width
    line_cell = ''.join(['-' * (line_width - 1)])
    line = (line_cell + '-+-') * (sqr_width - 1) + line_cell
    for r in range(0, mrows):
        print(''.join(
            mvalues[r * mcols + c].center(width) + (
                '| ' if (c != mcols - 1) and (int(c % sqr_width) == sqr_width - 1) else '') for c in
            range(0, mcols)))
        if (r != mcols - 1) and (int(r % sqr_width) == sqr_width - 1):
            print(line)


symbs = {'bl':u'\u255a', 'tl':u'\u2554', 'bm':u'\u2569', 'tl':u'\u2566', 'ml':u'\u2560', 'h':u'\u2550', 'mm':u'\u256c'}

def paperdisplay(mvalues):
    if mvalues is None:
        return
    width = 3 + max(len(mvalues[i]) for i in range_all_cells)
    mvalues1 = [mvalues[i] if mvalues[i] != '.' else ' ' for i in range(len(mvalues))]
    line_width = width * sqr_width
    line_cell = ''.join(['-' * (line_width - 1)])
    line = (line_cell + '-++-') * (sqr_width - 1) + line_cell
    for r in range(0, mrows):
        print(''.join(
            mvalues1[r * mcols + c].center(width) + (
                '|| ' if (c != mcols - 1) and (int(c % sqr_width) == sqr_width - 1) else '') for c in
            range(0, mcols)))
        if (r != mcols - 1) and (int(r % sqr_width) == sqr_width - 1):
            print(line)



# algorithm 1: simply propagating a cell with one digit ot all his peers
def propagate(mvalues, msingles, i):
    #  assert (len(mvalues[i]) == 1)
    value = mvalues[i]
    msingles[i] = True
    for j in peers[i]:
        if mvalues is None:
            return None,None
        if value in mvalues[j]:
            mvalues[j] = mvalues[j].replace(value, '')
            len_cell = len(mvalues[j])
            if len_cell == 0:
                return None, None
            if len_cell == 1:
                mvalues, msingles = propagate(mvalues, msingles, j)
    return mvalues, msingles


# algorithm 2: search for digits that are unique within an unit and then propagate
def search_2_for_naked_digits_in_units(mvalues, msingles):  # check if a digit can only occur on one place in a unit
    now_singles = sum(msingles)
    prev_singles = now_singles - 1
    while prev_singles < now_singles < mcells:
        prev_singles = now_singles
        for unit in all_rcs:
            val = ''.join(mvalues[i] for i in unit)
            if len(val) != len(digits):  # when len(val) == len(digits) the full unit contains single digit cells
                for d in digits:
                    if val.count(d) == 1:
                        for j in unit:
                            if d in mvalues[j] and not msingles[j]:
                                mvalues[j] = d
                                mvalues, msingles = propagate(mvalues, msingles, j)
                                if not mvalues:
                                    return None, None
        now_singles = sum(msingles)
    return mvalues, msingles


# algorithm 3: search for single digits - within a cell - with a double unit intersection
#              and propagate/clear values in intersection units
def search_3_for_digits_with_2_unit_intersection(mvalues, msingles):
    # max 3 digits can have such; above 3 digits always 1 unit intersection
    for unit in all_rcs:
        if not all(msingles[i] for i in unit):
            for d in digits:
                prop_list = []
                for i in unit:
                    if d in mvalues[i]:
                        prop_list = prop_list + [i]
                assert (len(prop_list) > 0)
                intersect = all_units[prop_list[0]]
                for i in range(1, len(prop_list)):
                    intersect = intersection_lists(intersect, all_units[prop_list[i]])
                assert (4 > len(intersect) > 0)
                assert (unit in intersect)
                for iunit in intersect:
                    if iunit != unit:
                        for i in iunit:
                            if i not in prop_list and d in mvalues[i]:
                                if d in mvalues[i]:
                                    mvalues[i] = mvalues[i].replace(d, '')
                                    if len(mvalues[i]) == 1:
                                        mvalues, msingles = propagate(mvalues, msingles, i)
                                        if not mvalues:
                                            return None, None
    return mvalues, msingles


def solve(mvalues, msingles, display_starting_grid):
    if display_starting_grid:
        display(mvalues)
    if msingles is None:
        return None, None
    if sum(msingles) < mcells:
        search_2_for_naked_digits_in_units(mvalues, msingles)
    now_singles = sum(msingles)
    prev_singles = now_singles - 1
    while mcells > now_singles > prev_singles:
        prev_singles = now_singles
        search_3_for_digits_with_2_unit_intersection(mvalues, msingles)
        now_singles = sum(msingles)
    if debug:
        display(mvalues)
        print(all(msingles))
    return mvalues, msingles


def rsolve(mvalues, msingles, display_starting_grid):
    mvalues, msingles = solve(mvalues, msingles, display_starting_grid)
    if debug:
        display(mvalues)
    if msingles is None:
        return None, None
    if sum(msingles) < mcells:
        check_i = first_non_single(mvalues)
        if debug:
            print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
            print("check_cell " + str(check_i) + " with possibilities " + mvalues[check_i])
        test_values = mvalues[check_i]
        passes = 0
        for test_val in test_values:
            mvalues1 = mvalues[:]
            msingles1 = msingles[:]
            if debug:
                display(mvalues)
                print("checking cell " + str(check_i) + " with " + test_val)
            mvalues[check_i] = test_val
            try:
                mvalues, msingles = propagate(mvalues, msingles, check_i)
                mvalues, msingles = rsolve(mvalues, msingles, False)
                assert (solved(mvalues, msingles))
                passes = passes + 1
                break
            except:
                mvalues = mvalues1
                msingles = msingles1
          #  print("passes " + str(passes))
    return mvalues, msingles


print("***************")
print("***************")
fails = 0
max_time, min_time = 0, 0
for k in range(0,len(grids)):
    start = time.time()
    values, sngles = parse_grid(grids[k])
    print("**START************* grid: " + str(k + 1))
    display(simple_parse_grid(grids[k]))
    if '-d' in arg_dict.keys():
        paperdisplay(simple_parse_grid(grids[k]))
    values, sngles = rsolve(values, sngles, display_starting_grid=False)
    print(" ")
    display(values)
    if solved(values, sngles):
        print("SOLVED")
    else:
        print("UNSOLVABLE")
        fails = fails + 1
        print_first_fail(values, sngles)
    now_time = (time.time() - start) * 1000
    print("It took " + str(now_time) + " milli-seconds.")
    max_time = now_time if now_time > max_time else max_time
    min_time = now_time if (now_time < min_time or min_time == 0) else min_time
    print("Maximum time = " + str(max_time) + "ms")
    print("**STOP************** grid: " + str(k + 1))
if fails == 0:
    print("All grids solved...")
    print("Minimum time = " + str(min_time) + "ms")
    print("Maximum time = " + str(max_time) + "ms")

