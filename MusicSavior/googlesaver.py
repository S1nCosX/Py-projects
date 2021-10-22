from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

import mimetypes
import os
import re

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

print('input target folder name')
targetFolder = input()

path = re.search(r'[\w\W]+\\(MusicSavior){0}', os.path.abspath(os.curdir)).group()

LocalFiles = []

for i in os.listdir(path):
    LocalFiles.append(i)

FilesInCloud = drive.ListFile().GetList()

NamesOfFilesInCloud = []
Undownloaded = []
Unuploaded = []

dirId = ''

# ищем не скачаные
for CloudFile in FilesInCloud:
    if CloudFile['title'] == targetFolder:
        dirId = CloudFile['id']
    NamesOfFilesInCloud.append(CloudFile['title'])

if dirId == '':
    newFolder = drive.CreateFile({'title': targetFolder, 'parents': [], 'mimeType': 'application/vnd.google-apps.folder'})
    newFolder.Upload()
    dirId = newFolder['id']

for CloudFile in FilesInCloud:
    Num = 0
    try:
        for i in range(len(CloudFile['parents'])):
            if CloudFile['parents'][i]['id'] == dirId:
                Num = i
    except:
        print('aboba')
    if len(CloudFile['parents']) > 0 and CloudFile['parents'][Num]['id'] == dirId:
        try:
            LocalFiles.index(CloudFile['title'])
        except:
            Undownloaded.append(CloudFile)

# ищем не загрушенные на облако
for LocalFile in LocalFiles:
    try:
        if LocalFile != 'MusicSavior':
            NamesOfFilesInCloud.index(LocalFile)
    except:
        Unuploaded.append(LocalFile)

#заполняем пробелы в обеих частях
#заливаем
for i in range(len(Unuploaded)):
    print('Progress', i, '/', len(Unuploaded))
    LocalFile = Unuploaded[i]
    LocalFileMime, LocalFileEncoding = mimetypes.guess_type(path + LocalFile)
    print(LocalFile, LocalFileMime)
    try:
        file = drive.CreateFile({'title': LocalFile, 'mimeType': LocalFileMime, 'parents': [{'id': dirId}]})
        file.Upload()
        file.SetContentFile(path + LocalFile)
        file.Upload()
        print("file ", file['title'], " uploaded\n")
    except:
        print("3ajlyna he pa6otaet\n")
if len(Unuploaded) > 0:
    print("Uploading ends")

#скачиваем
for i in range(len(Undownloaded)):
    print('Progress', i, '/', len(Undownloaded))
    CloudFile = Undownloaded[i]
    try:
        file = drive.CreateFile({'id': CloudFile['id']})
        file.GetContentFile(path + CloudFile['title'])
        print("file ", file['title'], " downloaded\n")
    except:
        print("3ajlyna he pa6otaet\n")
if len(Undownloaded) > 0:
    print("Downloading ends")

print('Sync Ends')

input()