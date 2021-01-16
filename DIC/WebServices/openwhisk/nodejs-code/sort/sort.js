function quickSort(arr){
    if (arr.length <= 1){return arr};
    var pivotIndex = Math.floor(arr.length / 2);
    var pivot = arr.splice(pivotIndex,1)[0];
    var left = [];
    var right = [];
    for (var i = 0; i < arr.length; i++){
        if(arr[i] < pivot) {
            left.push(arr[i]);
        }else{
            right.push(arr[i]);
        }
    }
    return quickSort(left).concat([pivot],quickSort(right));
}

function main(params) {
    startTime = Date.now();
    if(params.payload)
        var arr = params.payload.split(',');
    else
        var arr = [3, 6, 8, 10, 1, 2, 1, 4, 5, 6, 7, 8, 2232, 2, 4, 5, 7, 9, 20, 0, 88, 7, 34]
    var result = quickSort(arr);
    var token = result.toString();
    return {token: token, startTime: startTime}
}