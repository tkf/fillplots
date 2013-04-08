try:
    execfile = execfile
except NameError:
    def execfile(filename, globals=None, locals=None):
        code = compile(open(filename).read(), filename, 'exec')
        exec(code, globals, locals)

try:
    reduce = reduce
except NameError:
    from functools import reduce
