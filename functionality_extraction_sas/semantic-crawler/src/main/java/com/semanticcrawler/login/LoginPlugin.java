package com.semanticcrawler.login;

import com.crawljax.core.CrawlerContext;
import com.crawljax.core.plugin.OnUrlLoadPlugin;
import java.time.Duration;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class LoginPlugin implements OnUrlLoadPlugin {

    private final String username;

    private final String password;

    private boolean loginPerformed = false;

    public LoginPlugin(String username, String password) {

        this.username = username;
        this.password = password;
    }

    private WebElement findUserField(WebDriver driver) {

        String[] selectors = {
            "username", "user", "NewUserName", "Name", "email", "LoginForm[username]", "LoginForm_username"
        };

        for (String selector : selectors) {

            try {
                return driver.findElement(By.name(selector));
            } catch (Exception ignored) {
            }

            try {
                return driver.findElement(By.id(selector));
            } catch (Exception ignored) {
            }
        }

        return null;
    }

    private WebElement findPasswordField(WebDriver driver) {

        String[] selectors = {
            "password", "pass", "NewUserPassword", "Password", "LoginForm[password]", "LoginForm_password"
        };

        for (String selector : selectors) {

            try {
                return driver.findElement(By.name(selector));
            } catch (Exception ignored) {
            }

            try {
                return driver.findElement(By.id(selector));
            } catch (Exception ignored) {
            }
        }

        return null;
    }

    private boolean openLoginPage(WebDriver driver) {

        String[] loginTexts = {"Login", "Log in", "Sign in", "Accedi"};

        for (String text : loginTexts) {

            try {

                driver.findElement(By.partialLinkText(text)).click();

                System.out.println("Login page opened through link: " + text);

                return true;

            } catch (Exception ignored) {
            }

            try {

                driver.findElement(By.xpath("//button[contains(.,'" + text + "')]"))
                        .click();

                System.out.println("Login page opened through button: " + text);

                return true;

            } catch (Exception ignored) {
            }

            try {

                driver.findElement(By.xpath("//input[@type='submit' and contains(@value,'" + text + "')]"))
                        .click();

                System.out.println("Login page opened through submit: " + text);

                return true;

            } catch (Exception ignored) {
            }
        }

        return false;
    }

    private boolean isAuthenticated(WebDriver driver) {

        try {

            String pageText = driver.findElement(By.tagName("body")).getText().toLowerCase();

            System.out.println("Authentication check page text:");

            System.out.println(pageText);

            if (pageText.contains("log off")
                    || pageText.contains("logout")
                    || pageText.contains("sign out")
                    || pageText.contains("administrator")
                    || pageText.contains("admin")
                    || pageText.contains("tu sei")) {

                return true;
            }

            if (pageText.contains("utente sconosciuto") || pageText.contains("unknown user")) {

                return false;
            }

        } catch (Exception ignored) {
        }

        return false;
    }

    @Override
    public void onUrlLoad(CrawlerContext context) {

        try {

            if (loginPerformed || username == null || password == null) {

                return;
            }

            WebDriver driver = context.getBrowser().getWebDriver();

            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

            System.out.println("Current URL before login: " + driver.getCurrentUrl());

            System.out.println("Trying automatic login");

            WebElement userField = findUserField(driver);

            WebElement passwordField = findPasswordField(driver);

            if (userField == null || passwordField == null) {

                System.out.println("Login form not found. Trying to open login page.");

                if (openLoginPage(driver)) {

                    try {

                        wait.until(ExpectedConditions.presenceOfElementLocated(By.tagName("body")));

                        Thread.sleep(2000);

                    } catch (Exception ignored) {
                    }

                    System.out.println("Current URL after login page opening: " + driver.getCurrentUrl());

                    userField = findUserField(driver);

                    passwordField = findPasswordField(driver);
                }
            }

            if (userField == null || passwordField == null) {

                System.out.println("Login form not found");

                return;
            }

            System.out.println("User field found: " + userField.getAttribute("name"));

            System.out.println("Password field found: " + passwordField.getAttribute("name"));

            userField.clear();

            userField.sendKeys(username);

            passwordField.clear();

            passwordField.sendKeys(password);

            System.out.println("Username inserted: " + userField.getAttribute("value"));

            String passwordValue = passwordField.getAttribute("value");

            System.out.println("Password length inserted: " + (passwordValue != null ? passwordValue.length() : 0));

            try {

                WebElement loginForm = driver.findElement(By.id("logon"));

                System.out.println("Submitting form with id=logon");

                loginForm.submit();

            } catch (Exception e) {

                System.out.println("Form submit failed, trying passwordField.submit()");

                try {

                    passwordField.submit();

                } catch (Exception ignored) {

                    System.out.println("Fallback submit failed");
                }
            }

            try {

                wait.until(ExpectedConditions.presenceOfElementLocated(By.tagName("body")));

                Thread.sleep(2000);

            } catch (Exception ignored) {
            }

            System.out.println("Current URL after login: " + driver.getCurrentUrl());

            System.out.println("Page title after login: " + driver.getTitle());

            if (isAuthenticated(driver)) {

                loginPerformed = true;

                System.out.println("Authentication verified successfully");

                System.out.println("Automatic login completed");

            } else {

                System.out.println("Authentication verification failed");

                System.out.println("User is still anonymous");

                return;
            }

        } catch (Exception e) {

            System.out.println("Automatic login failed");

            e.printStackTrace();
        }
    }
}
