package com.openfaas.function;

import com.openfaas.model.IHandler;
import com.openfaas.model.IResponse;
import com.openfaas.model.IRequest;
import com.openfaas.model.Response;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Calendar;
import java.util.Map;
import java.util.HashMap;
import java.util.Arrays;

public class Handler extends com.openfaas.model.AbstractHandler {

    public static void sort1(int a[], int low, int hight) {
        int i, j, index;
        if (low > hight) {
            return;
        }
        i = low;
        j = hight;
        index = a[i];
        while (i < j) {
            while (i < j && a[j] >= index)
                j--;
            if (i < j)
                a[i++] = a[j];
            while (i < j && a[i] < index)
                i++;
            if (i < j)
                a[j--] = a[i];
        }
        a[i] = index;
        sort1(a, low, i - 1);
        sort1(a, i + 1, hight);
    }

    public static void quickSort(int a[]) {
        sort1(a, 0, a.length - 1);
    }

    public IResponse Handle(IRequest req) {
        long startTime = Calendar.getInstance().getTimeInMillis();
        ObjectMapper mapper = new ObjectMapper();
        
        String str;
        int[] arr;
        arr = new int[] {3, 6, 8, 10, 1, 2, 1, 4, 5, 6, 7, 8, 2232, 2, 4, 5, 7, 9, 20, 0, 88, 7, 34};
        quickSort(arr);

        Map<String, Object> rlt = new HashMap<>();
        rlt.put("token", Arrays.toString(arr));
        rlt.put("startTime", startTime);
        String rltStr = null;
        try {
            rltStr = mapper.writeValueAsString(rlt);
        } catch (Exception e) {
            e.printStackTrace();
        }

        Response res = new Response();
	    res.setBody(rltStr);

	    return res;
    }
}
