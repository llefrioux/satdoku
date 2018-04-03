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

parser = argparse.ArgumentParser(description="Sudoku (sdk) to CNF (dimacs)")

parser.add_argument(dest="sudoku_file", metavar="<sudoku_file>",
                    help="file containing the sudoku grid")

parser.add_argument("-s", dest="N", metavar="<sudoku_size>", default=9,
                    type=int, help="size of the sudoku grid, default is 9")

args = parser.parse_args()


##### Functions #####

# Return a unique value for variables based on the input triple (i, j, k)
def var_encoding(i, j, k):
   return (i * args.N + j) * args.N + k


# Print a clause given as a list of literals
def print_cls(cls):
   cls += [0]
   print(*cls)


##### MAIN #####

# Init the values
VALUES = {}
VALUES["."] = -1

if args.N == 16:
   for val in range(10):
      VALUES[str(val)] = val + 1
   VALUES["A"] = 11
   VALUES["B"] = 12
   VALUES["C"] = 13
   VALUES["D"] = 14
   VALUES["E"] = 15
   VALUES["F"] = 16
else:
   for val in range(1, args.N + 1):
      VALUES[str(val)] = val


# Parsing the input file containing the Sudoku grid
fd    = open(args.sudoku_file)
lines = fd.read().splitlines()
fd.close()

grid = [[] for i in range(args.N)]

for i in range(args.N):
   grid[i] = [VALUES[key] for key in lines[i]]

n_assumptions = 0

for i in range(args.N):
   for j in range(args.N):
      if grid[i][j] != VALUES["."]:
         n_assumptions += 1


# Print the header of the DIMACS file
n_vars = args.N ** 3

n_cls  = args.N ** 2
n_cls += int((args.N ** 2) * ((args.N * (args.N - 1)) / 2))
n_cls += int((args.N ** 2) * ((args.N * (args.N - 1)) / 2))
n_cls += int((args.N ** 2) * ((args.N * (args.N - 1)) / 2))
n_cls += n_assumptions

print("p cnf", n_vars, n_cls)


# Generate clauses forcing at least one digit per square
for i in range(args.N):
   for j in range(args.N):
      cls = []
      for k in range(1, args.N + 1):
         cls += [var_encoding(i, j, k)]
      print_cls(cls)


# Generate clauses forcing a digit not to be twice on a line
for i in range(args.N):
   for k in range(1, args.N + 1):
      for j1 in range(args.N):
         for j2 in range(j1 + 1, args.N):
            cls = [-var_encoding(i, j1, k), - var_encoding(i, j2, k)]
            print_cls(cls)


# Generate clauses forcing a digit not to be twice on a column
for j in range(args.N):
   for k in range(1, args.N + 1):
      for i1 in range(args.N):
         for i2 in range(i1 + 1, args.N):
            cls = [-var_encoding(i1, j, k), - var_encoding(i2, j, k)]
            print_cls(cls)


# Generate clauses forcing a digit not to be twice in a region
region_size = int(math.sqrt(args.N))
for I in range(region_size):
   for J in range(region_size):
      for k in range(1, args.N + 1):
         for i in range(I * region_size, (I + 1) * region_size):
            for j in range(J * region_size, (J + 1) * region_size):
               for j1 in range(j + 1, (J + 1) * region_size):
                  for i1 in range(I * region_size, (I + 1) * region_size):
                     cls = [-var_encoding(i, j, k), -var_encoding(i1, j1, k)]
                     print_cls(cls)
               for i1 in range(i + 1, (I + 1) * region_size):
                  cls = [-var_encoding(i, j, k), -var_encoding(i1, j, k)]
                  print_cls(cls)


# Generate clauses forcing the respect of the given assumptions
for i in range(args.N):
   for j in range(args.N):
      k = grid[i][j]

      if k == VALUES["."]:
         continue

      unit_cls = [var_encoding(i, j, k)]
      print_cls(unit_cls)
