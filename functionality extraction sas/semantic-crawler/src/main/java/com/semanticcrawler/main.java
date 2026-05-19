package com.semanticcrawler;

import com.crawljax.browser.EmbeddedBrowser.BrowserType;
import com.crawljax.core.CrawljaxRunner;
import com.crawljax.core.configuration.BrowserConfiguration;
import com.crawljax.core.configuration.CrawlRules.FormFillMode;
import com.crawljax.core.configuration.CrawljaxConfiguration;
import com.crawljax.core.configuration.CrawljaxConfiguration.CrawljaxConfigurationBuilder;
import com.crawljax.core.plugin.OnUrlLoadPlugin;
import com.crawljax.plugins.crawloverview.CrawlOverview;
import com.semanticcrawler.extraction.FunctionalityExtractionStateVertexFactory;
import java.io.IOException;
import java.util.concurrent.TimeUnit;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public final class main {

  private static final long WAIT_TIME_AFTER_EVENT = 500;

  private static final long WAIT_TIME_AFTER_RELOAD = 500;

  private static final String URL = "https://security-crawl-maze.app/";

  public static void main(String[] args) throws IOException {

    System.out.println("Starting semantic crawl");

    CrawljaxConfigurationBuilder builder = CrawljaxConfiguration.builderFor(URL);

    /*
     * Register semantic SAS
     */
    builder.setStateVertexFactory(new FunctionalityExtractionStateVertexFactory());

    System.out.println("Semantic SAS registered");

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
     * useful for Angular / SPA applications
     */
    builder.crawlRules().click("a");

    builder.crawlRules().click("button");

    builder.crawlRules().click("span");

    builder.crawlRules().click("div");

    builder.crawlRules().click("mat-card");

    builder.crawlRules().click("mat-icon");

    builder.crawlRules().click("mat-expansion-panel");

    builder.crawlRules().click("mat-row");

    builder.crawlRules().click("mat-cell");

    builder.crawlRules().click("svg");

    builder.crawlRules().click("mat-button");

    builder.crawlRules().click("mat-list-item");

    builder.crawlRules().click("mat-grid-tile");

    /*
     * Navigation / sidenav
     */
    builder.crawlRules().click("button").withAttribute("aria-label", "Open Sidenav");

    /*
     * Popup / dialog handling
     */
    builder.crawlRules().click("button").withText("Dismiss");

    builder.crawlRules().click("button").withText("Close");

    builder.crawlRules().click("button").withText("Me want it!");

    builder.crawlRules().click("button").withText("Got it");

    /*
     * Form interaction
     */
    builder.crawlRules().click("input");

    builder.crawlRules().click("textarea");

    builder.crawlRules().click("select");

    builder.crawlRules().click("option");

    builder.crawlRules().click("mat-select");

    builder.crawlRules().click("mat-option");

    /*
     * Crawl limits
     */
    builder.setMaximumStates(200);

    // builder.setMaximumDepth(10);

    builder.setMaximumRunTime(90, TimeUnit.MINUTES);

    /*
     * Wait configuration
     */
    builder.crawlRules().waitAfterReloadUrl(WAIT_TIME_AFTER_RELOAD, TimeUnit.MILLISECONDS);

    builder.crawlRules().waitAfterEvent(WAIT_TIME_AFTER_EVENT, TimeUnit.MILLISECONDS);

    /*
     * Browser configuration
     */
    builder.setBrowserConfig(new BrowserConfiguration(BrowserType.CHROME_HEADLESS, 1));

    /*
     * Plugin to close initial overlays/popups
     */
    builder.addPlugin(
        (OnUrlLoadPlugin)
            context -> {
              try {

                WebDriver driver = context.getBrowser().getWebDriver();

                Thread.sleep(3000);

                try {

                  driver.findElement(By.xpath("//button[contains(., 'Dismiss')]")).click();

                  System.out.println("Dismiss popup closed");

                } catch (Exception ignored) {
                }

                try {

                  driver.findElement(By.xpath("//button[contains(., 'Me want it!')]")).click();

                  System.out.println("Welcome popup closed");

                } catch (Exception ignored) {
                }

              } catch (Exception e) {

                System.out.println("Popup handling failed");
              }
            });

    /*
     * Plugins
     */
    builder.addPlugin(new CrawlOverview());

    /*
     * Build Crawljax
     */
    CrawljaxRunner crawljax = new CrawljaxRunner(builder.build());

    System.out.println("Starting Crawljax");

    /*
     * Start crawl
     */
    crawljax.call();

    System.out.println("Crawl completed");
  }
}
