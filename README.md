[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/anthonywritescode/aoc2020/master.svg)](https://results.pre-commit.ci/latest/github/anthonywritescode/aoc2020/master)

advent of code 2020
===================

https://adventofcode.com/2020

### stream / youtube

- [Streamed daily on twitch](https://twitch.tv/anthonywritescode)
- [Uploaded to youtube afterwards](https://www.youtube.com/anthonywritescode)

### about

for 2020, I'm planning to implement in python and then some meme language...
maybe.

### timing

- comparing to these numbers isn't necessarily useful
- normalize your timing to day 1 part 1 and compare
- alternate implementations are listed in parens
- these timings are very non-scientific (sample size 1)

```console
$ find -maxdepth 1 -type d -name 'day*' -not -name day00 | sort | xargs --replace bash -xc 'python {}/part1.py {}/input.txt; python {}/part2.py {}/input.txt'
+ python3 day01/part1.py day01/input.txt
806656
> 115 μs
+ python day01/part2.py day01/input.txt
230608320
> 190 ms
+ python3 day02/part1.py day02/input.txt
517
> 4247 μs
+ python3 day02/part2.py day02/input.txt
284
> 1273 μs
+ python day03/part1.py day03/input.txt
220
> 257 μs
+ python day04/part1.py day04/input.txt
230
> 1326 μs
+ python day04/part2.py day04/input.txt
156
> 2991 μs
+ python day05/part1.py day05/input.txt
980
> 1066 μs
+ python day05/part2.py day05/input.txt
607
> 1014 μs
+ python day06/part1.py day06/input.txt
6768
> 1027 μs
+ python3 day06/part2.py day06/input.txt
3489
> 1910 μs
+ python day07/part1.py day07/input.txt
126
> 4402 μs
+ python day07/part2.py day07/input.txt
220149
> 4189 μs
+ python day08/part1.py day08/input.txt
1528
> 704 μs
+ python3 day08/part2.py day08/input.txt
640
> 8278 μs
+ python3 day09/part1.py day09/input.txt
466456641
> 11640 μs
+ python3 day09/part2.py day09/input.txt
55732936
> 12151 μs
+ python day10/part1.py day10/input.txt
2046
> 127 μs
+ python day10/part2.py day10/input.txt
1157018619904
> 98 μs
+ python3 day11/part1.py day11/input.txt
2166
> 7259 ms
+ python3 day11/part2.py day11/input.txt
1955
> 3586 ms
+ python day12/part1.py day12/input.txt
1294
> 686 μs
+ python day12/part2.py day12/input.txt
20592
> 707 μs
+ python3 day13/part1.py day13/input.txt
2845
> 49 μs
+ python3 day13/part2.py day13/input.txt
487905974205117
> 105 μs (sympy)
487905974205117
> 276 ms (z3)
+ 487905974205117
> 206 μs (loop)
+ python day14/part1.py day14/input.txt
6513443633260
> 1080 μs
+ python day14/part2.py day14/input.txt
3442819875191
> 130 ms
+ python3 day15/part1.py day15/input.txt
206
> 1824 μs
+ python day15/part2.py day15/input.txt
955
> 34311 ms
+ python day16/part1.py day16/input.txt
30869
> 3525 μs
+ python3 day16/part2.py day16/input.txt
4381476149273
> 22986 μs
+ python3 day17/part1.py day17/input.txt
388
> 22131 μs
+ python day17/part2.py day17/input.txt
2280
> 430 ms
+ python day18/part1.py day18/input.txt
3647606140187
> 5725 μs
+ python day18/part2.py day18/input.txt
323802071857594
> 11517 μs
+ python day19/part1.py day19/input.txt
210
> 21139 μs
+ python day19/part2.py day19/input.txt
422
> 17384 μs
+ python day20/part1.py day20/input.txt
64802175715999
> 28779 μs
+ python day20/part2.py day20/input.txt
2146
> 143 ms
+ python day21/part1.py day21/input.txt
2315
> 901 μs
+ python day21/part2.py day21/input.txt
cfzdnz,htxsjf,ttbrlvd,bbbl,lmds,cbmjz,cmbcm,dvnbh
> 795 μs
+ python day22/part1.py day22/input.txt
35562
> 269 μs
+ python day22/part2.py day22/input.txt
34424
> 3996 ms
+ python3 day23/part1.py day23/input.txt
45286397
> 266 μs
+ python3 day23/part2.py day23/input.txt
836763710
> 24217 ms
+ python3 part1.py day24/input.txt
266
> 5621 μs
+ python day24/part2.py day24/input.txt
3627
> 970 ms
+ python day25/part1.py day25/input.txt
1890859
> 675 ms
```
