import random, math, sys

debug = False

arg_strings = [sys.argv[i]
               for i in range(1, len(sys.argv))
               if not sys.argv[i - 1].startswith('-') and not sys.argv[i].startswith('-')]
arg_dict = dict([(sys.argv[i], None) for i in range(1, len(sys.argv)) if sys.argv[i].startswith('-')] +
                [(sys.argv[i - 1], sys.argv[i])
                 for i in range(1, len(sys.argv))
                 if sys.argv[i - 1].startswith('-') and not sys.argv[i].startswith('-')])

digitss = { 9:'123456789', 16:'0123456789ABCDEF', 25:'ABCDEFGHIJKLMNOPQRSTUVWXY'  }
s = 9
try:
    s = int(arg_dict['-s'])
    if not (s == 9 or s == 16 or s == 25):
        s = 9
except:
    pass
digits = digitss[s]

w = 55
try:
    w = int(arg_dict['-w'])
    if w > 100: w = 100
except:
    pass
blanks = int(len(digits) * len(digits) * w / 100)

number = 10
try:
    number = int(arg_dict['-n'])
except:
    pass

ofile = None
if '-o' in arg_dict.keys():
    ofile = arg_dict['-o']
    if len(ofile) > 0:
        if not str(ofile).endswith('.py'):
            ofile = str(ofile) + 'py'


if ofile is None:
    print()
    print('command line: python3 sudoku_generate [-s dd] [-w ww] [-n nn] [-o outputgridfile]"')
    print('   example string: "......19.23....6.....24..........96....16..7..48.7......1..34.5..9..8.....6..58.."')
    print('   dd defaults to 9, and can be set to 16, 25 for respectively a grid with 81, 256, 625 cells')
    print('   ww defaults to 55%, represents the percentage of the cells that needs to be put to unknown')
    print('   nn defaults to 100, represents the number of grids to be generated')
    print('   outputgridfile is the outputfile - if not ending with .py, will be extended with .py')
    print()
    exit()


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


