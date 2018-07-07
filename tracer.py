#!/usr/bin/python

import lldb
import optparse
import os
import sys
import shlex
import threading
import time
import base64
import collections

from lldbutil import *

# parsed command line arugments.
options = None
program_name = None

# trace datas
traced_events = {}

# Global Methods
encode = base64.encodestring
decode = base64.decodestring

# event type
fBeginEvent = 'B'
fEndEvent = 'E'

def DEBUG(msg, obj):
    if options.verbose:
        stream = lldb.SBStream()
        obj.GetDescription(stream)
        print("======== {} ============".format(msg))
        print(stream.GetData())
        print("====================================")


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
                DEBUG("[EVENT] : ", event)

                if state == lldb.eStateExited:
                    print("EXITED!")
                    trace_finish(pid)
                    break

                if state == lldb.eStateStopped:
                    thread = get_stopped_thread(process,
                                                lldb.eStopReasonBreakpoint)
                    for thread in process.get_process_thread_list():
                        reason = thread.GetStopReason()
                        if reason is not lldb.eStopReasonInvalid:
                            print(stop_reason_to_str(reason))
                        continue
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

        module["name"] = program_name
        module["args"] = {"name" : program_name}
        events.append(module)
        if "traceEvents" in trace_format:
            trace_format["traceEvents"] += events
        else:
            trace_format["traceEvents"] = events
        print(events)
        print("")

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


def adjust_prev_event_ended(thread, frame):
    if len(traced_events) < 1:
        return

    print len(traced_events)
    prev_event = traced_events.values()[len(traced_events) - 1]
    prev_event = prev_event[-1]
    print prev_event

    if prev_event["ph"] != fBeginEvent:
        print prev_event["ph"]
        return

    prev_event_name = prev_event["name"]
    print prev_event_name

    for i in range(thread.GetNumFrames()):
        if i == 0 or i == 1: continue
        curr_frame = thread.GetFrameAtIndex(i)
        DEBUG("FRAME", curr_frame)
        curr_frame_name = curr_frame.GetDisplayFunctionName()

        # generally calling stack.
        if prev_event_name == curr_frame_name:
            print(i, prev_event_name, curr_frame_name)
            return

    # adjust previous event had ended.
    print (" ADJUSTMENT " )
    prev_event_clone = prev_event.copy()
    prev_event_clone["ph"] = fEndEvent
    traced_events.values().append(prev_event_clone)


def save_event(frame, event_type, args=None):
    thread = frame.GetThread()
    process = thread.GetProcess()
    target = process.GetTarget()
    symbol = frame.GetSymbol()

    addr = frame.GetPC()
    pid = process.GetProcessID()
    tid = thread.GetThreadID()
    tname = thread.GetThreadID()

    names = lldb.SBStringList()

    if addr in BreakpointList:
        if event_type == fBeginEvent:
            adjust_prev_event_ended(thread, frame)

        BreakpointList[addr].GetNames(names)
        name = names.GetStringAtIndex(0)
        if name is not None:
            name = decode(name)
            _event = collections.OrderedDict()
            _event["name"] = name[:-2]
            _event["ph"] = name[-1:]
            _event["pid"] = pid
            _event["tid"] = tid
            _event["ts"] = time.time()
            if args:
                _event["args"] = args
            if thread.GetNumFrames() > 2:
                caller = thread.GetFrameAtIndex(1)
                _event["caller"] = caller.GetDisplayFunctionName()

        else:
            print ("NAME IS NONE : " + hex(addr))

        if not (tid, tname) in traced_events:
            traced_events[tid, tname] = []

        traced_events[tid, tname].append(_event)
    else:
        print ("ADDRESS IS NOT MATCHED : " + hex(addr))


def handle_breakpoint(frame, bp_log, dict):
    thread = frame.GetThread()
    process = thread.GetProcess()
    target = process.GetTarget()
    symbol = frame.GetSymbol()

    addr = frame.GetPC()
    pid = process.GetProcessID()
    tid = thread.GetThreadID()
    tname = thread.GetThreadID()

    event_type = None

    if addr in BreakpointList:
        names = lldb.SBStringList()
        BreakpointList[addr].GetNames(names)
        name = names.GetStringAtIndex(0)
        if name is not None:
            name = decode(name)
            _event = collections.OrderedDict()
            _event["name"] = name[:-2]
            event_type = name[-1:]
            _event["ph"] = event_type
            _event["pid"] = pid
            _event["tid"] = tid
            _event["ts"] = time.time()

    # save arguments
    args = None

    if event_type is not fEndEvent:
        if options.print_args:
            # arguments     => True
            # locals        => False
            # statics       => False
            # in_scope_only => True
            vars = frame.GetVariables(True, False, False, True)
            if vars:
                args = collections.OrderedDict()
                for var in reversed(vars):
                    args[var.GetName()] = "{} {}".format(
                            var.GetTypeName(), var.GetValue())
                print(args)
                print(get_args_as_string(frame))
            else:
                print("Cannot parse arguments")

    if addr in BreakpointList:
        save_event(frame, event_type, args=args)
    else:
        print("Must not reach here : " + hex(addr))

    thread.Resume()
    process.Continue()


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

    process = target.Launch(listener,
            argv, # argv
            None, # envp
            None, # stdin_path
            'stdout_log', # stdout_path
            'stderr_log', # stderr_path
            None, # working directory
            0,    # launch flag
            True, # stop at entry
            error) # error

    if not process.IsValid():
        print("process invalied")
        exit()

    desc = lldb.SBStream()
    count = 0
    for module in target.module_iter():
        print str(module)

        for symbol in module:
            if (symbol.GetType() == lldb.eSymbolTypeCode
                    and symbol.GetName()):
                # find end of function to set the breakpoint.
                instlist = symbol.GetInstructions(target, "intel")
                size = instlist.GetSize()
                if size >= 2:
                    inst = instlist.GetInstructionAtIndex(size-1)
                else:
                    continue

                DEBUG("INSTRUCTIONS", instlist)
                DEBUG("LAST INSTRUCTION", inst)

                # find address to be breakpoint.
                # at this point, target already loaded to process.
                # so, we can find mapped-address of symbol from process.
                begin = symbol.GetStartAddress().GetLoadAddress(target)
                end = inst.GetAddress().GetLoadAddress(target)

                bpb = target.BreakpointCreateByAddress(begin)
                bpb.SetScriptCallbackFunction("handle_breakpoint")
                bpb.AddName(encode(symbol.GetName() + ":B"))
                BreakpointList[begin] = bpb

                bpe = target.BreakpointCreateByAddress(end)
                bpe.SetScriptCallbackFunction("handle_breakpoint")
                bpe.AddName(encode(symbol.GetName() + ":E"))
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
    parser.add_option("-p", "--print-args",
            action="store_true", dest="print_args", default=False,
            help="Print function arguments.")
    parser.add_option("--argv",
            action="store", dest="argv", default="", type="string",
            help="Specify the Value that as argument")
    (options, args) = parser.parse_args()


if __name__ == "__main__":
    parse_options()
    do_trace()
