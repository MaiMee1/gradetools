import difflib
import pathlib
import typing

import utils.models


def check_diff(f1_: pathlib.Path, f2_: pathlib.Path, verbose: bool = True):
    differ = difflib.Differ()
    d = {
        '+': 0,
        '-': 0,
        ' ': 0,
        '?': 0,
    }
    f1 = f1_.open(encoding='utf-8')
    f2 = f2_.open(encoding='utf-8')

    for line in differ.compare(
            f1.read().splitlines(), f2.read().splitlines()
    ):
        if verbose:
            print(line)
        d[line[0]] += 1

    f1 = f1_.open('r', encoding='utf-8')
    f2 = f2_.open('r', encoding='utf-8')
    return d, difflib.SequenceMatcher(a=f1.read(), b=f2.read()).ratio()


def func(combinations: typing.Iterable[typing.Tuple[utils.models.Student, utils.models.Student]],
         pathfunc: typing.Callable[[utils.models.Student], pathlib.Path],
         record_file: typing.IO,
         cutoff: float = -1):
    codes = []
    max_sim = {}
    for s1, s2 in combinations:
        try:
            d, r = check_diff(pathfunc(s1), pathfunc(s2), False)
            if r > cutoff:
                for code in codes:
                    if s1 in code:
                        code.add(s2)
                        break
                else:
                    codes.append({s1, s2})
                print(s1, s2, end=' ')
                print(d, round(r, 2))
                record_file.write(f'{s1} {s2} {d} {round(r, 2)}\n')
                if s1 in max_sim:
                    if max_sim[s1][1] < r:
                        max_sim[s1][0] = s2
                        max_sim[s1][1] = r
                else:
                    max_sim[s1] = [s2, r]
                if s2 in max_sim:
                    if max_sim[s2][1] < r:
                        max_sim[s2][0] = s1
                        max_sim[s2][1] = r
                else:
                    max_sim[s2] = [s1, r]
        except FileNotFoundError as e:
            print(e)
            pass
    print()
    record_file.write('\n')
    for code in codes:
        print([s for s in code])
        record_file.write(f'{[s for s in code]}\n')
    print()
    record_file.write('\n')
    for s1, v in max_sim.items():
        s2, r = v
        print(s1, s2, f'{r:.2f}')
        record_file.write(f'{s1} {s2} {round(r, 2)}\n')
    record_file.close()


if __name__ == '__main__':
    pass
