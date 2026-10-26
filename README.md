# Opna-Saga

Small, independent open-source tools from Okkar-Saga. Each tool has a narrow
purpose, synthetic examples, and tests. This repository starts with one tool.

## XYZ coordinate check

`check_xyz.py` reads a UTF-8 text file and checks that every data row contains
exactly three finite numbers. It rejects `NaN`, infinity, missing or extra
coordinates, invalid text, and files without points. Blank lines, `#` comments,
and inline `#` comments are allowed.

Requires Python 3.10 or later. No packages, network connection, API key, or
model are needed. The input file is opened for reading only.

```sh
python3 tools/check_xyz.py examples/valid.xyz
```

Expected result: `'valid.xyz': OK — 3 points` and exit code `0`.

```sh
python3 tools/check_xyz.py examples/invalid.xyz
```

The invalid example is deliberately rejected with a line number and exit code
`1`. Errors show the filename and reason without printing coordinates or parent
directories. Exit code `2` means a command-line, file-access, or UTF-8 error.

| Exit code | Meaning |
| --- | --- |
| `0` | All rows passed; at least one point |
| `1` | Invalid coordinate data |
| `2` | Usage, file-access, or encoding error |

This is a structural check. It does not verify a coordinate reference system,
units, geographic bounds, measurement accuracy, or whether a point is true.
It does not parse OBJ, CSV, LAS, raster, or PDF files. Export plain XYZ text
before using it.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

The tests exercise the command-line tool on synthetic files, including rejected
input, exit codes, useful errors, and unchanged source bytes. Local validation
is recorded in [VALIDATION.json](VALIDATION.json).

## Íslenska

Fyrsta verkfærið prófar XYZ-textaskrá: þrjár endanlegar tölur í hverri gagnalínu.
Það finnur meðal annars NaN/inf og rangan hnitafjölda án þess að breyta skránni.
Öll sýnigögn hér eru tilbúin. Staðsetning, hnitakerfi og mælinákvæmni þurfa
sjálfstæða sannprófun.

## Contributing

Keep changes small and focused. Include a synthetic example or a test that
demonstrates the problem, run the test command above, and open a pull request.
Use only data and code you have permission to share. Never include credentials
or private research files. Project archives and conversations are outside this
repository's scope.

## License and origin

The original code, documentation, tests, and synthetic examples in this
repository are licensed under [MIT](LICENSE). This starts a fresh history with
an explicit file list; it contains no imported research archive, model weights,
or prior repository history. The license applies to this repository's files.
