package io.kubeless;

import io.kubeless.Event;
import io.kubeless.Context;
import com.google.gson.JsonObject;
import java.util.Calendar;

public class Hash {
    public String foo(io.kubeless.Event event, io.kubeless.Context context) {
        long startTime = Calendar.getInstance().getTimeInMillis();
        
        String hash1 = "hashtest";
        int token = hash1.hashCode();

        JsonObject response= new JsonObject();
        response.addProperty("token", token);
        response.addProperty("startTime",startTime);
        return response.toString();
    }
}