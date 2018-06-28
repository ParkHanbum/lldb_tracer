# LLDB tracer
some examples to study lldb python scripting

an example c program to tracing. 

```
// test_trace.c
#include <stdio.h>
#include <stdlib.h>

int main()
{
        printf("HELLO WORLD\n");
}
```

compile this c source file with '-g' option for debugging symbol. 

```
$ gcc -g test_trace.c -o trace_this
```

running tracer.py with '-b' option. 
'-b' option targgeting the binary to tracing. 

```
$ python tracer.py -b trace_this
```

below message will printed to stdout.
this message include function symbols that could be traced. 
```
main
(x86_64) /home/m/git/lldb_script_study/trace_this
deregister_tm_clones trace_this`deregister_tm_clones-trace_this`register_tm_clones
register_tm_clones trace_this`register_tm_clones-trace_this`__do_global_dtors_aux
__do_global_dtors_aux trace_this`__do_global_dtors_aux-trace_this`frame_dummy
frame_dummy trace_this`frame_dummy-trace_this`main at test_trace.c:5
__libc_csu_fini trace_this`__libc_csu_fini-
_fini trace_this`-trace_this..fini + 12
__libc_csu_init trace_this`__libc_csu_init-
_start trace_this`-trace_this`deregister_tm_clones
main trace_this`main at test_trace.c:5-
_init trace_this`-trace_this..init + 32
Start Tracing...
trace_this
```

after that, it will set the breakpoint to each functions at listed at symbols table. 
when Program Counter reach breakpoint then will print the stack trace to stdout which contain the control flow and arguments to call the function. 

```
======= [Print Stack Trace] =======
Stack trace for thread id=0xff3 name=trace_this queue=None stop reason=breakpoint
  frame #0: 0x00000000400430 trace_this`None + 0
======= =================== =======
======= [Print Stack Trace] =======
Stack trace for thread id=0xff3 name=trace_this queue=None stop reason=breakpoint
  frame #0: 0x00000000400560 trace_this`__libc_csu_init + 0
  frame #1: 0x007f529a5427bf libc.so.6`__libc_start_main at libc-start.c:247 ((int (*)(int, char **, char **))main=0x0000000000400541, (int)argc=2, (char **)argv=0x00007ffec4
dc98e8, (int (*)(int, char **, char **))init=0x0000000000400560, (void (*)())fini=None, (void (*)())rtld_fini=None, (void *)stack_end=0x00007ffec4dc98d8)
  frame #2: 0x00000000400459 trace_this`None + 41
======= =================== =======
======= [Print Stack Trace] =======
Stack trace for thread id=0xff3 name=trace_this queue=None stop reason=breakpoint
  frame #0: 0x000000004003d0 trace_this`None + 0
  frame #1: 0x00000000400591 trace_this`__libc_csu_init + 49
  frame #2: 0x007f529a5427bf libc.so.6`__libc_start_main at libc-start.c:247 ((int (*)(int, char **, char **))main=0x0000000000400541, (int)argc=2, (char **)argv=0x00007ffec4
dc98e8, (int (*)(int, char **, char **))init=0x0000000000400560, (void (*)())fini=None, (void (*)())rtld_fini=None, (void *)stack_end=0x00007ffec4dc98d8)
  frame #3: 0x00000000400459 trace_this`None + 41
======= =================== =======
======= [Print Stack Trace] =======
Stack trace for thread id=0xff3 name=trace_this queue=None stop reason=breakpoint
  frame #0: 0x00000000400535 trace_this`frame_dummy + 0
  frame #1: 0x000000004005ad trace_this`__libc_csu_init + 77
  frame #2: 0x007f529a5427bf libc.so.6`__libc_start_main at libc-start.c:247 ((int (*)(int, char **, char **))main=0x0000000000400541, (int)argc=2, (char **)argv=0x00007ffec4
dc98e8, (int (*)(int, char **, char **))init=0x0000000000400560, (void (*)())fini=None, (void (*)())rtld_fini=None, (void *)stack_end=0x00007ffec4dc98d8)
  frame #3: 0x00000000400459 trace_this`None + 41
======= =================== =======
======= [Print Stack Trace] =======
Stack trace for thread id=0xff3 name=trace_this queue=None stop reason=breakpoint
  frame #0: 0x000000004004a3 trace_this`register_tm_clones + 0
  frame #1: 0x0000000040053e trace_this`frame_dummy + 9
  frame #2: 0x000000004005ad trace_this`__libc_csu_init + 77
  frame #3: 0x007f529a5427bf libc.so.6`__libc_start_main at libc-start.c:247 ((int (*)(int, char **, char **))main=0x0000000000400541, (int)argc=2, (char **)argv=0x00007ffec4
