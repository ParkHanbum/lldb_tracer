#!/usr/bin/python

import os
import json
import optparse


options = None
data = None

nodes = []
edges = []

# function associated events
fnBegin = 'B'
fnEnd = 'E'

# output file
output = open('result.dot', 'w+')


def gen_dot_header():
    global data
    print data
    command = data["metadata"]["command_line"]
    output.write('digraph "{}" {{\n'.format(command))
    output.write('\tsplines = ortho; \n')
    output.write('\tconcentrate = true; \n')

def gen_dot_attributes():
    output.write('\t# Attributes\n')
    output.write('\tnode [ shape = "rect", fontsize = "7", style = "filled" ];\n')
    output.write('\tgraph [ fontsize = "7", overlap = "scalexy"]; \n')
    output.write('\tedge [ fontsize = "7" ]; \n')

def gen_dot_groups():
    pass

def gen_dot_nodes():
    output.write("\t# Nodes\n")
    for el in nodes:
        name = el["name"]
        output.write('\t"{name}" [label = "{label}"]\n'.format(
            name=name,
            label=name))

    output.write('\n')


def gen_dot_edges():
    global edges
    output.write('\t# Edges\n')

    for (callee, caller) in edges:
        callee_name = callee["name"]
        caller_name = caller["name"]
        output.write('\t"{caller_name}" -> "{callee_name}" [label="{label}"]\n'.format(
            caller_name = caller_name, callee_name = callee_name,
            label = "1"))

    output.write('\n')


def gen_dot_footer():
    output.write("}\n")
    output.flush()
    output.close()

def parse_chrome_data():
    print options
    data = open(os.path.abspath(options.dumpfile)).read()

    try:
        data = json.loads(data)
    except ValueError, e:
        print "EXCEPTION"
        print e

    return data

def add_node(el):
    global nodes
    nodes.append(el)

def add_edge(el, caller):
    global edges
    edges.append((el,caller))

def do_trans():
    global data
    stack = []
    data = parse_chrome_data()
    event_list = data["traceEvents"]
    print event_list

    for el in event_list:
        print el
        if el['ph'] == fnBegin:
            stack.append(el)
            add_node(el)
            if len(stack) > 1:
                print "STACK"
                print stack
                add_edge(el, stack[-2])
            pass

        if el['ph'] == fnEnd:
            stack.pop()
            pass


def parse_options():
    global options
    usage = "[USAGE] : %prog [options] arg"
    parser = optparse.OptionParser(usage)
    parser.add_option("-c", "--chrome-dump",
            action="store", dest="dumpfile", type="string", default="",
            help="Specify path of the data file in chrome tracing data format")

    (options, args) = parser.parse_args()

if __name__ == "__main__":
    parse_options()
    do_trans()
    gen_dot_header()
    gen_dot_attributes()
    gen_dot_groups()
    gen_dot_nodes()
    gen_dot_edges()
    gen_dot_footer()