def intersection_lists(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def solved(mvalues, msingles):
    return all(msingles) and \
           all([(''.join(sorted(''.join(mvalues[i] for i in rcs))) == digits) for rcs in all_rcs])


def first_non_single(mvalues):
    for i in range_all_cells:
        if len(mvalues[i]) > 1:
            return i
    return -1


def print_first_fail(mvalues, msingles):
    if not all(msingles):
        print("not all single values")
    else:
        for unit in all_rcs:
            if ''.join(sorted(''.join(mvalues[i] for i in unit))) != digits:
                print("failing unit: " + str(unit))
                return
    return


def simple_parse_grid(grid):
    return [grid[i] if grid[i] in digits else '.' for i in range_all_cells]


def parse_grid(grid):
    if not (len(grid) == mcells):
        if debug: print("reach - 2, invalid grid size")
    mvalues = [grid[i] if grid[i] in digits else digits for i in range_all_cells]
    msingles = [(len(mvalues[i]) == 1) for i in range_all_cells]
    for i in range_all_cells:
        if msingles[i]:
            mvalues, msingles = algo_1_propagate(mvalues, msingles, i)
            if not mvalues:
                if debug: print("reach -1, invalid grid, failed on cell ", i)
                return None, None
    return mvalues, msingles


def display(mvalues):
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


# algorithm 1: simply propagating a cell with one digit ot all his peers
def algo_1_propagate(mvalues, msingles, i):
    #  assert (len(mvalues[i]) == 1)
    value = mvalues[i]
    msingles[i] = True
    for j in peers[i]:
        if value in mvalues[j]:
            mvalues[j] = mvalues[j].replace(value, '')
            len_cell = len(mvalues[j])
            if len_cell == 0:
                return None, None
            if len_cell == 1:
                mvalues, msingles = algo_1_propagate(mvalues, msingles, j)
                if mvalues is None:
                    return None, None
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
                                mvalues, msingles = algo_1_propagate(mvalues, msingles, j)
                                if mvalues is None:
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
                if len(prop_list) == 0:
                    return None, None
                intersect = all_units[prop_list[0]]
                for i in range(1, len(prop_list)):
                    intersect = intersection_lists(intersect, all_units[prop_list[i]])
                if not (4 > len(intersect) > 0) and not (unit in intersect):
                    return None, None
                for iunit in intersect:
                    if iunit != unit:
                        for i in iunit:
                            if i not in prop_list and d in mvalues[i]:
                                if d in mvalues[i]:
                                    mvalues[i] = mvalues[i].replace(d, '')
                                    if len(mvalues[i]) == 1:
                                        mvalues, msingles = algo_1_propagate(mvalues, msingles, i)
                                        if not mvalues:
                                            return None, None
    return mvalues, msingles


def solve(mvalues, msingles):
    if mvalues is not None and msingles is not None and sum(msingles) < mcells:
        mvalues, msingles = search_2_for_naked_digits_in_units(mvalues, msingles)
        if mvalues is not None and msingles is not None:
            now_singles = sum(msingles)
            prev_singles = now_singles - 1
            while mcells > now_singles > prev_singles:
                prev_singles = now_singles
                mvalues, msingles = search_3_for_digits_with_2_unit_intersection(mvalues, msingles)
                if mvalues is None:
                    return None, None
                now_singles = sum(msingles)
    return mvalues, msingles


def rsolve(mvalues, msingles):
    if mvalues is None or msingles is None:
        return None, None, 0
    mvalues, msingles = solve(mvalues, msingles)
    if mvalues is None or msingles is None:
        return None, None, 0
    if sum(msingles) == mcells:
        print(">>> a solution")
        display(mvalues)
        return mvalues, msingles, 1
    # now the case when (sum(msingles) < mcells)
    check_i = first_non_single(mvalues)
    digit_i = mvalues[check_i]
    iresults = [0 for i in range(len(digit_i))]
    rmvalues, rmsingles = None, None
    for j in range(len(digit_i)):
        ivalues, isingles = mvalues[:], msingles[:]
        ivalues[check_i] = digit_i[j]
        ivalues, isingles = algo_1_propagate(ivalues, isingles, check_i)
        if ivalues is not None and isingles is not None:
            ivalues, isingles, iresults[j] = rsolve(ivalues, isingles)
            if iresults[j] > 1:
                return ivalues, isingles, sum(iresults)
        if ivalues is None or isingles is None or not solved(ivalues, isingles):
            iresults[j] = 0
        else:
            rmvalues, rmsingles = ivalues, isingles
           # if sum(msingles) == mcells:
            #    display(mvalues)
    return rmvalues, rmsingles, sum(iresults)

# standard grid for 9x9 grid
#       "123456789"
#       "456789123"
#       "789123456"
#       "234567891"
#       "567891234"
#       "891234567"
#       "345678912"
#       "678912345"
#       "912345678"
# strings per row are shifted with 0, 3, 6, 1, 4, 7, 2, 5, 8
# str1 start[i*3+j for j in range(0,3) for i in range(0,3)]


def generate_standard_grid():
    return ''.join([(digits + digits)[i * sqr_width + j: i * sqr_width + j + len(digits)]
                    for j in range(0, sqr_width) for i in range(0, sqr_width)])


def grid_shuffle_sqr_rows_per_sqr_rows(grid):
    start = random.randint(0, sqr_width - 1) * mcols * sqr_width
    return (grid + grid)[start:start + mcells]


def grid_shuffle_rows_within_sqr(grid):
    sqrrow = random.randint(0, sqr_width - 1)
    rows_in_sqr = [i + sqrrow * sqr_width for i in sorted(random.sample(range(0, sqr_width), 2))]
    return grid[0:rows_in_sqr[0] * mcols] + grid[rows_in_sqr[1] * mcols:(rows_in_sqr[1] + 1) * mcols] + \
           grid[(rows_in_sqr[0]) * mcols:rows_in_sqr[1] * mcols] + grid[(rows_in_sqr[1] + 1) * mcols:mcells]


def grid_transpose(grid):
    return ''.join([grid[i * mcols + j:i * mcols + j + 1] for j in range(mcols) for i in range(mcols)])


def generate_random_grid():
    grid = generate_standard_grid()
    shuffle_functions = [grid_transpose, grid_shuffle_rows_within_sqr, grid_shuffle_sqr_rows_per_sqr_rows]
    for i in range(40):
        grid = shuffle_functions[random.randint(0, len(shuffle_functions) - 1)](grid)
    return grid


def grid_mask(grid, amt):
    lgrid = list(grid)
    for i in random.sample(range(0,mcells), amt):
        lgrid[i] = '.'
    return ''.join(lgrid)


grid_no_solution, grid_solved, grid_with_multiple_solutions = 0,0,0
solved_grids = []

for v in range(number):
    print("**")
    print("**START************* grid: " + str(v + 1))
    gridi = generate_random_grid()
    gridi = grid_mask(gridi, blanks)
    display(simple_parse_grid(gridi))
    values, sngles = parse_grid(gridi)
    values, sngles, result = rsolve(values, sngles)
    if result == 0:
        print("NO SOLUTION")
        grid_no_solution += 1
    else:
        if result == 1:
            print("VALID GRID, SOLVED")
            grid_solved +=1
            display(values)
            solved_grids.append(gridi)
        else:
            print("INVALID GRID, MULTIPLE SOLUTIONS, ABOVE SHOWN " + str(result) + " SOLUTIONS")
            grid_with_multiple_solutions += 1
    print("**STOP************** grid: " + str(v + 1))

print(str(number) + " grids randomly generated with " + str(w) + "% blanks results in " + str(len(solved_grids)) + " valid grids.")
print("Saved the " + str(len(solved_grids)) + " valid grids to " + str(ofile) + " .")
if ofile is not None:
    with open(ofile, 'w') as f:
        f.write("digits = '" + digits + "'" + '\n'+ '\n')
        f.write("grids = [")
        for g in solved_grids:
            f.write("'" + g + "',\n" + "         ")
        f.write("] \n")
