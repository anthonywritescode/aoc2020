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
```
