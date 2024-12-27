import os
import zipfile
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PROXY_HOST = "in.proxymesh.com"
PROXY_PORT = 31280
PROXY_USER = "anon"

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = f"""
var config = {{
    mode: "fixed_servers",
    rules: {{
        singleProxy: {{
            scheme: "http",
            host: "{PROXY_HOST}",
            port: parseInt({PROXY_PORT})
        }},
        bypassList: ["localhost","127.0.0.1"]
    }}
}};

chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

function callbackFn(details) {{
    return {{
        authCredentials: {{
            username: "{PROXY_USER}",
            password: "{os.environ.get("PROXY_PASSWORD")}"
        }}
    }};
}}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {{urls: ["https://x.com/*"]}},
    ["blocking"]
);
"""

# Function to get the proxy's current IP
def get_proxy_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_address = response.json().get('ip')
        return ip_address
    except requests.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None

def get_chromedriver_with_proxy():
    # Create a temporary directory for the proxy extension
    pluginfile = "proxy_auth_plugin.zip"
    with zipfile.ZipFile(pluginfile, "w") as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(pluginfile)
    
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_chromedriver_without_proxy():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def scrapping_script():

    driver = get_chromedriver_with_proxy()
    # Open Twitter login page
    driver.get("https://x.com/i/flow/login")

    try:
        # Wait until the username field is present and interactable
        username = WebDriverWait(driver,30).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username.send_keys("shirazyousuf1234@gmail.com")
        username.send_keys(Keys.RETURN)

        # Wait until the username input field is present and interactable
        password = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        password.send_keys("Shiraz284237810")
        password.send_keys(Keys.RETURN)

        # Wait until the password input field is present and interactable
        password = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password.send_keys(os.environ.get("X_PASSWORD"))
        password.send_keys(Keys.RETURN)

        # Wait until the homepage is loaded by checking the title
        WebDriverWait(driver, 30).until(EC.title_contains("Home / X"))

        print("Login Successful")

        # Wait until the trending section is visible
        trending_section = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Timeline: Trending now']"))
        )

        # Find trending topics
        trends = trending_section.find_elements(By.XPATH, "./div/div/div/div/div/div[2]/span")

        # Extract top 5 trending topics
        top_trends = [topic.text for topic in trends[:5]]
        
        print(top_trends)

        # Get the current proxy IP address
        proxy_ip = get_proxy_ip()

        return {
            "trends": top_trends,
            "ip_address": proxy_ip
        }

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}

    finally:
        driver.quit()
