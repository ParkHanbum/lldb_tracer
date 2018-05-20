#!/usr/bin/python

import lldb
import optparse
import os
import sys
import shlex
import threading

from lldbutil import *

# parsed command line arugments.
options = None


class MyListeningThread(threading.Thread):
    def __init__(self, listener, process):
        super(MyListeningThread, self).__init__()
        self.listener = listener
        self.process = process

    def run(self):
        event = lldb.SBEvent()
        process = self.process
        listener = self.listener

        while True:
            if listener.WaitForEvent(5, event):
                state = process.GetState()
                thread = process.GetSelectedThread()

                if state == lldb.eStateExited:
                    print("EXITED!")
                    break
                if state == lldb.eStateStopped:
                    thread = get_stopped_thread(process,
                                                lldb.eStopReasonBreakpoint)
                    if thread is None:
                        print("thread none")
                        continue
                    if thread.IsValid():
                        print("======= [Print Stack Trace] =======")
                        # print_stacktrace(thread)
                        stacktrace = get_stacktrace(thread)
                        print(stacktrace)
                        print("======= =================== =======")

                        thread.Resume()
                        process.Continue()
            else:
                print("timeout occured")
        listener.Clear()
        return


def get_stacktrace(thread, string_buffer=False):
    """Prints a simple stack trace of this thread."""
    result = {}
    target = thread.GetProcess().GetTarget()
    depth = thread.GetNumFrames()
    mods = get_module_names(thread)
    funcs = get_function_names(thread)
    symbols = get_symbol_names(thread)
    files = get_filenames(thread)
    lines = get_line_numbers(thread)
    addrs = get_pc_addresses(thread)

    result["TID"] = thread.GetThreadID()
    result["TNAME"] = thread.GetName()
    result["FRAMES"] = []

    for i in range(depth):
        frame = thread.GetFrameAtIndex(i)
        function = frame.GetFunction()

        load_addr = addrs[i].GetLoadAddress(target)
        if not function:
            file_addr = addrs[i].GetFileAddress()
            start_addr = frame.GetSymbol().GetStartAddress().GetFileAddress()
            symbol_offset = file_addr - start_addr

            result["FRAMES"].append({"num":i, "addr":load_addr, "mod":mods[i],
                "symbol":symbols[i], "offset":symbol_offset})
        else:
            result["FRAMES"].append({
                "num":i, "addr":load_addr, "mod":mods[i],
                "func":'%s [inlined]' %
                funcs[i] if frame.IsInlined() else funcs[i],
                "file":files[i], "line":lines[i],
                "args":get_args_as_string(frame, showFuncName=False)
                if not frame.IsInlined() else '()'})

    return result


def do_trace():
    global options
    dbg = lldb.SBDebugger_Create()
    dbg.SetAsync(True)

    binpath = options.bin
    argv = (options.argv).split(' ')
    target = dbg.CreateTarget(binpath)

    for module in target.module_iter():
        print str(module)

        for symbol in module:
            if (symbol.GetType() == lldb.eSymbolTypeCode):
                if (symbol.GetName()):
                    print("{} {}-{}"
                            .format(symbol.GetName(),
                                symbol.GetStartAddress(),
                                symbol.GetEndAddress()))
                    target.BreakpointCreateByName(symbol.GetName(), binpath)

    print("Start Tracing...")
    print(binpath)
    print(argv)

    error = lldb.SBError()
    listener = lldb.SBListener("my listener")

    process = target.Launch(listener,
            argv, # argv
            None, # envp
            None, # stdin_path
            None, # stdout_path
            None, # stderr_path
            None, # working directory
            0,    # launch flag
            True, # stop at entry
            error) # error

    if not process.IsValid():
        print("process invalied")
        exit()

    my_thread = MyListeningThread(listener, process)
    my_thread.start()
    process.Continue()
    my_thread.join()


def parse_options():
    global options
    usage = "[USAGE] : %prog [options] arg"
    parser = optparse.OptionParser(usage)
    parser.add_option("-b", "--bin",
            action="store", dest="bin", type="string", default="",
            help="Specify Absolute path of the Binary which to be traced")
    parser.add_option("--argv",
            action="store", dest="argv", default="", type="string",
            help="Specify the Value that as argument")
    (options, args) = parser.parse_args()


if __name__ == "__main__":
    parse_options()
    do_trace()
