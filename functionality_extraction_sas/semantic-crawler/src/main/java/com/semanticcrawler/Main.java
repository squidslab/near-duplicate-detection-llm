package com.semanticcrawler;

import com.crawljax.core.CrawljaxRunner;
import com.crawljax.core.configuration.CrawljaxConfiguration;

import com.semanticcrawler.configuration.CrawlConfig;
import com.semanticcrawler.configuration.CrawljaxConfigurationFactory;

import com.semanticcrawler.outputManager.OutputDirectoryManager;

import java.io.IOException;

public final class Main {

  private Main() {
  }

  public static void main(String[] args)
      throws IOException {

    /*
     * Read command line arguments
     */
    CrawlConfig config =
        CrawlConfig.fromArgs(args);

    /*
     * Create output directory
     */
    String outputDirectory =
        OutputDirectoryManager
            .createOutputDirectory(
                config.getAppName(),
                config.getSasType());

    System.out.println("=================================");

    System.out.println("Starting crawl");

    System.out.println("=================================");

    System.out.println(
        "Application: "
            + config.getAppName());

    System.out.println(
        "SAS: "
            + config.getSasType());

    System.out.println(
        "URL: "
            + config.getUrl());

    System.out.println(
        "Output directory: "
            + outputDirectory);

    if (config.getUsername() != null) {

      System.out.println(
          "Login credentials detected");
    }

    /*
     * Build Crawljax configuration
     */
    CrawljaxConfiguration configuration =
        CrawljaxConfigurationFactory.build(
            config,
            outputDirectory);

    /*
     * Create Crawljax runner
     */
    CrawljaxRunner crawljax =
        new CrawljaxRunner(
            configuration);

    System.out.println(
        "Starting Crawljax");

    /*
     * Start crawl
     */
    crawljax.call();

    System.out.println(
        "Crawl completed");
  }
}