dc98e8, (int (*)(int, char **, char **))init=0x0000000000400560, (void (*)())fini=None, (void (*)())rtld_fini=None, (void *)stack_end=0x00007ffec4dc98d8)
  frame #4: 0x00000000400459 trace_this`None + 41
======= =================== =======
======= [Print Stack Trace] =======
Stack trace for thread id=0xff3 name=trace_this queue=None stop reason=breakpoint
  frame #0: 0x00000000400545 trace_this`main at test_trace.c:6 ()
  frame #1: 0x007f529a542830 libc.so.6`__libc_start_main at libc-start.c:291 ((int (*)(int, char **, char **))main=0x0000000000400541, (int)argc=2, (char **)argv=0x00007ffec4
dc98e8, (int (*)(int, char **, char **))init=None, (void (*)())fini=None, (void (*)())rtld_fini=None, (void *)stack_end=0x00007ffec4dc98d8)
  frame #2: 0x00000000400459 trace_this`None + 41
  ======= =================== =======
======= [Print Stack Trace] =======
Stack trace for thread id=0xff3 name=trace_this queue=None stop reason=breakpoint
  frame #0: 0x00000000400511 trace_this`__do_global_dtors_aux + 0
  frame #1: 0x007f529a8fcde7 ld-linux-x86-64.so.2`??? + 823
  frame #2: 0x007f529a55bff8 libc.so.6`__run_exit_handlers at exit.c:82 ((int)status=0, (exit_function_list **)listp=0x00007f529a8e65f8, (bool)run_list_atexit=None)
  frame #3: 0x007f529a55c045 libc.so.6`__GI_exit at exit.c:104 ((int)status=None)
  frame #4: 0x007f529a542837 libc.so.6`__libc_start_main at libc-start.c:325 ((int (*)(int, char **, char **))main=None, (int)argc=None, (char **)argv=None, (int (*)(int, cha
r **, char **))init=None, (void (*)())fini=None, (void (*)())rtld_fini=None, (void *)stack_end=0x00007ffec4dc98d8)
  frame #5: 0x00000000400459 trace_this`None + 41
======= =================== =======
======= [Print Stack Trace] =======
Stack trace for thread id=0xff3 name=trace_this queue=None stop reason=breakpoint
  frame #0: 0x0000000040045a trace_this`deregister_tm_clones + 0
  frame #1: 0x00000000400529 trace_this`__do_global_dtors_aux + 24
  frame #2: 0x007f529a8fcde7 ld-linux-x86-64.so.2`??? + 823
  frame #3: 0x007f529a55bff8 libc.so.6`__run_exit_handlers at exit.c:82 ((int)status=0, (exit_function_list **)listp=0x00007f529a8e65f8, (bool)run_list_atexit=None)
  frame #4: 0x007f529a55c045 libc.so.6`__GI_exit at exit.c:104 ((int)status=None)
  frame #5: 0x007f529a542837 libc.so.6`__libc_start_main at libc-start.c:325 ((int (*)(int, char **, char **))main=None, (int)argc=None, (char **)argv=None, (int (*)(int, cha
r **, char **))init=None, (void (*)())fini=None, (void (*)())rtld_fini=None, (void *)stack_end=0x00007ffec4dc98d8)
  frame #6: 0x00000000400459 trace_this`None + 41
======= =================== =======
======= [Print Stack Trace] =======
Stack trace for thread id=0xff3 name=trace_this queue=None stop reason=breakpoint
  frame #0: 0x000000004005d4 trace_this`None + 0
  frame #1: 0x007f529a8fce05 ld-linux-x86-64.so.2`??? + 853
  frame #2: 0x007f529a55bff8 libc.so.6`__run_exit_handlers at exit.c:82 ((int)status=0, (exit_function_list **)listp=0x00007f529a8e65f8, (bool)run_list_atexit=None)
  frame #3: 0x007f529a55c045 libc.so.6`__GI_exit at exit.c:104 ((int)status=None)
  frame #4: 0x007f529a542837 libc.so.6`__libc_start_main at libc-start.c:325 ((int (*)(int, char **, char **))main=None, (int)argc=None, (char **)argv=None, (int (*)(int, cha
r **, char **))init=None, (void (*)())fini=None, (void (*)())rtld_fini=None, (void *)stack_end=0x00007ffec4dc98d8)
  frame #5: 0x00000000400459 trace_this`None + 41
======= =================== =======
```
 
