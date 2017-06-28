import unittest2
import json
from crispum import crispum
from pprint import pprint

class DotPropsTest(unittest2.TestCase):
  def test_basic(self):
    with open('../tests/basic.json') as data_file:
      data = json.load(data_file)

    for entry in data:
      pprint('testing next set...')
      pprint(entry['schema'])
      pprint(entry['input'])
      pprint(entry['expected'])
      parser = crispum(entry['schema'])
      result = parser(entry['input'])
      pprint(result)
      self.assertEquals(result, entry['expected'], entry.get('comment'))
