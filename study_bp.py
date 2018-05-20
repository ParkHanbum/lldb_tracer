
import lldb
import os
import sys
from lldbutil import *
from time import sleep


dbg = lldb.SBDebugger_Create()
dbg.SetAsync(True)
cwd = os.getcwd()

# binpath = os.path.join(cwd, 'a.out')
binpath = '/usr/local/bin/gcc'
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

error = lldb.SBError()
listener = lldb.SBListener("my listener")
event = lldb.SBEvent()
stream = lldb.SBStream()

process = target.Launch(listener,
			None, # argv
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

import threading
class MyListeningThread(threading.Thread):
	def run(self):
		while True:
			if listener.WaitForEvent(5, event):
				state = process.GetState()
				thread = process.GetSelectedThread()
				frame = thread.GetFrameAtIndex(0)
				desc = get_description(event)
				# print("EV DE :", desc)
				# print("EV DF :", event.GetDataFlavor())
				# print("STATE :", state_type_to_str(state))
				# print()
				if state == lldb.eStateExited:
					print("EXITED!")
					break
				if state == lldb.eStateStopped: 
					thread = get_stopped_thread(process, lldb.eStopReasonBreakpoint) 
					if thread is None:
						print("thread none")
						continue
					if thread.IsValid():
						print_stacktrace(thread)
						print("")
						thread.Resume()
						process.Continue()
			else:
				print("timeout occured")
		listener.Clear()
		return

my_thread = MyListeningThread()
my_thread.start()

process.Continue()
my_thread.join()
