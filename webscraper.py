

##IMPORTANT##
##make a batch before hand so you dont have to key enter every time
##make sure that csv file is fully closed before starting 



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os


driver = webdriver.Chrome()

def get_descriptions_from_page(sku_list):
    descriptions = []
    

    try:
        # Wait until the table rows are present on the first page
        #10 secs, you should already have the batch created
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.GridRow'))
        )
        print(f"Found {len(rows)} rows on the current page")

        # Loop through each row and extract the descrip
        for row in rows:
            # Look for input elements with data-column="5" (where the description resides)
            input_elements = row.find_elements(By.CSS_SELECTOR, 'input[data-column="5"]')
            

            for input_element in input_elements:
                
                description = input_element.get_attribute('value')
                print(f"Found description: {description}")

                descriptions.append(description)
            
            

                
    except Exception as e:
        print(f"Error scraping page: {e}")
    
    return descriptions

def get_price_data(sku_list):
    prices = []

    rows = WebDriverWait(driver, 10).until(
         EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.GridRow'))
    )

    for row in rows:
        input_elements = row.find_elements(By.CSS_SELECTOR, 'input[data-column="8"]')

        for input_element in input_elements:

            price = input_element.get_attribute('value')
            print(f'Found price: {price}')

            prices.append(price)

    return prices

    



   
url = 'https://kameleoncloud.vestcom.com/BatchRowsGridLite.aspx?id=146577511'
driver.get(url)
    
    
    # you got 60 secs to input login or else it will close
try:
    # 60 SECSSSS
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "batchRowsGrid")) 
    )
    print("Login successful and the table is loaded!")
except Exception as e:
    print(f"Error waiting for login or page load: {e}")
    driver.quit()
    
    
  
#add the list of skus you want before hand and probably save a batch before you run
sku_list = ["96072", "46232", "96031", "96069", "96016", "96014", "46245", "46235", 
    "96063", "46240", "25712", "29010", "45890", "65608", "65615", "65370", 
    "65984", "65600", "6504", "97043", "97045", "97041", "65748", "65506", 
    "61223", "61570", "26262", "8281", "65564", "65567", "26210", "26218", 
    "46478", "46487", "25617", "25611", "25608", "41945", "25616", "66530", 
    "25621", "41956", "66528", "31048", "31045", "31044", "31007", "31006", 
    "46541", "4649", "45249", "96060", "45023", "46482", "46483", "46505", 
    "46484", "46480", "46481"]

sku_to_description = []
get_price = []



while True:
    
    current_page_descriptions = get_descriptions_from_page(sku_list)
    sku_to_description.extend(current_page_descriptions)
    current_page_price = get_price_data(sku_list)
    get_price.extend(current_page_price)

    # load the next table 
    next_page = input("Press 'n' and Enter to continue to the next page, or 'q' to quit: ")

    if next_page.lower() == 'n':
        # before you press enter again, make sure the new table loaded
        print("Please manually click the 'Next' button in the browser, then press Enter here...")
        input()  #just press enter again
    elif next_page.lower() == 'q':
        print("Exiting the pagination loop.")
        break
    else:
        print("Invalid input, exiting...")
        break


    

#make sure you have the file closed, or it will not write or save
with open('sku_descriptions.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["SKU", "Description", "Price"])  # sku is useless, too lazy to fix so deal w it (NVM FIXED)
    for sku, description, price in zip(sku_list, sku_to_description, get_price):
        writer.writerow([sku, description, price])
print(f"The CSV file will be saved in: {os.getcwd()}")


driver.quit()
