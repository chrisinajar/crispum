from pprint import pprint
# {
#   "type": "conditional",
#   "key": "awesome",
#   "default": {
#     "type": "pluck",
#     "key": "default"
#   },
#   "options": {
#     "indeed": {
#       "type": "pluck",
#       "key": "indeed"
#     },
#     "other": {
#       "type": "pluck",
#       "key": "other"
#     }
#   }

def conditionalParser (options, createParser, data):
  pprint(data)
  keyVal = data.get(options.get('key'))
  default = options.get('default')
  valueOptions = options.get('options')
  schema = valueOptions.get(keyVal)

  if schema is None:
    schema = default

  return createParser(schema)(data)

