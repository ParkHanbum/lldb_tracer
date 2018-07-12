#!/usr/bin/python

import zlib

class Node():

    NodeArg = 'args'
    NodeName = 'name'
    NodeType = 'ph'
    NodeTid = 'tid'
    NodePid = 'pid'
    NodeCaller = 'caller'

    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.calling = 0

    def Called(self):
        self.calling += 1

    def GetName(self):
        return self.name

    def GetCallCount(self):
        return self.calling

    def GetColor(self):
        name = self.GetName()
        return hex(zlib.crc32(name) & 0xffffffff)[2:]

    def ToDotLabel(self):
        label = (('\t"{name}"'
            '[label="{label}'
            '\\ncalls: {callcount}"'
            ', color="#{color}"]\n')
                .format(name=self.name, 
                    label=self.name, 
                    callcount=self.GetCallCount(),
                    color=self.GetColor() 
                    )
                )

        return label

    def ToStr(self):
        result = ("{name}, {pid}, {tid}, {ts}".format(
            name = self.name,
            pid = self.pid,
            tid = self.tid,
            ts = self.ts
            ))
        return result

    def ToList(self):
        result = []
        result.append(self.name)
        result.append(self.pid)
        result.append(self.tid)
        result.append(self.ts)

        return result

class Edge():

    def __init__(self, caller, callee):
        self.caller = caller
        self.callee = callee
        self.calling = 1

    def Called(self):
        self.calling += 1

    def GetCallCount(self):
        return self.calling

    def GetColor(self):
        pass

    def GetCallerName(self):
        return self.caller.GetName()

    def GetCalleeName(self):
        return self.callee.GetName()

    def ToDotLabel(self):
        label = ('\t"{caller_name}"->"{callee_name}"[xlabel="{label}"]\n'
        .format(caller_name=self.caller.GetName(),
                callee_name=self.callee.GetName(),
                label=self.GetCallCount()
                ))
        return label

    def ToStr(self):
        result = ("{caller_name}, {callee_name}"
                .format(caller_name = self.caller.GetName(),
                    callee_name = self.callee.GetName())
                )
        return result

    def ToList(self):
        result = []
        result.append(self.caller.GetName())
        result.append(self.callee.GetName())
        result.append(self.GetCallCount())
        return result

