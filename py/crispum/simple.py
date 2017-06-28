from obstruction import Obstruct
import six

def simpleParser (options, data):
  obsOpts = {}
  if isinstance(data, dict):
    for key in six.iterkeys(data):
      obsOpts[key] = True
  for key,value in six.iteritems(options['keys']):
    if value is False:
      obsOpts.pop(key, None)
    else:
      obsOpts[key] = value

    if isinstance(value, six.string_types) and obsOpts.get(value) is True and not options['keys'].get(value) is True:
      obsOpts.pop(value, None)

  return Obstruct(obsOpts, data)
