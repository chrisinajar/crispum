from functools import partial
from functools import reduce
from .pluck import pluckParser
from .simple import simpleParser
from .conditional import conditionalParser
from .philter import FILTER_CONST
from .philter import filterParser
import dot_prop
import six

def crispum (options):
  return combineParsers(createParser(options), processOutput)

def createParser (options):
  if isinstance(options, list):
    return joinParsers(options)

  parse = None
  parserType = options['type']
  if parserType == 'simple':
    parse = partial(simpleParser, options)
  if parserType == 'pluck':
    parse = partial(pluckParser, options)
  if parserType == 'conditional':
    parse = partial(conditionalParser, options, createParser)
  if parserType == 'filter':
    parse = partial(filterParser, options)

  if options.get('array') is True:
    parse = partial(arrayParser, parse)

  return parse

  # var result = data[options.key];

  # if (options.keys) {
  #   options.keys.forEach(function (name) {
  #     result[name] = data[name];
  #   });
  # }
  # return result;

def arrayParser (parse, data):
  extraKeys = {}
  if isinstance(data, tuple):
    data, extraKeys = data
  result = list(filter(isNotFiltered, map(combineParsers(parse, processOutput), data)))
  if len(extraKeys):
    return result, extraKeys
  else:
    return result

def isNotFiltered (val):
  return val != FILTER_CONST

def joinParsers (optionsAr):
  arrayed = None

  (parser, arrayed) = reduce(reduceParser, optionsAr, (lambda x: x, arrayed))
  return parser

# [{'key': 'awesome', 'keys': ['indeed'], 'type': 'pluck'},
#  {'keys': ['indeed'], 'type': 'array'}]

# {'awesome': [{'foo': 'it works foo!'}, {'bar': 'it works bar!'}],
#  'extra': 'still here!',
#  'indeed': 'asdffdsa'}

# [{'foo': 'it works foo!', 'indeed': 'asdffdsa'},
#  {'bar': 'it works bar!', 'indeed': 'asdffdsa'}]


def reduceParser (data, val):
  (memo, arrayed) = data
  curType = None
  if isinstance(val, dict):
    curType = val.get('type')
  else:
    curType = val

  if curType == 'array':
    arrayed = True
    if isinstance(val, dict) and val.get('keys') is not None:
      return (partial(carryKeysIntoArray, val['keys'], memo), arrayed)
    return (memo, arrayed)

  if curType == 'dearray':
    arrayed = False
    return (memo, arrayed)

  if not isinstance(val, dict):
    raise Exception('Instruction must be a dict or either "array" or "dearray"')

  if val.get('array') is None:
    val['array'] = arrayed

  parser = createParser(val)

  return (combineParsers(memo, parser), arrayed)

def combineParsers (memo, parser):
  return partial(parserCombiner, memo, parser)

def parserCombiner (memo, parser, data):
  return parser(memo(data))

# function carryKeysIntoArray (keys, memo) {
#   return function (data) {
#     data = memo(data);
#     data = data.map(function (entry) {
#       keys.forEach(function (key) {
#         entry[key] = data[key];
#       });
#       return entry;
#     });
#     return data;
#   };
# }

def carryKeysIntoArray (keys, memo, data):
  data = memo(data)
  extraKeys = {}
  if isinstance(data, tuple):
    data, extraKeys = data
  data = list(map(partial(carryKeysMapper, keys, data, extraKeys), data))
  return data

def carryKeysMapper (keys, data, extraKeys, entry):
  localExtraKeys = {}
  for key in keys:
    value = None
    if not key.isdigit():
      value = dot_prop.get(extraKeys, key)
    else:
      value = dot_prop.get(data, key)

    if isinstance(entry, list):
      localExtraKeys[key] = value
    else:
      entry[key] = value

  if len(localExtraKeys) > 0:
    return entry, localExtraKeys
  else:
    return entry

def processOutput (data):
  if isinstance(data, tuple):
    return data[0]
  return data
