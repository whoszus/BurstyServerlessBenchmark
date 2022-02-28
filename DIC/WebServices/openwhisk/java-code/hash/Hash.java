import com.google.gson.JsonObject;
import java.util.Calendar;

public class Hash {
    public static JsonObject main(JsonObject args) {
        long startTime = Calendar.getInstance().getTimeInMillis();
        JsonObject response= new JsonObject();
        
        String hash1 = "hashtest";
        if (args.has("param"))
            hash1 = args.getAsJsonPrimitive("param").getAsString();
        int token = hash1.hashCode();
        response.addProperty("token", token);
        response.addProperty("startTime",startTime);
        return response;
    }
}