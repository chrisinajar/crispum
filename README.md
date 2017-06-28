# crispum
Cross-language declarative parsing pipeline.

## Installation
Node: `npm i crispum --save`  
Python: `pip install crispum`, or if you're clever `pipenv install crispum`

## Usage
Crispum is designed to take in static JSON schema objects and return back a parser function which will apply all of the transformations listed in the schema object.

Here is an example of a simple [obstruction](https://github.com/bendrucker/obstruction) example.
```json
{
  "type": "simple",
  "keys": {
    "indeed": "awesome"
  }
}
```
This schema would transform the following object...
```json
{
  "awesome": "it works!"
}
```
into
```json
{
  "indeed": "it works!"
}
```

The schema may also be an array of instructions, and can apply instructions to to the whole object or to each element of an array.
```json
[{
  "type": "pluck",
  "key": "indeed"
}, {
  "type": "array"
}, {
  "type": "conditional",
  "key": "foo",
  "default": {
    "type": "filter"
  },
  "options": {
    "bar": {
      "type": "pluck",
      "key": "nested"
    },
    "baz": {
      "type": "pluck",
      "key": "special"
    }
  }
}, {
  "type": "dearray"
}, {
  "type": "simple",
  "keys": {
    "result": "0",
    "extra": "1"
  }
}]
```
This results in a complex multistep schema, which when appled to data like this...
```json
{
  "extra": "oh hey",
  "indeed": [{
    "foo": "bar",
    "nested": "value"
  }, {
    "foo": "boozle",
    "nested": "lost in space"
  }, {
    "foo": "baz",
    "nested": "value",
    "special": "so bazzy"
  }]
}
```
results in...
```json
{
  "result": "value",
  "extra": "so bazzy"
}
```

# API

#### `crispum(schema)` -> `function (data)`
Create a new crispum parser with the options passed. The returned parse method takes one parameter, which is input data, and returns the transformed data.

### schema

*Required*  
Type: `object` or `array`

The schema may either be a single instruction or an array of them. Each instruction must have a `type`, and may optionally contain an `array` field.

When `array` is true, the current data will be reinterpreted as an array and each instruction will execute on the entries instead of the list itself. 


Available types are...

#### array

The array instruction tells the crispum pipeline to run all subsequent instructions as if they had `array: true` set. It also can take in an optional parameters, `keys`

`keys` is a list of keys to copy from the data into each element of the array before continuing on the pipeline

#### conditional

The conditional instruction looks at the value of a specified key and then executes a different instruction based on the value found.

 * `key`: They keyname to check the conditional against
 * `default`: The default instruction if the value found is not in the options list
 * `options`: An associative array of instruction options

#### dearray

Stops an array pipeline and goes back to interpreting the data as a whole instead of each element.

#### filter

This instruction deletes the current data and does ont take any parameters. This is useful in combination with `array` and `conditional`

#### simple

Simple onyl takes 1 other parameter, which is `keys`. Keys should be a valid [obstruction schema](https://github.com/bendrucker/obstruction#schema-definitions). 
The result is the same as the output obstruction would generate, except extra keys not mentioned in the schema are not removed.

#### pluck

The pluck instruction takes a given key and rebases the dataset onto it. It takes in two parameters
 * `key`: The keyname to grab and rebase the current dataset onto
 * `keys`: An array of extra keys to copy from the parent object into the plucked value


# License
MIT
