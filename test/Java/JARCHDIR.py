#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

"""
Test that when JARCHDIR that our command to create .jar files
correctly finds all the .class files (by putting -C in front
of each class file argument).

Includes logic to make sure that expansions of $JARCHDIR that include
${TARGET} or ${SOURCE} work.
"""

import os

import TestSCons

test = TestSCons.TestSCons()

where_javac, java_version = test.java_where_javac()
where_jar = test.java_where_jar()



test.write('SConstruct', """
dir = 'dist'
env = Environment(tools    = ['javac', 'jar'],
                  JAVAC = r'%(where_javac)s',
                  JAR = r'%(where_jar)s',
                  JARCHDIR = dir)
bin = env.Java(dir, Dir('./'))
jar = env.Jar(File('c.jar', dir), bin)

# Make sure we handle class files with $ in them, such as typically
# created for inner classes.
env = env.Clone(JARCHDIR = '.')
inner = env.Jar('inner.jar', 'Inner$$Class.class')

target_env = env.Clone(JARCHDIR = '${TARGET.dir}')
target_env.Jar('out/t.jar', 'in/t.class')

source_env = env.Clone(JARCHDIR = '${SOURCE.dir}')
source_env.Jar('out/s.jar', 'in/s.class')

Default(bin, jar, inner)
""" % locals())



test.subdir('in')

test.write('a.java', """\
package foo.bar;
public class a {}
""")

test.write('b.java', """\
package foo.bar;
public class b {}
""")

test.write(['in', 's.class'], "s.class\n")
test.write(['in', 't.class'], "t.class\n")

test.write('Inner$Class.class', "Inner$Class.class\n")

test.run(arguments = '.')



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
