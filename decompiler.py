# Copyright (c) 2012 Yuri K. Schlesner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import renpy.ast as ast

def pretty_print_ast(out_file, ast):
    for stmt in ast:
        print_statement(out_file, stmt, 0)

def indent(f, level):
    # Print indentation
    f.write(u'    ' * level)

def print_statement(f, statement, indent_level=0):
    indent(f, indent_level)

    func = statement_printer_dict.get(statement.__class__, print_Unknown)
    func(f, statement, indent_level)

def escape_string(s):
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\t', '\\t')
    return s

def print_atl(f, atl_block, indent_level):
    indent(f, indent_level)

    # TODO print ATL
    f.write(u"TODO atl\n")

def print_imspec(f, imspec):
    if imspec[1] is not None: # Expression
        # TODO expression
        f.write(u"TODO expression")
    else: # Image name
        f.write(' '.join(imspec[0]))

    # at
    if len(imspec[3]) > 0:
        # TODO at_list
        f.write(u" at TODO")

    # as
    if imspec[2] is not None:
        f.write(u" as %s" % (imspec[2], ))

    # behind
    if len(imspec[6]) > 0:
        # TODO behind
        f.write(u" behind TODO")

    # onlayer
    if imspec[4] != 'master':
        f.write(u" onlayer %s" % (imspec[4], ))

    # zorder
    # This isn't in the docs, but it's in the parser
    if imspec[5] is not None:
        f.write(u" zorder %s" % (imspec[5], ))

def print_Label(f, stmt, indent_level):
    f.write(u"label %s" % (stmt.name, ))
    if stmt.parameters is not None:
        # TODO parameters
        f.write(u"(parameters TODO)")
    f.write(u':\n')

    for sub_stmt in stmt.block:
        print_statement(f, sub_stmt, indent_level + 1)

def print_Say(f, stmt, indent_level):
    if stmt.who is not None:
        f.write(u"%s " % (stmt.who, ))
    f.write(u"\"%s\"" % (escape_string(stmt.what), ))
    if stmt.with_ is not None:
        f.write(u" with TODO")
        # TODO with_
    f.write(u'\n')

def print_Jump(f, stmt, indent_level):
    f.write(u"jump ")
    if stmt.expression:
        # TODO expression
        f.write(u"expression TODO")
    else:
        f.write(stmt.target)
    f.write(u'\n')

def print_Scene(f, stmt, indent_level):
    f.write(u"scene")
    if stmt.imspec is None:
        if stmt.layer != 'master':
            f.write(u" onlayer %s" % (stmt.layer, ))
    else:
        # TODO imspec
        f.write(u" TODO imspec")
    f.write(u'\n')

def print_With(f, stmt, indent_level):
    f.write(u"with %s\n" % (stmt.expr, ))

def print_Show(f, stmt, indent_level):
    f.write(u"show ")
    print_imspec(f, stmt.imspec)

    # with isn't handled here, but split in several statements

    if stmt.atl is not None:
        f.write(u':\n')
        print_atl(f, stmt.atl, indent_level+1)
    else:
        f.write('\n')

def print_Hide(f, stmt, indent_level):
    f.write(u"hide ")
    print_imspec(f, stmt.imspec)

    # with isn't handled here, but split in several statements

    f.write('\n')

statement_printer_dict = {
        ast.Label: print_Label,
        ast.Say: print_Say,
        ast.Jump: print_Jump,
        ast.Scene: print_Scene,
        ast.With: print_With,
        ast.Show: print_Show,
        ast.Hide: print_Hide,
    }

def print_Unknown(f, stmt, indent_level):
    print "Unknown AST node: %s" % (stmt.__class__.__name__, )
    f.write(u"<<<UNKNOWN NODE %s>>>\n" % (stmt.__class__.__name__, ))
