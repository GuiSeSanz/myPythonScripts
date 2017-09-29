import os
import time
import shutil
import multiprocessing
from datetime import datetime


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

class ScriptFile(object):
    __metaclass__ = IterRegistry
    _registry = []
    def __init__(self, user, path):
        self.user = str(user)
        self.path = str(path)
        self.fileName = os.path.basename(path)
    def getPath(self):
        return self.path
    def getUser(self):
        return self.user
    def getFileName(self):
        return self.fileName
    def printScriptFile(self):
        print('User: {0} \t File: {1}'.format(self.user, self.fileName))


def checkAndDeleteOldFolder(outFolder):
    now = time.time()
    daysToKeep = 5
    fiveDaysAgo = now - 60*60*24*daysToKeep # Number of seconds in five days
    cmd = "find {0} -maxdepth 1 | grep '.*\.zip'".format(outFolder)
    files = os.popen(cmd).read().split()
    if not files:
        return
    else:
        for fl in files:
            fileCreation = os.path.getctime(fl)
            if fileCreation < fiveDaysAgo:
                print "File deleted {0}".format(fl)
                os.remove(fl)
            else:
                print('Checked {0}'.format(fl))

def getFiles(user):
    # cmd = "find /home/bioinformatica/datos/03_Analysis/{0}/ -type f -print | grep '.*\.{1}$'".format(users[0], ext[0])
    fileList = []
    for ext in extensions:
        print('Searching for .{0} files in {1} user'.format(ext, user))
        cmd = "find /run/user/1000/gvfs/smb-share:server=valis.si.unav.es,share=calculus/03_Analysis/{0}/ -type f -print | grep '.*\.{1}$'".format(user, ext)
        # cmd = "find /home/guille/Desktop/tmp/ -type f -print | grep '.*\.txt$'"
        files = os.popen(cmd).read().split()
        for fl in files:
            if '._'not in fl:
                fileList.append(ScriptFile(user, fl))
    return fileList

def createDailyFolder(outFolder):
    dailyFolder = os.path.join(outFolder, 'Backup' + datetime.now().strftime('%d-%m-%Y'))
    try:
        os.mkdir(dailyFolder)
    except OSError:
        print('The folder {0} already exists, writting inside...'.format(dailyFolder))
    return dailyFolder

def createUserFiles(outPath, users):
    userNames = set(users)
    for user in userNames:
        try:
            os.mkdir(os.path.join(outPath, user))
        except OSError:
            print('The folder  for the user {0} already exists, writting inside...'.format(user))

def copyFiles(outPath, files):
    for fl in files:
        dst =os.path.join(outPath, str(fl.getUser()), str(fl.getFileName()))
        shutil.copyfile(fl.getPath(), dst)

def  compressFiles(dir_name):
    shutil.make_archive(dir_name, 'zip', dir_name)

def makeBackUp(user):
    copyFiles(outPath,getFiles(user))

def copyAllScriptsAndTree(folders, outPath):
    root = '/home/bioinformatica/datos/'
    for folder in folders:
        folderPath = os.path.join(root, folder)
        print('Copying the folder {0}'.format(folderPath))
        shutil.copytree(folderPath, outPath)

if __name__ == '__main__':
    users = ['gserranos']
    folders  = ['01_Rscripts', '02_Cluster_Sripts']
    extensions = ['R', 'py', 'jar', 'sh']
    outFolder = '/tmp/'
    checkAndDeleteOldFolder(outFolder)
    outPath = createDailyFolder(outFolder)
    createUserFiles(outPath, users)
    pool = multiprocessing.Pool(processes=len(users))
    # for user in users:
    #     copyFiles(outPath,getFiles(user))
    pool.map(makeBackUp, users)
    compressFiles(outPath)
    shutil.rmtree(outPath)
