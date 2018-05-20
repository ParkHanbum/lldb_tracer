#!/usr/bin/python

import lldb
import commands
import optparse
import shlex
import threading
import time
import sys
from lldbutil import *

def target(debugger, commnad, result, internal_dict):
    target = debugger.GetSelectedTarget()
    
    for module in target.module_iter():
        print str(module)

    for bp in target.breakpoint_iter():
        print str(bp)

    for wp in target.watchpoint_iter():
        print str(wp)

def module(debugger, commnad, result, internal_dict):
    target = debugger.GetSelectedTarget()
    
    for module in target.module_iter():
        print str(module)
        print('Number of sections: %d' % module.GetNumSections())
        for sec in module.section_iter():
            print(sec)

def process(debugger, commnad, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    print str(process)

    # print threads that belong the process.
    for thread in process:
        print str(thread)

def thread(debugger, commnad, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    print str(thread) 

def frame(debugger, commnad, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    
    for i in range(thread.GetNumFrames()):
        frame = thread.GetFrameAtIndex(i)
        print str(frame)

def symbol(debugger, commnad, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    
    for module in target.module_iter():
        print ("=========================================")
        print str(module)
        print ("=========================================")

        for symbol in module:
            if (symbol.GetType() == lldb.eSymbolTypeCode):
                if (symbol.GetName()):
                    print("[NAME] {} [ADDR] {} - {} "
                            .format(symbol.GetName(), 
                                    symbol.GetStartAddress(),
                                    symbol.GetEndAddress(),
                                    )
                            )
            target.BreakpointCreateByName(symbol.GetName(), 'a.out')

    process = target.LaunchSimple(None, None, os.getcwd())

    if not process.IsValid():
        print("process invalied")
        exit()

    while True:
        thread = get_stopped_thread(process, lldb.eStopReasonBreakpoint)
        if thread.IsValid():
            frame = thread.GetFrameAtIndex(0)
            print("stop by bp " + str(target) + str(frame))  
            process.Continue()
        else:
            print("no in bp")
            

def __lldb_init_module(debugger, internal_dict):
    command = ['target', 'module', 'process', 'thread', 'frame', 'symbol']
    cmdPrefix = 'st'
    cmdModule = 'study'
    for cmd in command:
        cmdPrefixed = cmdPrefix + cmd
        cmdModuled = cmdModule + '.' + cmd 
        cmdAppend = 'command script add -f '+cmdModuled+' '+cmdPrefixed
        debugger.HandleCommand(cmdAppend)
        print 'The '+cmdPrefixed+' command has been installed. '

