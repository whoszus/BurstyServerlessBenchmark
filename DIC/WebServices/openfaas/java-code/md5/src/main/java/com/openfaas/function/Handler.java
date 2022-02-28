package com.openfaas.function;

import com.openfaas.model.IHandler;
import com.openfaas.model.IResponse;
import com.openfaas.model.IRequest;
import com.openfaas.model.Response;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Calendar;
import java.util.Map;
import java.util.HashMap;
import java.security.*;

public class Handler extends com.openfaas.model.AbstractHandler {

    public static String crypt(String str) {
		if (str == null || str.length() == 0) {
			throw new IllegalArgumentException("String to encript cannot be null or zero length");
		}
		StringBuffer hexString = new StringBuffer();
		try {
			MessageDigest md = MessageDigest.getInstance("MD5");
			md.update(str.getBytes());
			byte[] hash = md.digest();
			for (int i = 0; i < hash.length; i++) {
				if ((0xff & hash[i]) < 0x10) {
					hexString.append("0" + Integer.toHexString((0xFF & hash[i])));
				} else {
					hexString.append(Integer.toHexString(0xFF & hash[i]));
				}
			}
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}
		return hexString.toString();
	}

    public IResponse Handle(IRequest req) {
        long startTime = Calendar.getInstance().getTimeInMillis();
        ObjectMapper mapper = new ObjectMapper();
        String txt = "user_name.....";

        String result = crypt(txt);

        Map<String, Object> rlt = new HashMap<>();
        rlt.put("token", result);
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
