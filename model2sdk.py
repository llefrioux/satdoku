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
import sys


##### Parsing the arguments #####

parser = argparse.ArgumentParser(description="Model (dimacs) to Sudoku (sdk)")

parser.add_argument(dest="model_file", metavar="<model_file>",
                    help="file containing the ouput of the SAT solver")

parser.add_argument("-s", dest="N", metavar="<sudoku_size>", default=9,
                    type=int, help="size of the sudoku grid, default is 9")

args = parser.parse_args()


##### Functions #####

# Return a unique triple (i, j, k) based on the input number
def var_decoding(x):
   k  = x % args.N
   if k == 0:
      k = args.N
   x -= k
   x += 1
   i  = x // (args.N ** 2)
   j  = (x // args.N) % args.N
   return i, j, k


# Print a sudoku grid in sdk format
def print_sdk_grid(grid):
   for i in range(args.N):
      print(*grid[i], sep="")


##### MAIN #####

# Init the values
VALUES = {}

if args.N == 16:
   for val in range(10):
      VALUES[val + 1] = str(val)
   VALUES[11] = "A"
   VALUES[12] = "B"
   VALUES[13] = "C"
   VALUES[14] = "D"
   VALUES[15] = "E"
   VALUES[16] = "F"
else:
   for val in range(1, args.N + 1):
      VALUES[val] = str(val)

# Parsing the input file containing the enswer of the SAT solver
fd    = open(args.model_file)
lines = fd.read().splitlines()
fd.close()

model = []
for line in lines:
   if line == "s UNSATISFIABLE":
      print("No solution has been found for this grid.", file=sys.stderr)
      exit(0)

   if line[0] != "v":
      continue

   model += [int(i) for i in line[2:].split()]

# Create the Sudoku grid and print it
grid = [["."] * args.N for i in range(args.N)]

for value in model[:-1]:
   if value < 0:
      continue

   i, j, k    = var_decoding(value)
   grid[i][j] = VALUES[k]

print_sdk_grid(grid)
