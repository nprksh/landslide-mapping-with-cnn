import os
import yaml
import glob
import shutil

def removeFile(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
        print(fileName + ' removed.')


def emptyDirectory(dirPath, ext = "*", verbose = True):
    allFiles = glob.glob(dirPath + "/" + ext)
    if verbose:
        print(str(len(allFiles)) + " files found in " + dirPath + " --> Will be deleted.")
    for f in allFiles:
        try:
            os.remove(f)
        except:
            shutil.rmtree(f)


def createDirectory(dirPath, emptyExistingFiles = False, verbose = True):
    if not os.path.isdir(dirPath):
        os.makedirs(dirPath)
        if verbose:
            print("Folder not found!!!   " + dirPath + " created.")
    else:
        print('%s --> Folder exists!!!'%dirPath)
        if emptyExistingFiles:
            emptyDirectory(dirPath, verbose = verbose)

