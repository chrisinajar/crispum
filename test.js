var test = require('tape');
var spok = require('spok');
var Parse = require('./');
var TestData = require('./tests/basic.json');

test('fixture data', function (t) {
  TestData.forEach(function (data) {
    var parser = Parse(data.schema);
    var result = parser(data.input);
    spok(t, result, data.expected);
  });

  t.end();
});
