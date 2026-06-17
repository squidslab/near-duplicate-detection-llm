package com.semanticcrawler.configuration;

public class CrawlConfig {

    private final String appName;

    private final SasType sasType;

    private final String url;

    private final String username;

    private final String password;

    public CrawlConfig(String appName, SasType sasType, String url, String username, String password) {

        this.appName = appName;

        this.sasType = sasType;

        this.url = url;

        this.username = username;

        this.password = password;
    }

    public static CrawlConfig fromArgs(String[] args) {

        /*
         * Application name
         */
        String appName = args.length > 0 ? args[0] : "security-crawl-maze";

        /*
         * SAS type
         */
        SasType sasType = SasType.FUNCTIONALITY_EXTRACTION;

        if (args.length > 1) {

            switch (args[1].toLowerCase()) {
                case "basic":
                    sasType = SasType.BASIC;

                    break;

                case "dhash":
                    sasType = SasType.DHASH;

                    break;

                case "functionality_extraction":

                default:
                    sasType = SasType.FUNCTIONALITY_EXTRACTION;

                    break;
            }
        }

        /*
         * URL
         */
        String url = args.length > 2 ? args[2] : "https://security-crawl-maze.app/";

        /*
         * Optional login credentials
         */
        String username = args.length > 3 ? args[3] : null;

        String password = args.length > 4 ? args[4] : null;

        return new CrawlConfig(appName, sasType, url, username, password);
    }

    public String getAppName() {

        return appName;
    }

    public SasType getSasType() {

        return sasType;
    }

    public String getUrl() {

        return url;
    }

    public String getUsername() {

        return username;
    }

    public String getPassword() {

        return password;
    }
}
