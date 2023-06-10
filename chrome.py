from selenium import webdriver
from anticaptchaofficial.recaptchav2enterpriseproxyless import *
from twocaptcha import TwoCaptcha
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse, parse_qs
#from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pandas as pd
import time
import requests
from webdriver_manager.chrome import ChromeDriverManager

TARGET_URLs = ["https://www.portalinmobiliario.com/arriendo/departamento/particular/las-condes-metropolitana", "https://www.portalinmobiliario.com/arriendo/departamento/particular/nunoa-metropolitana", "https://www.portalinmobiliario.com/arriendo/departamento/particular/providencia-metropolitana"]
LOGIN_URL = "https://www.mercadolibre.com/jms/mlc/lgz/msl/login/H4sIAAAAAAAEAzWOQQ7CMBAD_-JzBPcc-Ui0tE4bkZJqsyWgqn9HKeJo2R57Ry5Tegb7rITHyChbNjisWSwWXUIa4bFkONRk_MuhR0RloVEr_N45E8cbY9FOMt0IB9lsDjGXBv9bgkOqgW-jPiWHxvsrsbtRcu2NqcBjNlurv15ba5eFOshYcrorL0M_opxSNSr7tXPocIhSLZjK8IA_WccXNRkjxNwAAAA/user"

api_twocaptcha_key = 'd34b6cea5d999aea03766d376434a179'
api_anticaptcha_key = '3b939cd231a2d6e72d11d611076d82e4'
driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install())
driver.maximize_window()

list_xpath = '//*[@id="root-app"]/div/div[2]/section/ol'
name_publication_path = '//*[@id="header"]/div/div[2]/h1'
priceunit_path = '//*[@id="price"]/div/div/span/span[2]'
price_path = '//*[@id="price"]/div/div/span/span[3]'
sqr_meter_path = '//*[@id="highlighted_specs_res"]/div/div[1]/span'
number_bedroom_path = '//*[@id="highlighted_specs_res"]/div/div[2]/span'
number_bathroom_path = '//*[@id="highlighted_specs_res"]/div/div[3]/span'
address_path = '//*[@id="location"]/div/div[1]/div/p'

parkingdiv_classname = 'ui-vpp-highlighted-specs__key-value__labels__key-value'

description_path = '//*[@id="description"]/div/p'
contact_name_path = '//*[@id="question"]'
phone_btn_path = '//*[@id="grouped_main_actions"]/div/form/div/button'
phone_num_path = '/html/body/app-root/adview-index/div/div[2]/div/div[2]/div/adview-publisher/div/div[1]/adview-publisher-button/adview-phone-button/div/img[2]'
date_publication_path = '//*[@id="header"]/div/p'

contact_recaptcha_iframe_path = '//*[@id="contact-info-recaptcha"]/div/div/iframe'
login_recaptcha_iframe_path = '//*[@id="g-recaptcha"]/div/div/iframe'
submit_btn_xpath = '//*[@id="login_user_form"]/div[2]/button'
whatsapp_btn_xpath = ''

name_publications = []
prices = []
sqr_meters = []
number_bedrooms = []
number_bathrooms = []
addresses = []
parkings = []
descriptions = []
contact_names = []
phone_numbers = []
date_publications = []

def solve_anticaptcha(iframe_xpath, btn_xpath):
    try:
        url = driver.find_element(By.XPATH, iframe_xpath).get_attribute('src')
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        site_key =query_params["k"][0]
        print(site_key)
        
        solver = recaptchaV2EnterpriseProxyless()
        solver.set_verbose(1)
        solver.set_key(api_anticaptcha_key)
        solver.set_website_url(driver.current_url)
        solver.set_website_key(site_key)
        # solver.set_enterprise_payload({"s": "sometoken"})

        # Specify softId to earn 10% commission with your app.
        # Get your softId here: https://anti-captcha.com/clients/tools/devcenter
        solver.set_soft_id(0)

        g_response = solver.solve_and_return_solution()
        if g_response != 0:
            print("g-response: "+ g_response)
        else:
            print("task finished with error "+solver.error_code)

        # Inject the solution into the page and submit the form
        driver.execute_script('document.getElementById("g-recaptcha-response").value = "{}";'.format(g_response))
         
        submit_btn = driver.find_element(By.XPATH, btn_xpath)
        submit_btn.click()
        time.sleep(10)

    except:
        print("recaptcha error")
    

