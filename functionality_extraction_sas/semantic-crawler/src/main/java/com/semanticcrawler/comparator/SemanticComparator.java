package com.semanticcrawler.comparator;

import com.semanticcrawler.extraction.FunctionalityExtractionVertexImpl;
import java.io.FileWriter;
import java.io.IOException;
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

  private void logPythonCall(
      FunctionalityExtractionVertexImpl state1,
      FunctionalityExtractionVertexImpl state2,
      int statusCode,
      String prediction) {

    try (FileWriter fw = new FileWriter("python_calls.txt", true)) {

      fw.write("=====================================\n");

      fw.write("PYTHON SEMANTIC CALL\n");

      fw.write("STATE 1 ID: " + state1.getId() + "\n");
      fw.write("STATE 1 NAME: " + state1.getName() + "\n");
      fw.write("STATE 1 URL: " + state1.getUrl() + "\n");

      fw.write("STATE 2 ID: " + state2.getId() + "\n");
      fw.write("STATE 2 NAME: " + state2.getName() + "\n");
      fw.write("STATE 2 URL: " + state2.getUrl() + "\n");

      fw.write("DOM1 LENGTH: " + state1.getDom().length() + "\n");
      fw.write("DOM2 LENGTH: " + state2.getDom().length() + "\n");

      fw.write("HTTP STATUS: " + statusCode + "\n");

      fw.write("PREDICTION: " + prediction + "\n");

      fw.write("=====================================\n\n");

    } catch (IOException e) {

      e.printStackTrace();
    }
  }

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
      String response =
          new String(connection.getInputStream().readAllBytes(), StandardCharsets.UTF_8);

      System.out.println("Python response: " + response);

      JSONObject responseJson = new JSONObject(response);

      String classification = responseJson.getString("prediction");

      logPythonCall(state1, state2, statusCode, classification);

      return classification.equals("CLONE");

    } catch (Exception e) {

      System.out.println("Error during semantic comparison");

      e.printStackTrace();

      return false;
    }
  }
}
