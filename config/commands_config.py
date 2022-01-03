commands = {
    '+': lambda x, y: x+y,
    '-': lambda x, y: y-x,
    '*': lambda x, y: y*x,
    '/': lambda x, y: y/x,
    'min': lambda x: min(x),
    'max': lambda x: max(x),
    'sum': lambda x: sum(x),
    'avg': lambda x: sum(x)/len(x),
}
commands_names = set(['avg', 'min', 'max', 'sum'])
precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3,
}
