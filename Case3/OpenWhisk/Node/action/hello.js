function main() {
  // var msg = 'you did not tell me who you are.';
  // if (name) {
  //   msg = `hello ${name}!`
  // }
  // return {body: `<html><body><h3>${msg}</h3></body></html>`}
  var d = new Date();
  var startTime = d.getTime();
  var bodyjson =  {"startTime":startTime}
  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: bodyjson
  };

}