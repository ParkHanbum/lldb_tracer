#!/usr/bin/python

import lldb
import optparse
import os
import sys
import shlex
import threading
import time
import base64

from lldbutil import *

# parsed command line arugments.
options = None
program_name = None

# trace datas
traced_events = {}


class MyListeningThread(threading.Thread):
    def __init__(self, listener, process):
        super(MyListeningThread, self).__init__()
        self.listener = listener
        self.process = process

    def run(self):
        global options
        event = lldb.SBEvent()
        process = self.process
        listener = self.listener
        pid = process.GetProcessID()

        while True:
            if listener.WaitForEvent(5, event):
                state = process.GetState()

                if state == lldb.eStateExited:
                    print("EXITED!")
                    trace_finish(pid)
                    break
                if state == lldb.eStateStopped:
                    thread = get_stopped_thread(process,
                                                lldb.eStopReasonBreakpoint)
                    if thread is None:
                        print("thread none")
                        process.Continue()
                        continue

                    if thread.IsValid():
                        thread = process.GetSelectedThread()
                        tid = thread.GetThreadID()
                        pid = thread.GetProcess().GetProcessID()
                        tname = thread.GetName()
                        stacktrace = get_stacktrace(thread)
                        if options.verbose:
                            print("======= [Print Stack Trace] =======")
                            # print_stacktrace(thread)
                            print(stacktrace)
                            print("======= =================== =======")
                        current_frame = stacktrace["FRAMES"].pop(0)
                        addr = current_frame["addr"]
                        names = lldb.SBStringList()
                        BreakpointList[addr].GetNames(names)
                        name = names.GetStringAtIndex(0)
                        if name is not None:
                            name = base64.decodestring(name)
                            _event = {}
                            _event["name"] = name[:-2]
                            _event["ph"] = name[-1:]
                            _event["pid"] = pid
                            _event["tid"] = tid
                            _event["ts"] = time.time()

                            if not (tid, tname) in traced_events:
                                traced_events[tid, tname] = []

                            traced_events[tid, tname].append(_event)

                        thread.Resume()
                        process.Continue()
            else:
                print("timeout occured")

        listener.Clear()
        return


def trace_finish(pid):
    trace_format = {}

    for (tid, tname), events in traced_events.iteritems():
        module = {}
        module["ts"] = 0
        module["ph"] = "M"

        if pid == tid:
            module["pid"] = pid
        else:
            module["tid"] = tid

        module["name"] = tname
        module["args"] = {"name" : program_name}
        events.append(module)
        if "traceEvents" in trace_format:
            trace_format["traceEvents"] += events
        else:
            trace_format["traceEvents"] = events
        print(events)

    trace_format["displayTimeUnit"] = "ns"
    metadata = {}
    metadata["command_line"] = "{} {}".format(options.bin, options.argv)
    trace_format["metadata"] = metadata

    import json
    with open('data.json', 'w') as fp:
        json.dump(trace_format, fp)


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

"""
prev_stacktrace = None
def print_customize_trace(stacktrace):
    global prev_stacktrace
    if prev_stacktrace is None:
        prev_stacktrace = stacktrace
        return

    own_st = handle_stacktrace(stacktrace)
    prev_stacktrace = stacktrace
"""

BreakpointList = {}
def do_trace():
    global options, program_name
    dbg = lldb.SBDebugger_Create()
    dbg.SetAsync(True)

    binpath = options.bin
    argv = (options.argv).split(' ')
    target = dbg.CreateTarget(binpath)
    program_name = target.GetExecutable().GetFilename()
    error = lldb.SBError()
    listener = lldb.SBListener("my listener")
    encode = base64.encodestring
    decode = base64.decodestring

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

    count = 0
    for module in target.module_iter():
        print str(module)

        for symbol in module:
            if (symbol.GetType() == lldb.eSymbolTypeCode):
                begin = symbol.GetStartAddress().GetLoadAddress(target)
                end   = symbol.GetEndAddress().GetLoadAddress(target)-1

                if begin is None or end is None:
                    print(count, symbol)
                    count += 1
                    continue

                bpb = target.BreakpointCreateByAddress(begin)
                bpe = target.BreakpointCreateByAddress(end)

                if (symbol.GetName()):
                    bpb.AddName(encode(symbol.GetName() + ":B"))
                    BreakpointList[begin] = bpb
                    bpe.AddName(encode(symbol.GetName() + ":E"))
                    BreakpointList[end] = bpe
                else:
                    bpb.AddName(encode(str(begin) + ":B"))
                    BreakpointList[begin] = bpb
                    bpe.AddName(encode(str(end) + ":E"))
                    BreakpointList[end] = bpe

    print("Start Tracing...")
    print(binpath)
    print(argv)

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
    parser.add_option("-v", "--verbose",
            action="store_true", dest="verbose", default=False,
            help="Running with detail messages")
    parser.add_option("--argv",
            action="store", dest="argv", default="", type="string",
            help="Specify the Value that as argument")
    (options, args) = parser.parse_args()


if __name__ == "__main__":
    parse_options()
    do_trace()
