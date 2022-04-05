# Sudoku-Tools
Tools for generating valid Sudoku's and for solving Sudoku's



All files should be run with python3, sudoku_print.py will not work when not using Python 3
This tool works for sudoku grids with 81, 256 or 625 cells.



-----
**sudoku_generate.py : tool for generating sudoku's**

command line: python3 sudoku_generate [-s dd] [-w ww] [-n nn] [-o outputgridfile]"')

    example string: "......19.23....6.....24..........96....16..7..48.7......1..34.5..9..8.....6..58.."
    dd defaults to 9, and can be set to 16, 25 for respectively a grid with 81, 256, 625 cells
    ww defaults to 55%, represents the percentage of the cells that needs to be put to unknown
    nn defaults to 100, represents the number of grids to be generated
    outputgridfile is the outputfile - if not ending with .py, will be extended with .py
---------
**sudoku_solve.py : tool for solving whatever sudoku's it is offered**

command line: python3 sudoku_solve ["string with grid to be solved of 81 characters"] [-d] [-g gridpythonfile]"

    example string: "......19.23....6.....24..........96....16..7..48.7......1..34.5..9..8.....6..58.."
    for strings of bigger grids like with 256 or 512 cells, use gridpythonfile input
    gridpythonfile is a filename that contains the digits var & and array of grids
    -d when using -d option, then grids will not be solved but just printed for easy sudoku user solving

---------
**sudoku_print.py : tool for printing sudoku's**

command line: python3 sudoku_print ["string with grid to be solved of 81 characters"] [[-g gridpythonfile] [-n x]]

    only one of both options can be shown a string or a file
    example string: "......19.23....6.....24..........96....16..7..48.7......1..34.5..9..8.....6..58.."
    for strings of bigger grids like with 256 or 512 cells, use gridpythonfile input
    gridpythonfile is a filename that contains the a grids array
    -n x if -n is specified only grid i will be printed, if -n is not specified all grids will be printed

---
**gridpythonfile** examples can be generated with sudoku_generate.py or can be created manually, some examples are included in the repository see the files grid*.py