#!/usr/bin/python

import os
import sqlite3
from DOTElement import *


class DBHelper():

    qCreateNodeT = (
            """
            CREATE TABLE IF NOT EXISTS
            node(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name,pid,tid,ts)
            """
            )
    qInsertNode = (
            """
            INSERT INTO
            node(name,pid,tid,ts)
            VALUES(?, ?, ?, ?)
            """
            )

    qCreateEdgeT = (
            """
            CREATE TABLE IF NOT EXISTS
            edge(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caller_name,callee_name,calling)
            """
            )

    qInsertEdge = (
            """
            INSERT INTO
            edge(
            caller_name,callee_name,calling)
            VALUES(?, ?, ?)
            """
            )

    qFindEdge = (
            """
            SELECT * FROM edge
            where caller_name = ? and callee_name = ?
            """
            )
    # UPDATE edge SET calling = calling+1
    # where caller_name = "test" and callee_name = "test1"
    qCalledEdge = (
            """
            UPDATE edge SET calling = calling + 1
            where caller_name = ? and callee_name = ?
            """
            )


    def __init__(self, path):
        if os.path.isfile(path):
            os.rename(path, "backup_" + path)

        self.db = sqlite3.connect(path)
        self.c = self.db.cursor()
        self.CreateNodeTable()
        self.CreateEdgeTable()

    # C methods
    def CreateNodeTable(self):
        self.c.execute(DBHelper.qCreateNodeT)

    def CreateEdgeTable(self):
        self.c.execute(DBHelper.qCreateEdgeT)

    # U methods
    def InsertNode(self, node):
        self.c.execute(DBHelper.qInsertNode, tuple(node.ToList()))
        pass

    def InsertEdge(self, edge):
        self.c.execute(DBHelper.qInsertEdge, tuple(edge.ToList()))

    # R methods
    def GetAllNode(self):
        return self.c.execute("SELECT * FROM node")

    def GetAllEdge(self):
        return self.c.execute("SELECT * FROM edge")

    def GetNodeByName(self, name):
        pass

    def GetEdgeByName(self, name):
        pass

    def FindEdge(self, caller_name, callee_name):
        rows = self.c.execute(
                DBHelper.qFindEdge, tuple([caller_name, callee_name])
                )

        return rows

    # Etc...
    def doQuery(query):
        return self.c.execute(query)

    def SQLite3(filename):
        from os.path import isfile, getsize
        if not isfile(filename):
            return False

        # SQLite database file header is 100 bytes
        if getsize(filename) < 100:             
            return False

        with open(filename, 'rb') as fd:
            header = fd.read(100)

        return header[:16] == 'SQLite format 3\x00'
