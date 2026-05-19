package com.semanticcrawler.extraction;

import com.crawljax.core.state.StateVertexImpl;
import com.semanticcrawler.comparator.SemanticComparator;
import java.io.FileWriter;
import java.io.IOException;

public class FunctionalityExtractionVertexImpl extends StateVertexImpl {

  private final SemanticComparator semanticComparator;

  public FunctionalityExtractionVertexImpl(
      int id, String url, String name, String dom, String strippedDom) {

    super(id, url, name, dom, strippedDom);

    this.semanticComparator = new SemanticComparator();
  }

  private void logComparison(FunctionalityExtractionVertexImpl other, boolean result) {

    try (FileWriter fw = new FileWriter("state_comparisons.txt", true)) {

      fw.write("=====================================\n");

      fw.write("PURE SEMANTIC COMPARISON\n");

      fw.write("STATE 1 ID: " + this.getId() + "\n");
      fw.write("STATE 1 NAME: " + this.getName() + "\n");
      fw.write("STATE 1 URL: " + this.getUrl() + "\n");

      fw.write("STATE 2 ID: " + other.getId() + "\n");
      fw.write("STATE 2 NAME: " + other.getName() + "\n");
      fw.write("STATE 2 URL: " + other.getUrl() + "\n");

      fw.write("SEMANTIC RESULT: " + result + "\n");

      fw.write("=====================================\n\n");

    } catch (IOException e) {

      e.printStackTrace();
    }
  }

  @Override
  public boolean equals(Object object) {

    if (this == object) {

      return true;
    }

    if (!(object instanceof FunctionalityExtractionVertexImpl)) {

      return false;
    }

    FunctionalityExtractionVertexImpl other = (FunctionalityExtractionVertexImpl) object;

    /*
     * Pure semantic comparison
     */

    System.out.println("Pure semantic comparison invoked");

    boolean semanticResult = semanticComparator.semanticEquivalent(this, other);

    logComparison(other, semanticResult);

    return semanticResult;
  }

  @Override
  public int hashCode() {

    /*
     * Keep stable hash
     */
    return getStrippedDom().hashCode();
  }
}