def solve_twocaptcha():                                                             
    #set up the 2captcha solver
    solver = TwoCaptcha(api_twocaptcha_key)

    url = driver.find_element(By.XPATH, '//*[@id="g-recaptcha"]/div/div/iframe').get_attribute('src')
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    site_key =query_params["k"][0]
    
    # Solve the reCAPTCHA challenge using 2captcha
    result = solver.recaptcha(site_key, driver.current_url)
    print(result)
        
    # Inject the solution into the page and submit the form
    driver.execute_script('document.getElementById("g-recaptcha-response").style.display = "block"')
    driver.execute_script('document.getElementById("g-recaptcha-response").value = "{}";'.format(result['code']))
     
    #time.sleep(30)

    submit_btn = driver.find_element(By.XPATH, '//*[@id="login_user_form"]/div[2]/button')
    submit_btn.click()

    #time.sleep(10)

    # Wait for the reCAPTCHA iframe to load
    #WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="g-recaptcha"]/div/div/iframe')))

    #check_btn = driver.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]')
    #check_btn.click()
    #print("check_btn")

    # Switch back to the default content
    #river.switch_to.default_content()
    
    # try:
    #     result = solver.recaptcha(site_key, driver.current_url)
    #     print(result)
        
    #     # Inject the solution into the page and submit the form
    #     driver.execute_script('document.getElementById("g-recaptcha-response").style.display = "block"')
    #     driver.execute_script('document.getElementById("g-recaptcha-response").value = "{}";'.format(result['code']))
    #     time.sleep(10)
    #     print("recaptcha")

    #     submit_btn = driver.find_element(By.XPATH, '//*[@id="login_user_form"]/div[2]/button')
    #     submit_btn.click()
    #     print("submit_btn")

    #     check_btn = driver.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]')
    #     check_btn.click()
    #     print("check_btn")
    # except:
    #     print("Recaptcha Error")

    submit_btn = driver.find_element(By.XPATH, '//*[@id="login_user_form"]/div[2]/button')
    submit_btn.click()

def log_in():
    driver.get(LOGIN_URL)
    time.sleep(10)

    email = "bastian@pluscapitalcl.com"
    password = "2023contodo"

    id_field = driver.find_element(By.ID, 'user_id')
    id_field.send_keys(email)

    submit_btn = driver.find_element(By.XPATH, '//*[@id="login_user_form"]/div[2]/button')
    submit_btn.click()

    time.sleep(50)
    solve_anticaptcha(login_recaptcha_iframe_path, submit_btn_xpath)
    
    submit_btn = driver.find_element(By.XPATH, '//*[@id="login_user_form"]/div[2]/button')
    submit_btn.click()

    time.sleep(10)
    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(password)

    time.sleep(50)
    solve_anticaptcha(login_recaptcha_iframe_path, submit_btn_xpath)

    # login_btn = driver.find_element(By.XPATH, '//*[@id="action-complete"]')
    # login_btn.click()

    time.sleep(30)


