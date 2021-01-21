/**
 * Hello, world. kubeless nodejs
 */
module.exports = {
    foo: function (event, context) {
      startTime = Date.now();
      console.log(event);
      if(event.data)
        greeting = event.data
      else 
        greeting = "stranger"
      result = 'hello from Nodejs, ' + greeting + '!'
      return {token: result, startTime: startTime}
      }
  }