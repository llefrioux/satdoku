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
def encode_dimacs_var(i, j, k):
   return (i * args.N + j) * args.N + k

# Print dimacs header
def print_dimacs_header(n_vars, n_cls):
   print(f"p cnf {n_vars} {n_cls}")

# Print dimacs comment
def print_dimacs_comment(comment):
   print(f"c {comment}")

# Print a clause given as a list of literals
def print_dimacs_cls(cls):
   print(*cls + [0])


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
n_cls += args.N ** 2 * args.N * (args.N - 1) // 2
n_cls += args.N ** 2 * args.N * (args.N - 1) // 2
n_cls += args.N ** 2 * args.N * (args.N - 1) // 2
n_cls += n_assumptions

print_dimacs_header(n_vars, n_cls)

# Generate clauses forcing at least one digit per square
print_dimacs_comment("Forcing at least one digit per square.")
for i in range(args.N):
   for j in range(args.N):
      cls = []
      for k in range(1, args.N + 1):
         cls += [encode_dimacs_var(i, j, k)]
      print_dimacs_cls(cls)


# Generate clauses forcing a digit not to be twice on a line
print_dimacs_comment("Forcing a digit not to be twice on a line.")
for i in range(args.N):
   for k in range(1, args.N + 1):
      for j1 in range(args.N):
         for j2 in range(j1 + 1, args.N):
            cls = [-encode_dimacs_var(i, j1, k), -encode_dimacs_var(i, j2, k)]
            print_dimacs_cls(cls)


# Generate clauses forcing a digit not to be twice on a column
print_dimacs_comment("Forcing a digit not to be twice on a column.")
for j in range(args.N):
   for k in range(1, args.N + 1):
      for i1 in range(args.N):
         for i2 in range(i1 + 1, args.N):
            cls = [-encode_dimacs_var(i1, j, k), -encode_dimacs_var(i2, j, k)]
            print_dimacs_cls(cls)


# Generate clauses forcing a digit not to be twice in a region
print_dimacs_comment("Forcing a digit not to be twice on a region.")
region_size = int(math.sqrt(args.N))
for I in range(region_size):
   for J in range(region_size):
      for k in range(1, args.N + 1):
         for i in range(I * region_size, (I + 1) * region_size):
            for j in range(J * region_size, (J + 1) * region_size):
               for j1 in range(j + 1, (J + 1) * region_size):
                  for i1 in range(I * region_size, (I + 1) * region_size):
                     cls = [-encode_dimacs_var(i, j, k), -encode_dimacs_var(i1, j1, k)]
                     print_dimacs_cls(cls)
               for i1 in range(i + 1, (I + 1) * region_size):
                  cls = [-encode_dimacs_var(i, j, k), -encode_dimacs_var(i1, j, k)]
                  print_dimacs_cls(cls)


# Generate clauses forcing the respect of given assumptions
print_dimacs_comment("Forcing the respect of given assumptions")
for i in range(args.N):
   for j in range(args.N):
      k = grid[i][j]

      if k == VALUES["."]:
         continue

      unit_cls = [encode_dimacs_var(i, j, k)]
      print_dimacs_cls(unit_cls)
