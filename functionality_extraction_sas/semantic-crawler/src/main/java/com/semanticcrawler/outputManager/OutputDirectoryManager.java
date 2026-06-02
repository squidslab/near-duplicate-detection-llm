package com.semanticcrawler.outputManager;

import com.semanticcrawler.configuration.SasType;

import java.io.File;

public final class OutputDirectoryManager {

  private OutputDirectoryManager() {
  }

  public static String createOutputDirectory(
      String appName,
      SasType sasType) {

    /*
     * Create application directory
     */
    File appDirectory =
        new File("out/" + appName);

    if (!appDirectory.exists()) {

      appDirectory.mkdirs();
    }

    /*
     * Find next crawl number
     */
    int nextCrawlNumber = 1;

    File[] existingCrawls =
        appDirectory.listFiles();

    if (existingCrawls != null) {

      for (File file : existingCrawls) {

        String name = file.getName();

        if (name.startsWith("crawl-")) {

          try {

            String[] parts =
                name.split("-");

            int crawlNumber =
                Integer.parseInt(parts[1]);

            if (crawlNumber >= nextCrawlNumber) {

              nextCrawlNumber =
                  crawlNumber + 1;
            }

          } catch (Exception ignored) {
          }
        }
      }
    }

    /*
     * Final output directory
     */
    return "out/"
        + appName
        + "/crawl-"
        + nextCrawlNumber
        + "-"
        + sasType.name().toLowerCase();
  }
}