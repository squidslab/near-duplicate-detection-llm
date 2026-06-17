package com.semanticcrawler.extraction;

import com.crawljax.core.state.StateVertexImpl;
import com.semanticcrawler.comparator.SemanticComparator;

public class FunctionalityExtractionVertexImpl extends StateVertexImpl {

    private final SemanticComparator semanticComparator;

    public FunctionalityExtractionVertexImpl(int id, String url, String name, String dom, String strippedDom) {

        super(id, url, name, dom, strippedDom);

        this.semanticComparator = new SemanticComparator();
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
