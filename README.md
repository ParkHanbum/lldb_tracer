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
'-b' option targeting the binary to tracing. 

```
$ python tracer.py -b trace_this
```
when tracing was finished, tracer make data file that named 'data.json' on its work directory. it contains the tracing datas that have formatted by chromium trace data. you can load it from chromium. 

if you want pretty result, use json tool that have embedded python. like this.
```
python -m json.tool data.json > <output_filename>
```

you can see the result like below after running it.
```
        {
            "name": "__libc_csu_init",
            "ph": "B",
            "pid": 2111,
            "tid": 2111,
            "ts": 1530333620.407282
        },
```


## Tracing with function arguments. 

if you use tracer.py with '-p' option, then tracer will record the function calling with its arguments. in same situation, only add '-p' option to command line arguments.

```
python tracer.py -b a.out -p 
```

after running it, you can see what has changed. 

```
        {
            "args": {
                "argc": "int 2",
                "argv": "char ** 0x00007ffd346c5858",
                "fini": "void (*)() None",
                "init": "int (*)(int, char **, char **) 0x0000000000400560",
                "main": "int (*)(int, char **, char **) 0x0000000000400541",
                "rtld_fini": "void (*)() None",
                "stack_end": "void * 0x00007ffd346c5848"
            },
            "name": "__libc_csu_init",
            "ph": "B",
            "pid": 2017,
            "tid": 2017,
            "ts": 1530333165.097881
        },
```


