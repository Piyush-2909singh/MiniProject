import java.io.*;
import java.net.*;

public class QueryClient {

public static void main(String[] args) throws Exception {

URL url = new URL("http://127.0.0.1:5000/ask");

HttpURLConnection con = (HttpURLConnection) url.openConnection();

con.setRequestMethod("POST");

con.setDoOutput(true);

String jsonInputString = "{\"query\":\"What is leave policy?\"}";

try(OutputStream os = con.getOutputStream()){

byte[] input = jsonInputString.getBytes("utf-8");

os.write(input,0,input.length);

}

BufferedReader br = new BufferedReader(

new InputStreamReader(con.getInputStream(),"utf-8")

);

StringBuilder response = new StringBuilder();

String responseLine;

while((responseLine = br.readLine()) != null){

response.append(responseLine.trim());

}

System.out.println(response.toString());

}

}