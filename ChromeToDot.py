#!/usr/bin/python

import os
import json
import optparse
from DOTElement import *

options = None
data = None

nodes = {}
edges = {}

# function associated events
fnBegin = 'B'
fnEnd = 'E'

# output file
output = None

# keys from chrome data format
kMetadata = "metadata"
kCommandLine = "command_line"

def gen_dot_header():
    global data
    command = data[kMetadata][kCommandLine]
    output.write('digraph "{}" {{\n'.format(command))
    output.write('\tsplines=ortho; \n')
    output.write('\tconcentrate=true; \n')

def gen_dot_attributes():
    output.write('\t# Attributes\n')
    output.write('\tnode [shape="rect",fontsize="7",style="filled"];\n')
    output.write('\tgraph [fontsize="7",overlap="scalexy"];\n')
    output.write('\tedge [fontsize="7"];\n')

def gen_dot_groups():
    pass

def gen_dot_nodes():
    output.write("\t# Nodes\n")
    for key, el in nodes.iteritems():
        name = el.name
        output.write(el.ToDotLabel())

    output.write('\n')


def gen_dot_edges():
    global edges
    output.write('\t# Edges\n')

    for (caller_name, callee_name), edge in edges.iteritems():
        output.write(edge.ToDotLabel())

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
    node = Node(**el)
    if not (node.name in nodes):
        nodes[node.name] = node

def add_edge(caller, callee):
    global edges
    caller_name = caller[Node.NodeName]
    callee_name = callee[Node.NodeName]

    if caller_name in nodes:
        caller = nodes[caller_name]
    else:
        caller = Node(**caller)
        nodes[caller_name] = caller

    if callee_name in nodes:
        callee = nodes[callee_name]
        callee.Called()
    else:
        callee = Node(**callee)
        nodes[callee_name] = callee

    edge = Edge(caller, callee)

    if (caller_name, callee_name) in edges:
        edges[(caller_name, callee_name)].Called()
    else:
        edges[(caller_name, callee_name)] = edge

def do_trans():
    global data
    stack = []
    data = parse_chrome_data()
    event_list = data["traceEvents"]

    for el in event_list:
        if el['ph'] == fnBegin:
            stack.append(el)
            add_node(el)
            if len(stack) > 1:
                add_edge(stack[-2], el)

        elif el['ph'] == fnEnd:
            if len(stack) > 1:
                stack.pop()


def parse_options():
    global options
    usage = "[USAGE] : %prog [options] arg"
    parser = optparse.OptionParser(usage)
    parser.add_option("-c", "--chrome-dump",
            action="store", dest="dumpfile", type="string", default="",
            help="Specify path of the data file in chrome tracing data format")
    parser.add_option("-o", "--output-file",
            action="store", dest="outputfile", type="string", default=None,
            help="Specify file to store the data in DOT formatted from chrome tracing data")

    (options, args) = parser.parse_args()


def prepare_output():
    global output
    global options
    print options

    output = "result.dot"
    if options.outputfile is not None:
        output = options.outputfile

    output = open(output, 'w+')


if __name__ == "__main__":
    parse_options()
    prepare_output()
    do_trans()
    gen_dot_header()
    gen_dot_attributes()
    gen_dot_groups()
    gen_dot_nodes()
    gen_dot_edges()
    gen_dot_footer()