def scrape_eachlink(link):
    print(link)
    
    name_publication = ""
    price = ""
    sqr_meter = ""
    number_bedroom = ""
    number_bathroom = ""
    address = ""
    parking = ""
    description = ""
    contact_name = ""
    phone_number = ""
    date_publication = ""
           
    try:
        driver.get(link)
        time.sleep(5)
        
        try:
            name_publication = driver.find_element(By.XPATH, name_publication_path).get_attribute('innerHTML')
        except:
            print("No such name_publication element")
        try:
            price = driver.find_element(By.XPATH, priceunit_path).get_attribute('innerHTML') + driver.find_element(By.XPATH, price_path).get_attribute('innerHTML')
        except:
            print("No such price element")

        try:
            sqr_meter = driver.find_element(By.XPATH, sqr_meter_path).get_attribute('innerHTML')
        except:
            print("No such sqr_meter element")

        try:
            number_bedroom = driver.find_element(By.XPATH, number_bedroom_path).get_attribute('innerHTML')
        except:
            print("No such number_bedroom element")

        try:
            number_bathroom = driver.find_element(By.XPATH, number_bathroom_path).get_attribute('innerHTML')
        except:
            print("No such number_bathroom element")

        try:
            address = driver.find_element(By.XPATH, address_path).get_attribute('innerHTML')
        except:
            print("No such address element")

        try:
            parking_divs = driver.find_elements(By.CLASS_NAME, parkingdiv_classname)
            for i in range(len(parking_divs)):
                parking_div = parking_divs[i]
                parking_name = parking_div.find_elements(By.TAG_NAME, 'span')[0].get_attribute('innerHTML')
                if(parking_name == 'Estacionamientos:'):
                    parking = parking_div.find_elements(By.TAG_NAME, 'span')[1].get_attribute('innerHTML')
                    break

        except:
            print("No such parking element")

        try:
            description = driver.find_element(By.XPATH, description_path).get_attribute('innerHTML')
        except:
            print("No such description element")

        try:
            contact_string = driver.find_element(By.XPATH, contact_name_path).get_attribute('innerHTML')
            strs = contact_string.split(",")
            contact_name = strs[0].replace("Hola ", "")
            
        except:
            print("No such contact_name element")

        try:
            date_publication = driver.find_element(By.XPATH, date_publication_path).get_attribute('innerHTML')
        except:
            print("No such date_publication element")

        try:
            phone_btn = driver.find_element(By.XPATH, phone_btn_path)
            phone_btn.click()
            time.sleep(50)

            solve_anticaptcha(contact_recaptcha_iframe_path, phone_btn_path)
            url = driver.current_url
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            phone_number =query_params["phone"][0]
            print(phone_number)
            time.sleep(50)

        except:
            print("Phone Number Error")
        
        name_publications.append(name_publication)
        prices.append(price)
        sqr_meters.append(sqr_meter)
        number_bedrooms.append(number_bedroom)
        number_bathrooms.append(number_bathroom)
        addresses.append(address)
        parkings.append(parking)
        descriptions.append(description)
        contact_names.append(contact_name)
        phone_numbers.append(phone_number)
        date_publications.append(date_publication)
        
    except:
        print("cannot reach this url")

def get_urls(links_array):
    # Scrape the data from the current page
    list = driver.find_element(By.XPATH, list_xpath)
    lists = list.find_elements(By.XPATH, './li')
    for i in range(len(lists)):
        list_item = lists[i]
        link = list_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
        links_array.append(link)

def scrape_site(url):
    driver.get(url)
    time.sleep(10)
    links_array = []

    get_urls(links_array)
    next_btn = driver.find_element(By.CLASS_NAME, "andes-pagination__button--next").find_element(By.TAG_NAME, 'a')
    while next_btn:
        url = next_btn.get_attribute('href')
        driver.get(url)
        time.sleep(10)
        get_urls(links_array)

        try:
            next_btn = driver.find_element(By.CLASS_NAME, "andes-pagination__button--next").find_element(By.TAG_NAME, 'a')
        except:
            next_btn = None

    
    for j in range(len(links_array)):
        link = links_array[j]
        scrape_eachlink(link)
    
        df = pd.DataFrame({'Name publication': name_publications, 'prices': prices, 'sqr meters': sqr_meters, 'number of bedrooms': number_bedrooms, 'number of bathrooms': number_bathrooms, 'address': addresses, 'parking': parkings,  'contact name': contact_names, 'phone number': phone_numbers, 'date of publication': date_publications})  # Create a DF with the lists

        with pd.ExcelWriter('result.xlsx') as writer:
            df.to_excel(writer, sheet_name='Sheet1')

def main():
    log_in()

    for url in TARGET_URLs:
        driver.get(url)
        scrape_site(url)
        driver.quit()

if __name__ == '__main__':
    main()

