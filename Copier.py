import json
import os, shutil, stat

class Copier():
    def __init__(self):
        # read rule json
        rules = json.load(open("Rules.json"))

        # build dict tree
        self.dictTree = Node()
        for rule in rules:
            self._generateRule(rule)
        # self._printDictTree(self.dictTree)

    def copy(self, filePath):
        # check dict tree
        # replace is used for different platform
        relPath = os.path.relpath(filePath).replace("\\", "/")
        cur = self.dictTree
        copiedFiles = []
        length = 0
        for directory in relPath.split("/"):
            if directory in cur.children:
                cur = cur.children[directory]
                length += len(directory) + 1
            else:
                if cur.dst:
                    # force copy
                    # print(relPath, cur.dst)
                    remainPath = relPath[length:]
                    for dst in cur.dst:
                        dstPath = os.path.join(dst, os.path.normpath(remainPath))
                        try:
                            shutil.copyfile(relPath, dstPath)
                        except IOError as e:
                            dirName = os.path.dirname(dstPath)
                            if not os.path.exists(dirName):
                                os.makedirs(dirName)
                            try:
                                shutil.copyfile(relPath, dstPath)
                            except IOError as e:
                                os.chmod(dstPath, stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
                                shutil.copyfile(relPath, dstPath)
                        copiedFiles.append("Copy " + filePath + "\n to " + os.path.abspath(dstPath).replace("\\", "/"))
                break
        # return copied files
        return copiedFiles

    def _generateRule(self, rule):
        if rule["src"].startswith("/"):
            return
        cur = self.dictTree
        # print(os.path.normpath(rule["src"]))
        directories = os.path.normpath(rule["src"]).replace("\\", "/").split("/")
        for directory in directories:
            if directory:
                if directory not in cur.children:
                    cur.children[directory] = Node(directory)
                cur = cur.children[directory]
                if directory is directories[-1]:
                    cur.dst = rule["dst"]

    def _printDictTree(self, node):
        print("dir: " + str(node.directory))
        if node.dst:
            print("dst: " + str(node.dst))
        for key in node.children:
            self._printDictTree(node.children[key])

class Node():
    def __init__(self, directory = ".", dst = None):
        self.directory = directory
        self.dst = dst
        self.children = {}
