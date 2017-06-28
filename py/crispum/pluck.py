
def pluckParser (options, data):
  result = data.get(options.get('key'))
  extraKeys = {}
  if options.get('keys') is not None:
    for name in options['keys']:
      extraKeys[name] = data[name]

      if isinstance(result, list):
        if name.isdigit():
          result[int(name)] = data[name]
      else:
        result[name] = data[name]

  return result, extraKeys
