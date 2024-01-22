import argparse
import os
import sys
import shutil
import hashlib
import time

def controlArguments():
    global pathSource, pathReplica, fileToLog, interval
    parser = argparse.ArgumentParser(description="Synchronize two folders and log actions")
    parser.add_argument("source", type=str, help="Path to source folder")
    parser.add_argument("replica", type=str, help="Path to replica folder")
    parser.add_argument("interval", type=int, help="Interval in seconds (10-60)")
    parser.add_argument("logFile", type=str, help="Path to log file")

    args = parser.parse_args()

    # Verify if source and replica paths exist
    if not os.path.isdir(args.source):
        sys.exit(f"Error: The source folder '{args.source}' does not exist.")
    if not os.path.isdir(args.replica):
        sys.exit(f"Error: The replica folder'{args.replica}' does not exist.")
    if args.interval < 10 or args.interval > 60:
        sys.exit(f"Error: interval must be between 10 and 60.")
    pathSource = args.source
    pathReplica = args.replica
    interval = args.interval
    fileToLog = open(args.logFile, "w")

def readFoldersContent():
    global pathSource, pathReplica, pathSourceContent, pathReplicaContent
    pathSourceContent = readFolderContent(pathSource, pathSource)
    pathReplicaContent = readFolderContent(pathReplica, pathReplica)
    
def readFolderContent(rootPath, path, folders=None, files=None):
    if folders is None:
        folders = []
    if files is None:
        files = []
    content = os.listdir(path)
    for item in content:
        full_item_path = os.path.join(path, item)
        relative_item_path = getRelativePath(rootPath, full_item_path)
        if os.path.isdir(full_item_path):
            folders.append(relative_item_path)
            readFolderContent(rootPath, full_item_path, folders, files)
        elif os.path.isfile(full_item_path):
            files.append(relative_item_path)
    return {"folders": folders, "files": files}

def getRelativePath(rootPath, path):
    return path.replace(rootPath, '')

def createFoldersIfNoExistsInReplicaFromSorurce():    
    global pathSourceContent, pathReplicaContent, pathReplica
    for folder in pathSourceContent["folders"]:
        if folder not in pathReplicaContent["folders"]:
            os.makedirs(pathReplica + folder)
            log(f"Create folder from source: {pathSource}{folder} to replica: {pathReplica}{folder}")

def removeFoldersIfNoExistInSourceFromReplica():
    global pathSourceContent, pathReplicaContent, pathReplica
    for folder in pathReplicaContent["folders"]:
        if folder not in pathSourceContent["folders"]:
            try:
                shutil.rmtree(pathReplica + folder)
                log(f"Remove folder from replica: {pathReplica}{folder}")
            except Exception:
                pass

def copyFilesIfNoExistsInReplicaFromSorurce():
    global pathSourceContent, pathReplicaContent, pathReplica, pathSource
    for file in pathSourceContent["files"]:
        if file not in pathReplicaContent["files"]:
            shutil.copyfile(pathSource + file, pathReplica + file)
            log(f"Copy file from source: {pathSource}{file} to replica: {pathReplica}{file}")

def removeFilesIfNoExistsInSourceFromReplica():
    global pathSourceContent, pathReplicaContent, pathReplica, pathSource
    for file in pathReplicaContent["files"]:
        if file not in pathSourceContent["files"]:
            try:
                os.remove(pathReplica + file)
                log(f"Remove file from replica: {pathReplica}{file}")
            except Exception:
                pass

def copyFilesIfContentIsDiferentInReplicaFromSorurce():
    for file in pathReplicaContent["files"]:
        try:
            if (calcular_md5(pathSource + file) != calcular_md5(pathReplica + file)):
                shutil.copyfile(pathSource + file, pathReplica + file)
                log(f"Copy content file from source: {pathSource}{file} to replica: {pathReplica}{file}")
        except Exception:
            pass

def calcular_md5(path_file):
    hash_md5 = hashlib.md5()
    with open(path_file, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_md5.update(bloque)
        f.flush()
    return hash_md5.hexdigest()

def log(text):
    global fileToLog
    print(text)
    fileToLog.write(f"{text}\n")
    fileToLog.flush()

if __name__ == "__main__":
    pathSource = ""
    pathReplica = ""
    fileToLog = None
    pathSourceContent = {"folders": [], "files": []}
    pathReplicaContent = {"folders": [], "files": []}
    interval = None
    numberOfExecution = 0
    controlArguments()
    while True:
        numberOfExecution += 1
        print(f"Execution number: {numberOfExecution}" + str())
        readFoldersContent()
        createFoldersIfNoExistsInReplicaFromSorurce()
        removeFoldersIfNoExistInSourceFromReplica()
        copyFilesIfNoExistsInReplicaFromSorurce()
        removeFilesIfNoExistsInSourceFromReplica()
        copyFilesIfContentIsDiferentInReplicaFromSorurce()
        time.sleep(interval)    