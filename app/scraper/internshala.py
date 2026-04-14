import time
import os
from dotenv import load_dotenv #type: ignore
import undetected_chromedriver as uc #type: ignore
from selenium.webdriver.common.by import By #type: ignore
from selenium.webdriver.support.ui import WebDriverWait #type: ignore
from selenium.webdriver.support import expected_conditions as EC #type: ignore




load_dotenv()

Email = os.getenv("Internshala_Email")
Password = os.getenv("Internshala_Password")

def get_driver():
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options, version_main=146)
    return driver

def login(driver):
    print("Logging in..")
    driver.get("https://internshala.com/login/student")
    time.sleep(3)

    try:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))           
        )
        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys(Email)
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(Password)
        driver.find_element(By.ID, "login_submit").click()
        time.sleep(4)
        print("Login successful...")
    except Exception as e:
        print(f"Login failed: {e}")


def close_popup(driver):
    try:
        close_btn = WebDriverWait(driver,4).until(
            EC.element_to_be_clickable((By.ID, "close_popup"))
        )
        close_btn.click()
        time.sleep(0.5)
    except:
        pass

def extract_job(card, keyword):
    def safe_text(by, value):
        try:
            return card.find_element(by, value).text.strip()
        except:
            return ""
        
    def safe_attr(by, value, attr):
        try:
            return card.find_element(by, value).get_attribute(attr)
        except:
            return ""
        
    title    = safe_text(By.CLASS_NAME, "job-internship-name")
    company  = safe_text(By.CLASS_NAME, "company-name")
    location = safe_text(By.CLASS_NAME, "locations_details_container")    
    stipend  = safe_text(By.CLASS_NAME, "stipend")
    duration = safe_text(By.CLASS_NAME, "other_detail_item_value")
    link     = safe_attr(By.TAG_NAME, "a", "href")
    url = link if link and link.startswith("http") else "https://internshala.com" + link if link else ""
    if not title or not company:
        return None
    
    return {
        "title": title,
        "company": company,
        "location": location,
        "stipend": stipend,
        "duration": duration,
        "url": url,
        "source": "internshala",
        "keyword": keyword,
    }

def scrape_internshala(keywords=["python", "machine learning", "flask", "ai"], max_pages=2):
    driver = get_driver()
    all_jobs = []

    try:
        for keyword in keywords:
            for page in range(1, max_pages+1):
                url = f"https://internshala.com/internships/{keyword}-internship/page-{page}"
                print(f"Scraping: {url}")
                driver.get(url)

                try:
                    WebDriverWait(driver, 12).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "internship_meta"))
                    )
                except:
                    print(f" No listings on page {page} - skipping")
                    continue
                    
                close_popup(driver)
                time.sleep(1)

                cards = driver.find_elements(By.CLASS_NAME,"internship_meta")
                print(f" Cards found: {len(cards)}")

                for card in cards:
                    job = extract_job(card, keyword)
                    if job:
                        all_jobs.append(job)

                time.sleep(2)

    finally:
        driver.quit()

    return all_jobs
 