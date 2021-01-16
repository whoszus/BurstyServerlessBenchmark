/**
 * Hello, world.
 */
function main(params) {
    startTime = Date.now();
    greeting = 'hello from Nodejs, ' + params.payload + '!'
    console.log(greeting);
    return {token: greeting, startTime: startTime}
}
