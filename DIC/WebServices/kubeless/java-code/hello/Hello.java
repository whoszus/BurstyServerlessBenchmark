package io.kubeless;

import io.kubeless.Event;
import io.kubeless.Context;
import java.util.Calendar;
import com.google.gson.JsonObject;

public class Hello {
    public String foo(io.kubeless.Event event, io.kubeless.Context context) {
        long startTime = Calendar.getInstance().getTimeInMillis();
        String name = "stranger";

        //String greeting = "Hello " + name + "!";
        JsonObject response = new JsonObject();
        response.addProperty("greeting", "Hello " + name + "!");
        response.addProperty("startTime",startTime);
        return response.toString();
    }
}
