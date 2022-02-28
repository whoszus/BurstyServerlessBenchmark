import com.google.gson.JsonObject;
import java.util.Calendar;
import java.security.*;

public class Md5 {
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

    public static JsonObject main(JsonObject args) {
        long startTime = Calendar.getInstance().getTimeInMillis();
        String txt = "user_name.....";
        if (args.has("text"))
            txt = args.getAsJsonPrimitive("text").getAsString();
        
        String result = crypt(txt);
        
        JsonObject response = new JsonObject();
        response.addProperty("token", result);
        response.addProperty("startTime",startTime);
        return response;
    }
 
}