/**
 * Hello, world. openfaas nodejs
 */
"use strict"

module.exports = (context, callback) => {
    var startTime = Date.now();
    if(context)
        var greeting = context.data
    else 
        var greeting = "stranger"
    var result = 'hello from Nodejs, ' + greeting + '!'
    callback(undefined, {token: result, startTime: startTime});
  }