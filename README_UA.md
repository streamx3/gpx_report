# gpx_report

[In English](https://github.com/streamx3/gpx_report/blob/master/README.md)

Ця програма може:
- створювати .GPX файли з папок з фотками
- створювати HTML-звіти з .GPX файлів

#### Залежності:
- ntpath
- xmltodict
- PIL
- ffmpeg

##### Задовільнити залежності під Linux:
```
sudo -i
apt-get install -y python3 python3-pip ffmpeg
^D
```

##### Задовільнити залежності під Mac:
- Скачати Python 3 з офіційного сайту
```
brew install ffmpeg
```

##### Задовільнити залежності під Windows:
- Скачати Python 3 з офіційного сайту
- Скачати ffmpeg з офіційного сайту
- прописати ffmpeg, python3 та pip3 до змінної $PATH

##### Для кожної системи доведеться:
Ввести в консоль:
```
pip3 install ntpath xmltodict pillow
```

### Як зробити GPX з папки з фотками?
Просто:
```
gpx_report -d folder
```

Якщо Ви не прописували прогу в систему:
```
python3 gpx_report.py -d folder
```

Додались нові фотки? Треба переписати .GPX?
```
python3 gpx_report.py -d folder -f
```

в результаті буде створено `folder/folder.gpx`. Можна відкрити його в JOSM або іншому софті.


### Як згенерувати HTML з GPX?
Просто:
```
gpx_report -g folder/folder.gpx
```

Якщо Ви не прописували прогу в систему:
```
python3 gpx_report.py -g folder/folder.gpx
```

в результаті буде створено `folder/index.html`. Відкривайте його браузером.
Зауважте, якщо ваш .GPX файл посилається на аудіо-нотатки в .3gpp, то ці файли будуть конвертовані в .mp3 та додані до веб-сторінки.
