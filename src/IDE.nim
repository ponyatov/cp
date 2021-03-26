import config
import metainfo

import syntax/generic
import parser

assert parse("") == "nil"

when isMainModule:
  echo(generic())

# https://github.com/StefanSalewski/NimProgrammingBook/blob/master/nimprogramming.adoc

var sum: int = 0x1234
assert sum == 4660
echo sum
inc sum, 1
echo sum
inc sum, 11
echo sum
let n = 1
while sum < 7777:
  inc sum, 1
  # n += 1
echo sum
