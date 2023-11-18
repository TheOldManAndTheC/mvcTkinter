# Copyright (c) 2023 The Old Man and the C
#
# This file is part of mvcTkinter.
#
# mvcTkinter is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# mvcTkinter is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with mvcTkinter. If not, see <https://www.gnu.org/licenses/>.

# Methods for file I/O operations
import csv
import json
import os
import sys
import shutil
import subprocess
import shlex
from warnings import warn

validOpenArgs = ["file", "mode", "buffering", "encoding", "errors", "newline",
                 "closefd", "opener"]
validJSONLoadsArgs = ["cls", "object_hook", "parse_float", "parse_int",
                      "parse_constant", "object_pairs_hook"]
validJSONDumpsArgs = ["obj", "skipkeys", "ensure_ascii", "check_circular",
                      "allow_nan", "cls", "indent", "separators", "default",
                      "sort_keys"]
validCSVArgs = ["csvfile", "dialect", "delimiter", "doublequote", "escapechar",
                "lineterminator", "quotechar", "quoting", "skipinitialspace",
                "strict"]

settings = dict()


# Get a path to a resource from a relative path for both normal source
# and pyinstaller one file installations
def resourcePath(relativePath):
    # pyinstaller one file configuration
    try:
        basePath = sys._MEIPASS
    except AttributeError:
        basePath = currentDir()
    return os.path.join(basePath, relativePath)


# Get the current directory of the application
def currentDir():
    return os.getcwd()


# Check if a path exists and handle None as False
def pathExists(path):
    if path is not None:
        return os.path.exists(path)
    return False


# Create a directory tree
def createDirectory(directory):
    if directory is not None:
        os.makedirs(directory, exist_ok=True)


# Remove a directory tree
def deleteDirectory(directory):
    if directory is not None:
        shutil.rmtree(directory, ignore_errors=True)


# Return the most recently modified file in a directory with optional extension
def latestFile(directory, extension=""):
    if not directory:
        return None
    paths = []
    for entry in os.scandir(directory):
        if entry.is_file() and entry.path.endswith(extension):
            paths.append(entry.path)
    file = max(paths, key=os.path.getctime)
    return file


# Copy a file in the filesystem
def copyFile(source, destination):
    try:
        shutil.copy(source, destination)
    except shutil.SameFileError:
        pass


# Delete a file from the filesystem
def deleteFile(file):
    if pathExists(file):
        os.remove(file)


# Read data from a file
def readFile(file, lines=False, mode="r", encoding="utf8", **kwargs):
    args = {key: kwargs[key] for key in validOpenArgs if key in kwargs}
    if not pathExists(file):
        return None
    with open(file, mode=mode, encoding=encoding, **args) as fileObject:
        if lines:
            data = fileObject.readlines()
        else:
            data = fileObject.read()
    return data


def writeFile(data, file, lines=False, mode="w", encoding="utf8", **kwargs):
    args = {key: kwargs[key] for key in validOpenArgs if key in kwargs}
    with open(file, mode=mode, encoding=encoding, **args) as fileObject:
        if lines:
            fileObject.writelines(data)
        else:
            fileObject.write(data)


# Read a json file
def readJSON(file, **kwargs):
    args = {key: kwargs[key] for key in validJSONLoadsArgs if key in kwargs}
    jsonText = readFile(file, **kwargs)
    if jsonText is None:
        return None
    try:
        data = json.loads(jsonText, **args)
    except json.JSONDecodeError as error:
        warn(str(error), SyntaxWarning)
        return None
    return data


# Write an object to a json file
def writeJSON(obj, file, indent=4, **kwargs):
    args = {key: kwargs[key] for key in validJSONDumpsArgs if key in kwargs}
    writeFile(json.dumps(obj, indent=indent, **args), file, **kwargs)


