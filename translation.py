#!/usr/bin/env python3

import sys
import os

code_flag = True
table_flag = True


def tomarkdown(line):
    global code_flag, table_flag
    markdown = ""
    if (code_flag):
        if not (table_flag):
            if not (line[0:1] == ","):
                table_flag = True
        if (line[0:5] == "{{pre"):
            markdown = "```\n"
            code_flag = False
        elif (line[0:3] == "!!!"):
            markdown = "#" + line[3:]
        elif (line[0:2] == "!!"):
            markdown = "##" + line[2:]
        elif (line[0:1] == "!"):
            markdown = "###" + line[1:]
        elif (line[0:3] == "***"):
            markdown = "        -" + line[3:]
        elif (line[0:2] == "**"):
            markdown = "    -" + line[2:]
        elif (line[0:1] == "*"):
            markdown = "-" + line[1:]
        elif (line[0:2] == "\"\""):
            markdown = "> " + line[3:]
        elif (line[0:1] == ","):
            if (table_flag):
                table_flag = False
                markdown = line.replace(",", "|").replace("\n", "") + "|\n|"
                for i in range(line.count(",")):
                    markdown += "-|"
                markdown += "\n"
            else:
                markdown = line.replace(",", "|").replace("\n", "") + "|\n"
        else:
            markdown = line
        markdown.replace("'''", "**")
    elif (line[0:2] == "}}"):
        markdown = "```\n"
        code_flag = True
    else:
        markdown = line
    return markdown


def tofreestyle(line):
    freestyle = ""
    if (code_flag):
        pass
    return freestyle


# check
if (len(sys.argv) <= 3):
    print("invalid argument:", sys.argv[0], "(input)", "(output)", "(trancelate to)")
    sys.exit(1)
if not (os.path.exists(sys.argv[1])):
    print(sys.argv[1] + ": file dont exists.")
    sys.exit(1)
if (os.path.exists(sys.argv[2])):
    check = input(sys.argv[2] + ": file already exists. overwrite? [y/n]: ")
    if (check.lower() != "y"):
        sys.exit(1)
if (sys.argv[3] != "markdown" and sys.argv[3] != "freestyle"):
    print("argv[3] is only \"markdown\" or \"freestyle\"")

with open(sys.argv[1], "r") as rfile:
    with open(sys.argv[2], "w")as wfile:
        for line in rfile:
            if (sys.argv[3] == "markdown"):
                wfile.write(tomarkdown(line))
            elif (sys.argv[3] == "freestyle"):
                print("not implement yet")
                #wfile.write(tofreestyle(line))
