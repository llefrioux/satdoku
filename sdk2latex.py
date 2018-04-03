# -----------------------------------------------------------------------------
#
# Copyright (C) 2018  Ludovic LE FRIOUX
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------


###### Import all needed packages #####

import argparse
import math


##### Parsing the arguments #####

parser = argparse.ArgumentParser(description="Sudoku (sdk) to LaTeX tabular")

parser.add_argument(dest="sudoku_file", metavar="<sudoku_file>",
                    help="file containing the Sudoku grid")

parser.add_argument("-s", dest="N", metavar="<sudoku_size>", default=9,
                    type=int, help="size of the sudoku grid, default is 9")

args = parser.parse_args()


##### Functions #####

# Print a sudoku grid in a LaTeX tabular
def print_latex_grid(grid):
   region_size = int(math.sqrt(args.N))

   header = "\\begin{tabular}{!{\\vrule width 1pt}"
   for i in range(1, args.N + 1):
      if i % region_size == 0:
         header += "c!{\\vrule width 1pt}"
      else:
         header += "c|"
   header += "}"
   print(header)

   for i in range(args.N):
      if i % region_size == 0:
         print("   \\noalign{\\hrule height 1pt}")
      else:
         print("   \\hline")

      line = ["$" + str(grid[i][j]) + "$" for j in range(args.N)]
      print("   ", end="")
      print(*line, sep=" & ", end=" \\\\\n")

   print("   \\noalign{\\hrule height 1pt}")
   print("\\end{tabular}")


##### MAIN #####

# Parsing the input file containing the Sudoku grid
fd    = open(args.sudoku_file)
lines = fd.read().splitlines()
fd.close()

grid = [[] for i in range(args.N)]

for i in range(args.N):
   grid[i] = [val for val in lines[i].replace(".", " ")]

# Print the grid in a LaTeX tabular
print_latex_grid(grid)
