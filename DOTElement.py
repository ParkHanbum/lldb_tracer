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

    def ToDotLabel(self):
        label = ('\t"{caller_name}"->"{callee_name}"[xlabel="{label}"]\n'
        .format(caller_name=self.caller.GetName(),
                callee_name=self.callee.GetName(),
                label=self.GetCallCount()
                ))
        return label

