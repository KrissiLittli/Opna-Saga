# Prófa og bæta verkfærið á Linux

XYZ-prófun Opna-Saga er lítið Python-verkfæri sem má sannreyna með tilbúnum
gögnum. Það krefst Python 3.10 eða nýrra og notar aðeins staðalsafnið.

## Keyrsla úr rót safnsins

```sh
python3 --version
python3 -m unittest discover -s tests -v
python3 tools/check_xyz.py examples/valid.xyz
python3 tools/check_xyz.py examples/invalid.xyz
```

Gilda dæmið skilar `'valid.xyz': OK — 3 points` og útgöngukóða `0`.
Ógilda dæmið skilar `'invalid.xyz':3: coordinates must be finite` og kóða `1`.
Það er ætlað mótdæmi. Kóði `2` merkir notkunar-, skráaraðgangs- eða
UTF-8-villu. Verkfærið les inntakið án þess að breyta því.

## Sannreynd Linux keyrsla

Prófað 5. nóvember 2026 með opinberum skrám frá
[commit 04d94b3](https://github.com/KrissiLittli/Opna-Saga/commit/04d94b34aef68bfa66eb7d4527d00dc7df086421).

| Atriði | Raunverulegt prófumhverfi |
| --- | --- |
| Stýrikerfi | Ubuntu 24.04.3 LTS í Linux-vinnuumhverfi |
| Kjarni | 6.18.57 |
| Vélargerð | x86_64 |
| Python | CPython 3.12.14 |
| Sjálfvirk próf | 9 af 9 stóðust |
| Gilt XYZ-dæmi | 3 punktar og útgöngukóði 0 |
| Ógilt XYZ-dæmi | Höfnun á línu 3 og útgöngukóði 1 |

Þessi niðurstaða nær til skipanalínuverkfærisins og prófanna í töflunni.
Hún staðfestir ekki mælinákvæmni, hnitakerfi eða ytri mæligögn.

## Skila endurgeranlegri villu og lagfæringu

Opnaðu villumál í þessu safni með commit-auðkenni, Python-útgáfu, Linux-dreifingu,
nákvæmri skipun, útgöngukóða og því sem þú bjóst við að gerðist. Bættu við
eins lítilli tilbúinni XYZ-skrá og þarf til að sýna vandann. Þannig getur annar
aðili endurtekið keyrsluna án aðgangs að þínum gögnum.

Prófaðu fyrst [núverandi dæmi](../../examples/valid.xyz). Ef villan kemur aðeins
fram með þínu inntaki skaltu minnka það í fáar tilbúnar línur sem endurskapa
sama hegðun. Skráðu nákvæmlega hvað þessi prófun sýnir.

Settu lagfæringu í sér grein og bættu við prófi í
[tests/test_check_xyz.py](../../tests/test_check_xyz.py) sem sýnir vandann áður
en lagfæringin er sett inn. Keyrðu prófaskipunina aftur og lýstu breytingu og
niðurstöðu í pull request. Haltu prófinu svo sama villa greinist við síðari
breytingar.

Kóðinn og þessi leiðbeining fylgja [MIT-leyfi safnsins](../../LICENSE).
Varðveittu leyfistexta og upprunamerkingar þegar þú dreifir kóðanum áfram.
Ef framlag nýtir kóða úr öðru verkefni fylgja skilmálar og tilgreiningar þess
verkefnis með framlaginu.
