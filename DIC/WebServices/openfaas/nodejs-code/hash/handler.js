"use strict"

String.prototype.hashCode = function(){
    if (Array.prototype.reduce){
        return this.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);
    }
    var hash = 0;
    if (this.length === 0) return hash;
    for (var i = 0; i < this.length; i++) {
        var character  = this.charCodeAt(i);
        hash  = ((hash<<5)-hash)+character;
        hash = hash & hash;
    }
    return hash;
}

module.exports = (context, callback) => {
    var startTime = Date.now();
    if(context)
        var token = new String(params.payload).hashCode();
    else 
        var token = "hashtest".hashCode()

    callback(undefined, {token: token, startTime: startTime});
  }