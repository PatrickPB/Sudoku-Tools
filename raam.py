import math

# double lines for drawing boxes
# t = top, l = left, m = mid, r = right, b = bottom, h = horizontal, v = vertical
# mm_h2 == mid-mid with horizontal double line, mm_v2 = same position with vertical double line
dsymbs = {'tl': u'\u2554', 'tm': u'\u2566', 'tr': u'\u2557',
          'ml': u'\u2560', 'mm': u'\u256c', 'mr': u'\u2563',
          'bl': u'\u255a', 'bm': u'\u2569', 'br': u'\u255d',
          'h': u'\u2550', 'v': u'\u2551', }
# single lines for drawing boxes
ssymbs = {'tl': u'\u250c', 'tm': u'\u252c', 'tr': u'\u2510',
          'ml': u'\u251c', 'mm': u'\u253c', 'mr': u'\u2524',
          'bl': u'\u2514', 'bm': u'\u2534', 'br': u'\u2518',
          'h': u'\u2500', 'v': u'\u2502', }
# double/single lines for drawing boxes
dssymbs = {'tm': u'\u2564',
           'ml': u'\u255F', 'mm_h2': u'\u256A', 'mm_v2': u'\u256B', 'mr': u'\u2562',
           'bm': u'\u2567'}


grid_digits = { 81:'123456789', 256:'1234567890ABCDEF', 625:'ABCDEFGHIJKLMNOPQRSTUVWXY'}

def print_paper_grid(grid):
    if len(grid) in grid_digits.keys():
        digits = grid_digits[len(grid)]
    else:
        print("error: invalid grid size!")
        return
    wspaces = '  '
    width = len(wspaces) * 2 + 1
    mcols, mrows = len(digits), len(digits)
    sqr_width = int(math.sqrt(mcols))
    range_all_cells = range(0, mrows * mcols)

    topline = dsymbs['tl'] + (
            (dsymbs['h'] * width + dssymbs['tm']) * (sqr_width - 1) + dsymbs['h'] * width + dsymbs['tm']) * (
                      sqr_width - 1) + (
                      (dsymbs['h'] * width + dssymbs['tm']) * (sqr_width - 1) + dsymbs['h'] * width + dsymbs['tr'])
    regline = dsymbs['v'] + ((' ' * width + ssymbs['v']) * (sqr_width - 1) + ' ' * width + dsymbs['v']) * (
                sqr_width - 1) + (
                      (' ' * width + ssymbs['v']) * (sqr_width - 1) + ' ' * width + dsymbs['v'])
    dmidline = dsymbs['ml'] + (
            (dsymbs['h'] * width + dssymbs['mm_h2']) * (sqr_width - 1) + dsymbs['h'] * width + dsymbs['mm']) * (
                       sqr_width - 1) + (
                       (dsymbs['h'] * width + dssymbs['mm_h2']) * (sqr_width - 1) + dsymbs['h'] * width + dsymbs['mr'])
    smidline = dssymbs['ml'] + (
            (ssymbs['h'] * width + ssymbs['mm']) * (sqr_width - 1) + ssymbs['h'] * width + dssymbs['mm_v2']) * (
                       sqr_width - 1) + (
                       (ssymbs['h'] * width + ssymbs['mm']) * (sqr_width - 1) + ssymbs['h'] * width + dssymbs['mr'])
    botline = dsymbs['bl'] + (
            (dsymbs['h'] * width + dssymbs['bm']) * (sqr_width - 1) + dsymbs['h'] * width + dsymbs['bm']) * (
                      sqr_width - 1) + (
                      (dsymbs['h'] * width + dssymbs['bm']) * (sqr_width - 1) + dsymbs['h'] * width + dsymbs['br'])
    pgrid = [grid[i] if grid[i] != '.' else ' ' for i in range_all_cells]
    for j in range_all_cells:
        if j == 0:
            print(topline)
            print(dsymbs['v'] + wspaces,end='' )
        else:
            if j % (mcols * sqr_width) == 0:
                print()
                print(regline)
                print(dmidline)
                print(dsymbs['v'] + wspaces, end='')
            else:
                if j % mcols == 0:
                    print()
                    print(regline)
                    print(smidline)
                    print(dsymbs['v'] + wspaces, end='')
        if (j + 1) % sqr_width == 0:
            print(pgrid[j] + wspaces + dsymbs['v'] + wspaces, end='')
        else:
            print(pgrid[j] + wspaces + ssymbs['v'] + wspaces, end='')
    print()
    print(regline)
    print(botline)

if __name__ == "__main__":
    grid9 = '.691.7...4..2.896.5...6.1...9.47.28.7.458..96..56....71.7.....993671452.25.9.6...'
    grid16 = '8..4....E.6ABF375.D1.E26.F3.8..4..F..04...5.A..66.E...3.C04.9.15..15E26.F37.....AE..F37.048..1....3..4..15..E.6A.0.8.59D2.A...7...8.5..1.A..37B.F..B48.05.D1....D15.26A.37.....C..6A...F48.0.5.............459.115.D6A..7B..48...7B.8C04.D...AE248....15..26.B.3'
    print_paper_grid(grid9)
    #print_paper_grid(grid16)

