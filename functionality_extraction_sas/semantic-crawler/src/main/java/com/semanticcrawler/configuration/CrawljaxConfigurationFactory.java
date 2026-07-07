package com.semanticcrawler.configuration;

import com.crawljax.browser.EmbeddedBrowser.BrowserType;
import com.crawljax.core.configuration.BrowserConfiguration;
import com.crawljax.core.configuration.CrawlRules.FormFillMode;
import com.crawljax.core.configuration.CrawljaxConfiguration;
import com.crawljax.core.configuration.CrawljaxConfiguration.CrawljaxConfigurationBuilder;
import com.crawljax.plugins.crawloverview.CrawlOverview;
import com.crawljax.plugins.testcasegenerator.TestConfiguration;
import com.crawljax.plugins.testcasegenerator.TestConfiguration.StateEquivalenceAssertionMode;
import com.crawljax.plugins.testcasegenerator.TestSuiteGenerator;
import com.crawljax.stateabstractions.visual.imagehashes.DHashStateVertexFactory;
import com.semanticcrawler.extraction.FunctionalityExtractionStateVertexFactory;
import com.semanticcrawler.login.LoginPlugin;
import java.io.File;
import java.util.concurrent.TimeUnit;

public final class CrawljaxConfigurationFactory {

    private static final long WAIT_TIME_AFTER_EVENT = 2000;

    private static final long WAIT_TIME_AFTER_RELOAD = 2000;

    private CrawljaxConfigurationFactory() {}

    public static CrawljaxConfiguration build(CrawlConfig config, String outputDirectory) {

        CrawljaxConfigurationBuilder builder = CrawljaxConfiguration.builderFor(config.getUrl());

        /*
         * Output directory
         */
        builder.setOutputDirectory(new File(outputDirectory));

        /*
         * Register SAS
         */
        switch (config.getSasType()) {
            case FUNCTIONALITY_EXTRACTION:
                builder.setStateVertexFactory(new FunctionalityExtractionStateVertexFactory());

                System.out.println("Functionality extraction SAS registered");

                break;

            case BASIC:
                System.out.println("Using Crawljax default SAS");

                break;

            case DHASH:
                builder.setStateVertexFactory(new DHashStateVertexFactory());

                System.out.println("DHash visual SAS registered");

                break;
        }

        /*
         * Form handling
         */
        builder.crawlRules().setFormFillMode(FormFillMode.RANDOM);

        /*
         * SPA exploration configuration
         */
        builder.crawlRules().crawlHiddenAnchors(true);

        builder.crawlRules().crawlFrames(false);

        builder.crawlRules().clickElementsInRandomOrder(false);

        /*
         * Click default elements
         */
        builder.crawlRules().clickDefaultElements();

        /*
         * Explicit clickable elements
         */
        builder.crawlRules().click("a");

        builder.crawlRules().click("button");

        builder.crawlRules().click("input");

        builder.crawlRules().click("textarea");

        builder.crawlRules().click("select");

        builder.crawlRules().click("option");

        /*
         * Avoid logout
         */
        builder.crawlRules().dontClick("a").withAttribute("onclick", "document.logout.submit();");

        /*
         * Crawl limits
         */
        builder.setMaximumStates(200);

        builder.setMaximumRunTime(60, TimeUnit.MINUTES); 

        /*
         * Wait configuration
         */
        builder.crawlRules().waitAfterReloadUrl(WAIT_TIME_AFTER_RELOAD, TimeUnit.MILLISECONDS);

        builder.crawlRules().waitAfterEvent(WAIT_TIME_AFTER_EVENT, TimeUnit.MILLISECONDS);

        /*
         * Browser configuration
         */
        builder.setBrowserConfig(new BrowserConfiguration(BrowserType.CHROME, 1));

        /*
         * Login plugin
         */
        builder.addPlugin(new LoginPlugin(config.getUsername(), config.getPassword()));

        /*
         * Other plugins
         */
        builder.addPlugin(new CrawlOverview());

        TestConfiguration testConfiguration;

        switch (config.getSasType()) {
            case FUNCTIONALITY_EXTRACTION:
                testConfiguration = new TestConfiguration(StateEquivalenceAssertionMode.NONE);

                break;

            case BASIC:
                testConfiguration = new TestConfiguration(StateEquivalenceAssertionMode.NONE);

                break;

            case DHASH:
                testConfiguration = new TestConfiguration(StateEquivalenceAssertionMode.NONE);

                break;

            default:
                testConfiguration = new TestConfiguration(StateEquivalenceAssertionMode.NONE);
        }

        builder.addPlugin(new TestSuiteGenerator(testConfiguration));

        return builder.build();
    }
}
