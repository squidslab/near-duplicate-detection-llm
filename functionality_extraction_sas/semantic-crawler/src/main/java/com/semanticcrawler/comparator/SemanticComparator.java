package com.semanticcrawler.comparator;

import com.semanticcrawler.extraction.FunctionalityExtractionVertexImpl;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import org.json.JSONObject;

public class SemanticComparator {

    /*
     * Python FastAPI endpoint
     */
    private static final String API_URL = "http://localhost:8000/compare";

    /*
     * Semantic comparison via Python
     */
    public boolean semanticEquivalent(
            FunctionalityExtractionVertexImpl state1, FunctionalityExtractionVertexImpl state2) {

        try {

            System.out.println("Sending HTTP request to Python");

            /*
             * Create JSON request body
             */
            JSONObject json = new JSONObject();

            json.put("dom1", state1.getDom());

            json.put("dom2", state2.getDom());

            /*
             * Open HTTP connection
             */
            URL url = new URL(API_URL);

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("POST");

            connection.setRequestProperty("Content-Type", "application/json");

            connection.setDoOutput(true);

            /*
             * Timeout configuration
             */
            connection.setConnectTimeout(10000);

            connection.setReadTimeout(60000);

            /*
             * Send JSON body
             */
            try (OutputStream os = connection.getOutputStream()) {

                byte[] input = json.toString().getBytes(StandardCharsets.UTF_8);

                os.write(input, 0, input.length);
            }

            /*
             * HTTP status code
             */
            int statusCode = connection.getResponseCode();

            System.out.println("HTTP status: " + statusCode);

            /*
             * Read response
             */
            String response = new String(connection.getInputStream().readAllBytes(), StandardCharsets.UTF_8);

            System.out.println("Python response: " + response);

            JSONObject responseJson = new JSONObject(response);

            String classification = responseJson.getString("prediction");

            return classification.equals("CLONE");

        } catch (Exception e) {

            System.out.println("Error during semantic comparison");

            e.printStackTrace();

            return false;
        }
    }
}
