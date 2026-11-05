# Sannprófun með tilbúnum gögnum

Þessi leiðbeining sýnir hvernig má prófa XYZ-gagnaskrá áður en hún er notuð í
korti eða þrívíddarlíkani. Dæmin eru tilbúin og innihalda engar mælingar eða
staðsetningar úr rannsóknarsafni.

| Efni | Slóð |
| --- | --- |
| XYZ-prófun | [tools/check_xyz.py](../../tools/check_xyz.py) |
| Gilt dæmi | [examples/valid.xyz](../../examples/valid.xyz) |
| Ógilt dæmi | [examples/invalid.xyz](../../examples/invalid.xyz) |
| Sjálfvirk próf | [tests/test_check_xyz.py](../../tests/test_check_xyz.py) |
| Leyfi | [MIT](../../LICENSE) |

## Keyra prófun

Keyrðu skipanirnar í rót Opna-Saga með Python 3.10 eða nýrra. Engir pakkar,
aðgangslyklar eða nettenging eru nauðsynleg við keyrslu.

```sh
python3 tools/check_xyz.py examples/valid.xyz
python3 -m unittest discover -s tests -v
```

Fyrri skipunin skilar `'valid.xyz': OK — 3 points`. Seinni skipunin keyrir
prófasafnið. Við yfirferð 5. nóvember 2026 stóðust öll níu prófin á
[útgáfu 04d94b3](https://github.com/KrissiLittli/Opna-Saga/commit/04d94b34aef68bfa66eb7d4527d00dc7df086421).

## Búa til eigið mótdæmi

Þessi skipun býr til nýja skrá í vinnumöppunni:

```sh
printf '1 2 NaN\n' > synthetic-invalid.xyz
python3 tools/check_xyz.py synthetic-invalid.xyz
```

Verkfærið hafnar línunni og skilar útgöngukóða `1`. Það les skrána án þess að
breyta henni. Endurtaktu með `1 2 3` til að fá gilt gagnapunktadæmi.

| Útgöngukóði | Merking |
| --- | --- |
| `0` | Að minnsta kosti einn punktur og þrjár endanlegar tölur í hverri gagnalínu |
| `1` | Gögn standast ekki byggingarprófun |
| `2` | Notkunarvilla, skráaraðgangur eða UTF-8-afkóðun |

## Hvað niðurstaðan segir

Gild skrá hefur rétta talnabyggingu fyrir þetta verkfæri. Hnitakerfi, mælieiningar,
staðsetning og mælinákvæmni þurfa eigin heimild og sannprófun áður en punktar
eru túlkaðir sem raunverulegar mælingar. Skráðu þær upplýsingar með gögnunum
þegar þú undirbýrð þau fyrir kort eða líkan.

Þessi nýja leiðbeining fylgir [MIT-leyfi Opna-Saga](../../LICENSE).
