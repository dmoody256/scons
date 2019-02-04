"""SCons.Tool.lex

Tool-specific initialization for lex.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

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

import os.path
import sys

import SCons.Action
import SCons.Tool
import SCons.Util
from SCons.Platform.mingw import MINGW_DEFAULT_PATHS
from SCons.Platform.cygwin import CYGWIN_DEFAULT_PATHS

LexAction = SCons.Action.Action("$LEXCOM", "$LEXCOMSTR")

def lexEmitter(target, source, env):
    sourceBase, sourceExt = os.path.splitext(SCons.Util.to_String(source[0]))

    if sourceExt == ".lm":           # If using Objective-C
        target = [sourceBase + ".m"] # the extension is ".m".

    # This emitter essentially tries to add to the target all extra
    # files generated by flex.

    # Different options that are used to trigger the creation of extra files.
    fileGenOptions = ["--header-file=", "--tables-file="]

    lexflags = env.subst("$LEXFLAGS", target=target, source=source)
    for option in SCons.Util.CLVar(lexflags):
        for fileGenOption in fileGenOptions:
            l = len(fileGenOption)
            if option[:l] == fileGenOption:
                # A file generating option is present, so add the
                # file name to the target list.
                fileName = option[l:].strip()
                target.append(fileName)
    return (target, source)

def get_lex_path(env, append=False):
    """
    Find the a path containing the lex or flex binaries. If a construction 
    environment is passed in then append the path to the ENV PATH.
    """
    lex = SCons.Tool.find_program_path(env, 'lex', default_paths=MINGW_DEFAULT_PATHS + CYGWIN_DEFAULT_PATHS )
    if lex:
        if append:
            lex_bin_dir = os.path.dirname(lex)
            env.AppendENVPath('PATH', lex_bin_dir)
        return lex

    flex = SCons.Tool.find_program_path(env, 'flex', default_paths=MINGW_DEFAULT_PATHS + CYGWIN_DEFAULT_PATHS )
    if flex:
        if append:
            flex_bin_dir = os.path.dirname(flex)
            env.AppendENVPath('PATH', flex_bin_dir)
        return flex
    else:
        SCons.Warnings.Warning('lex tool requested, but lex or flex binary not found in ENV PATH')


def generate(env):
    """Add Builders and construction variables for lex to an Environment."""
    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)

    if sys.platform == 'win32':
        if(get_lex_path(env, append=True)):
            SCons.Tool.Tool('mingw')(env)

    # C
    c_file.add_action(".l", LexAction)
    c_file.add_emitter(".l", lexEmitter)

    c_file.add_action(".lex", LexAction)
    c_file.add_emitter(".lex", lexEmitter)

    # Objective-C
    cxx_file.add_action(".lm", LexAction)
    cxx_file.add_emitter(".lm", lexEmitter)

    # C++
    cxx_file.add_action(".ll", LexAction)
    cxx_file.add_emitter(".ll", lexEmitter)

    env["LEX"] = env.Detect("flex") or "lex"
    env["LEXFLAGS"] = SCons.Util.CLVar("")
    env["LEXCOM"] = "$LEX $LEXFLAGS -t $SOURCES > $TARGET"

def exists(env):
    if sys.platform == 'win32':
        return get_lex_path(env)
    else:
        return env.Detect(["flex", "lex"])

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
