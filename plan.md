# Plan

## Features

\### Grade

1. Run `unittest` on files
2. Show individual file  

\### Diff

1. Run diff on files + keep data
2. Show data
3. Show individual file

### Example use

```
$ python -m gradetools grade lab3 "lab3/<id>.py"

grading from "assets\\submissions\\lab3\\<id>.py"
...X...X...X....X.....X.
Graded x files (MISSING=5)
output stored at "temp/lab3.json"
view grades with command `python -m gradetools show grade lab3`
```

```sh
python -m gradetools show grade lab3
5710547221 Warat NARATTHARAKSA | Ran x tests in x.xxxs OK
6010545749 Kannipa PRAYOONPRUK | Ran x tests in x.xxxs OK
...
```

```sh
python -m gradetools show grade lab3 --sort firstname
6210546722 Anas AKHUNKHEL      | Ran x tests in x.xxxs OK
6210546714 Anusid WACHIRACH... | Ran x tests in x.xxxs OK
...
```

```sh
python -m gradetools show grade lab3 --sort lastname
6210546722 Anas AKHUNKHEL      | Ran x tests in x.xxxs OK
6210545980 Pittayut BENJAMA... | Ran x tests in x.xxxs OK
...
```

```sh
python -m gradetools show grade lab3 --detail 6210546722
6210546722 Anas AKHUNKHEL
----------------------------------------------------------------------
Ran 10 tests in x.xxxs
..........
OK
```

```sh
python -m gradetools show grade lab3 --v 0
5710547221 | Ran x tests in x.xxxs OK
6010545749 | Ran x tests in x.xxxs OK
...
```

```sh
python -m gradetools grade elab "code17262/b<id>/a17262.py"
python -m gradetools grade elab 17262
```