# Read a CSV spreadsheet into an array of rows, each an array of cells.
# Alternatively, read it into a dictionary keyed by the values in the
# indexRow, containing dictionaries keyed by the values in the header row.
# If there are duplicate values for keys, the keys will be suffixed with
# [<integer>].
def readCSV(file, useDict=False, indexRow=0, **kwargs):
    args = {key: kwargs[key] for key in validCSVArgs if key in kwargs}
    csvData = []
    csvLines = readFile(file, lines=True, **kwargs)
    if csvLines is None:
        return None
    csvReader = csv.reader(csvLines, **args)
    for row in csvReader:
        csvData.append(row)
    if not useDict:
        return csvData
    headers = []
    csvDict = dict()
    for row in csvData:
        if not headers:
            headers = row
        rowID = row[indexRow]
        rowIDsubscript = 0
        while rowID in csvDict:
            rowID = row[indexRow] + "[{}]".format(rowIDsubscript)
            # rowID = row[indexRow] + "[" + str(rowIDsubscript) + "]"
            rowIDsubscript += 1
        rowDict = dict()
        dummyHeader = "unknownHeader"
        dummySubscript = 0
        for index in range(len(row)):
            if index >= len(headers):
                while True:
                    header = dummyHeader + "[{}]".format(dummySubscript)
                    # header = dummyHeader + "[" + str(dummySubscript) + "]"
                    dummySubscript += 1
                    if header not in rowDict:
                        break
            else:
                header = headers[index]
                headerSubscript = 0
                while header in rowDict:
                    header = headers[index] + "[{}]".format(headerSubscript)
                    # header = headers[index] + "[" + str(headerSubscript) + "]"
                    headerSubscript += 1
            rowDict[header] = row[index]
        csvDict[rowID] = rowDict
    return csvDict


# Write a CSV file from the given csvData. If it is a dictionary, only the
# values will be written.
def writeCSV(data, file, mode="w", encoding="utf8", **kwargs):
    openArgs = {key: kwargs[key] for key in validOpenArgs if key in kwargs}
    csvArgs = {key: kwargs[key] for key in validCSVArgs if key in kwargs}
    with open(file, mode=mode, encoding=encoding, **openArgs) as csvFile:
        csvWriter = csv.writer(csvFile, **csvArgs)
        if isinstance(data, dict):
            for row in data.values():
                csvWriter.writerow(row.values())
        else:
            for row in data:
                csvWriter.writerow(row)


# Run a shell command. By default, process output is set to redirect to
# sys.stdout in realtime. This helps ensure any redirection of sys.stdout will
# capture it.
def shellCmd(command, output=True, stdout=subprocess.PIPE,
             stderr=subprocess.STDOUT, text=True, **kwargs):
    # Windows specific flags to prevent shell windows from appearing
    startupInfo = subprocess.STARTUPINFO()
    startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    with (subprocess.Popen(shlex.split(command), stdout=stdout, stderr=stderr,
                          text=text, startupinfo=startupInfo, **kwargs)
          as process):
        outText = ""
        while True:
            if stdout == subprocess.PIPE:
                out = process.stdout.readline()
                if output:
                    sys.stdout.write(out)
                else:
                    outText += out
            else:
                out = ""
            if len(out) == 0 and process.poll() is not None:
                break
        # no way to properly integrate stdout output with stderr in
        # chronological order so just dump  stderr afterward
        if stderr == subprocess.PIPE:
            err = process.stderr.read()
            if output:
                sys.stderr.write(err)
            else:
                outText += err
        return process.returncode, outText


def settingValue(setting):
    global settings
    if setting in settings:
        return settings[setting]
    return None


def setSetting(setting, value, write=True):
    global settings
    if setting is not None:
        if setting in settings and settings[setting] == value:
            write = False
        else:
            settings[setting] = value
    if write:
        writeSettings()


def readSettings(path=None):
    global settings
    if path is None:
        path = currentDir() + "/settings.json"
    settings = readJSON(file=path)
    if not settings:
        settings = dict()
        return False
    return True


def writeSettings(path=None):
    global settings
    if path is None:
        path = currentDir() + "/settings.json"
    writeJSON(obj=settings, file=path)


def importSettings(path, exportKeys):
    global settings
    newSettings = readJSON(file=path)
    for setting in exportKeys:
        if setting in newSettings:
            settings[setting] = newSettings[setting]
    writeSettings()


def exportSettings(path, exportKeys):
    global settings
    newSettings = dict()
    for setting in exportKeys:
        newSettings[setting] = settingValue(setting)
    writeJSON(obj=newSettings, file=path)
