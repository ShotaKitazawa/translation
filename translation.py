#!/usr/bin/env python3

import sys
import os
import re

code_flag = False
table_flag = False
table_border = False


def tomarkdown(line):
    global code_flag, table_flag
    markdown = ""

    if not (code_flag):
        if (table_flag):
            if not (line.startswith(",")):
                table_flag = False

        if (line.startswith("{{pre")):
            markdown = "```\n"
            code_flag = True
        elif (line.startswith("!!!")):
            markdown = "#" + line[3:]
        elif (line.startswith("!!")):
            markdown = "##" + line[2:]
        elif (line.startswith("!")):
            markdown = "###" + line[1:]
        elif (line.startswith("***")):
            markdown = "        -" + line[3:]
        elif (line.startswith("**")):
            markdown = "    -" + line[2:]
        elif (line.startswith("*")):
            markdown = "-" + line[1:]
        elif (line.startswith("\"\"")):
            markdown = "> " + line[3:]
        elif (line.startswith(",")):
            if not (table_flag):
                table_flag = True
                markdown = line.replace(",", "|").replace("\n", "") + "|\n|"
                for i in range(line.count(",")):
                    markdown += "-|"
                markdown += "\n"
            else:
                markdown = line.replace(",", "|").replace("\n", "") + "|\n"
        else:
            markdown = line

        markdown.replace("'''", "**")
        markdown = re.sub(r'<<\(.*\)>>', '`\1`', markdown)

    elif (line.startswith("}}")):
        markdown = "```\n"
        code_flag = False
    else:
        markdown = line
    return markdown


def tofswiki(line):

    global code_flag, table_flag, table_border
    fswiki = ""

    if not (code_flag):
        if (table_flag):
            if not (line.startswith("|")):
                table_flag = False

        if (line.startswith("```")):
            fswiki = "{{pre\n"
            code_flag = True
        elif (line.startswith("###")):
            fswiki = "!" + line[3:]
        elif (line.startswith("##")):
            fswiki = "!!" + line[2:]
        elif (line.startswith("#")):
            fswiki = "!!!" + line[1:]
        elif (line.startswith("        -")):
            fswiki = "***" + line[9:]
        elif (line.startswith("    -")):
            fswiki = "**" + line[5:]
        elif (line.startswith("-")):
            fswiki = "*" + line[1:]
        elif (line.startswith("> ")):
            fswiki = "\"\"" + line[2:]
        elif (line.startswith("|")):
            if not (table_flag):
                table_flag = True
                table_border = True
                fswiki = line.replace("|", ",").replace(",\n","\n")
            else:
                fswiki = line.replace("|", ",").replace(",\n","\n")
        else:
            fswiki = line

        fswiki.replace("**", "'''")
        fswiki = re.sub(r'`\(.*\)`', '<<\1>>', fswiki)

    elif (line.startswith("```")):
        fswiki = "}}\n"
        code_flag = False
    else:
        fswiki = line
    return fswiki


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
if (sys.argv[3] != "markdown" and sys.argv[3] != "fswiki"):
    print("argv[3] is only \"markdown\" or \"fswiki\"")

with open(sys.argv[1], "r") as rfile:
    with open(sys.argv[2], "w")as wfile:
        if (sys.argv[3] == "markdown"):
            for line in rfile:
                wfile.write(tomarkdown(line))
        elif (sys.argv[3] == "fswiki"):
            for line in rfile:
                if not (table_border):
                    wfile.write(tofswiki(line))
                else:
                    table_border = False
