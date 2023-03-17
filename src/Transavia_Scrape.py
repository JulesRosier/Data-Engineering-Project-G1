from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time as t
import datetime
dict = {}
#from fake_useragent import UserAgent

URL = 'https://www.transavia.com/nl-BE/boek-een-vlucht/uitgebreid-zoeken/zoeken/'
DEPART = "Brussel, België"
ARRIVAL = ["Alicante, Spanje", "Corfu, Griekenland", "Kreta (Heraklion), Griekenland", "Rhodos, Griekenland", "Brindisi, Italië", "Napels, Italië", "Palermo, Italië", "Faro, Portugal", "Ibiza, Spanje", "Malaga, Spanje", "Palma, Spanje", "Tenerife, Spanje"]
CODEARRIVAL = ["ALC", "CFU", "HER", "RHO", "BDS", "NAP", "PMO", "FAO", "IBZ", "AGP", "PMI", "TFS"]
MAAND = ["april 2023", "mei 2023", "juni 2023", "juli 2023", "augustus 2023", "september 2023", "oktober 2023"]

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument("--start-maximized")

    webdriver_service = Service("../chromedriver.exe") ## path to where you saved chromedriver binary
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    return driver

def get_data():

    #2: get data
    driver = get_driver()
    actions = ActionChains(driver)
    driver.get(URL)

    t.sleep(5)
    wait = WebDriverWait(driver, 10)

    #2.1 uitgebreid zoeken: accepteer cookies
    try:
        cookies = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='cb__button cb__button--accept-all']")))
        cookies.click()
    except:
        pass
    #reload voor captcha
    t.sleep(20)
    # #2.2 voer in: vanaf Brussel, België
    
    inputDepartElement = driver.find_element(By.ID, "countryStationSelection_Origin-input")
    t.sleep(4)
    inputDepartElement.clear()
    t.sleep(6)
    inputDepartElement.send_keys(DEPART)
    #inputElement.send_keys(Keys.ENTER) #enter simuleren

    #2.3 voer in: naar bestemming, vb Alicante, Spanje --> niet meer nodig, check komt later obv div
    t.sleep(10)
    inputArriveElement = driver.find_element(By.ID, "countryStationSelection_Destination-input")
    t.sleep(6)
    # for i in range(ARRIVAL):
    #     inputArriveElement.send_keys(ARRIVAL[i])

    
    # s = Select(driver.find_element(By.XPATH, "//*[@id='countryStationSelection_Destination']"))
    # t.sleep(3)
    # bestemmingen = [x.text for x in s.options]
    # t.sleep(3)
    # print(bestemmingen)
    # t.sleep(50)

    #klik op meerdere bestemmingen
    # meerdereBestemmingen = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/div/div/form/div[2]/div[2]/div/div[2]/div/button')))
    # meerdereBestemmingen.click()

    # for bestemming in ARRIVAL[1:]:
    #     inputArriveElement = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/div/div/form/div[2]/div[2]/div/div[2]/div/button')
    #     t.sleep(3)
    #     inputArriveElement.send_keys(bestemming)
    #     meerdereBestemmingen = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='link no-underline']")))
    #     meerdereBestemmingen.click()
    

    #2.4 klik op "weet je al wanneer je wil vertrekken?"
    t.sleep(3)
    dropdown = driver.find_element(By.XPATH, '//*[@id="alternativesearch"]/div[4]/div[1]/div[2]')
    dropdown.click() 

    #2.5 klik op "enkele vlucht"

    t.sleep(5.5)
    selectEnkeleVlucht = Select(driver.find_element(By.ID, "data-flight-type"))
    selectEnkeleVlucht.select_by_visible_text('Enkele vlucht')

    #2.6 kies maand
    # t.sleep(4)
    # selectMaand = Select(driver.find_element(By.ID, "timeFrameSelection_SingleFlight_SpecificMonth"))
    # selectMaand.select_by_visible_text(MAAND)


    #2.7 klik op zoeken
    #zoek per maand en per arrival
    #Probleem captcha: zoeken geeft geen data indien geen captcha gedaan, oplossen
    for maand in MAAND:
        t.sleep(3)
        selectMaand = Select(driver.find_element(By.ID, "timeFrameSelection_SingleFlight_SpecificMonth"))
        selectMaand.select_by_visible_text(maand)
        for dest in ARRIVAL:
            t.sleep(3)
            inputArriveElement.send_keys(dest)
            try:
                knopZoeken = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button button-primary']")))
                knopZoeken.click()
            
            

    #2.8 check of bestemming in available bestemmingen ligt. zo ja, klik op toon resultaten

    #2.8.1 check of div ID juist is --> Alicante = <div id="ALC"
                t.sleep(3)
                index = ARRIVAL.index(dest)
                code = CODEARRIVAL[index]
                knopResultaten = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="{}"]/button[1]'.format(code))))
                knopResultaten.click()
                t.sleep(3)
            

    #2.9 klik op iedere kaart, haal datum, vertrek en prijs op
    
    #code om op iedere kaart te klikken, blijkt niet nodig omdat data al in html staat
    # divs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='toggle-button-level-2']")))
    # for div in divs:
    #     div.click()
    #     t.sleep(3)
            #dict: key per maand, values per datum en prijs
                for datum in driver.find_elements(By.XPATH, ".//span[@class='is-hidden is-visible-inline-block--bp20']"):
                    print(datum.text)

                for prijs in driver.find_elements(By.XPATH, ".//div[@class='HV-gu--bp0--x2-2 HV-gu--bp0--50p text-align-right']//span[@class='integer']"):
                    print(prijs.text)
            except:
                pass
            

    
    



    t.sleep(10000)

def call_site():
    driver = get_driver()
    wait = WebDriverWait(driver, 10)
    driver.get(URL)
    t.sleep(50)
    
    #om een of andere reden werkt deze nog niet
    for elem in driver.find_elements(By.CLASS_NAME, "HV-gu--bp0--x2-2 HV-gu--bp0--50p HV-gu--bp20--x2-2"):
        print(elem)

    t.sleep(1000)

def solve_captcha():
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC

    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, executable_path=r'../chromedriver.exe')
    driver.get(URL)
    webbie = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
    wobbie = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()

get_data()