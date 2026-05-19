package com.semanticcrawler.extraction;

import com.crawljax.browser.EmbeddedBrowser;
import com.crawljax.core.state.StateVertex;
import com.crawljax.core.state.StateVertexFactory;
import java.io.FileWriter;
import java.io.IOException;

public class FunctionalityExtractionStateVertexFactory extends StateVertexFactory {

  private void logStateCreation(int id, String url, String name, String dom) {

    try (FileWriter fw = new FileWriter("states_created.txt", true)) {

      fw.write("=====================================\n");

      fw.write("NEW STATE CREATED\n");

      fw.write("ID: " + id + "\n");

      fw.write("NAME: " + name + "\n");

      fw.write("URL: " + url + "\n");

      fw.write("DOM LENGTH: " + dom.length() + "\n");

      fw.write("=====================================\n\n");

    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  @Override
  public StateVertex newStateVertex(
      int id, String url, String name, String dom, String strippedDom, EmbeddedBrowser browser) {

    logStateCreation(id, url, name, dom);

    return new FunctionalityExtractionVertexImpl(id, url, name, dom, strippedDom);
  }

  @Override
  public String toString() {

    return "FUNCTIONALITY_EXTRACTION_SAS";
  }
}
