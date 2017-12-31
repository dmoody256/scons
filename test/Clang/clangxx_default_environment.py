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

import TestSCons
import sys

_exe = TestSCons._exe
test = TestSCons.TestSCons()

if not test.where_is('clang++'):
    test.skip_test("Could not find 'clang++', skipping test.\n")

if 'win32' == sys.platform:
    test.skip_test("clang++ is not part of default environment on windows, skipping test.\n")


## This will likely NOT use clang++.

test.write('SConstruct', """\
env = Environment()
if env['CXX'] != 'clang++':
    env['CXX'] = 'clang++'
env.Program('foo.cpp')
""")

test.write('foo.cpp', """\
#include <iostream>
int main(int argc, char ** argv) {
    std::cout << "Hello!" << std::endl;
    return 0;
}
""")

test.run()

test.run(program=test.workpath('foo'+_exe))

test.fail_test(not test.stdout() == 'Hello!\n')

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: