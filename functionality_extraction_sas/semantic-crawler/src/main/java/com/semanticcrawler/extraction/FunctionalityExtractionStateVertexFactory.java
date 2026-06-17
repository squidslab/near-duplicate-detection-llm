package com.semanticcrawler.extraction;

import com.crawljax.browser.EmbeddedBrowser;
import com.crawljax.core.state.StateVertex;
import com.crawljax.core.state.StateVertexFactory;

public class FunctionalityExtractionStateVertexFactory extends StateVertexFactory {

    @Override
    public StateVertex newStateVertex(
            int id, String url, String name, String dom, String strippedDom, EmbeddedBrowser browser) {

        return new FunctionalityExtractionVertexImpl(id, url, name, dom, strippedDom);
    }

    @Override
    public String toString() {

        return "FUNCTIONALITY_EXTRACTION_SAS";
    }
}
