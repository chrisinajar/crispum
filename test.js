var test = require('tape');
var Parse = require('./');
var TestData = require('./tests/basic.json');

test('fixture data', function (t) {
  var numberOfTests = 1;
  t.plan(TestData.length * numberOfTests);

  TestData.forEach(function (data) {
    var parser = Parse(data.schema);
    var result = parser(data.input);
    t.deepEqual(result, data.expected);
  });
});
