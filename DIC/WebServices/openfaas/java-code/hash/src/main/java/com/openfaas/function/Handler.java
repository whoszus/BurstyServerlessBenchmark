package com.openfaas.function;

import com.openfaas.model.IHandler;
import com.openfaas.model.IResponse;
import com.openfaas.model.IRequest;
import com.openfaas.model.Response;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Calendar;
import java.util.Map;
import java.util.HashMap;

public class Handler extends com.openfaas.model.AbstractHandler {

    public IResponse Handle(IRequest req) {
        long startTime = Calendar.getInstance().getTimeInMillis();
        ObjectMapper mapper = new ObjectMapper();

        String hash1 = "hashtest";
        int token = hash1.hashCode();

        Map<String, Object> rlt = new HashMap<>();
        rlt.put("token", token);
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
