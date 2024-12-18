from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')  # For headless stability
options.add_argument('--no-sandbox')  # To avoid certain security issues
options.add_argument('--disable-dev-shm-usage')  # For memory usage optimization
options.add_argument('--disable-notifications')
driver = webdriver.Chrome(options=options)

urls = [
    'https://www.booking.com/searchresults.html?ss=Vancouver&ssne=Vancouver&ssne_untouched=Vancouver&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-575268&dest_type=city&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=London%2C+Greater+London%2C+United+Kingdom&ssne=Vancouver&ssne_untouched=Vancouver&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-2601889&dest_type=city&ac_position=1&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=72198316b7d4061b&ac_meta=GhA3MjE5ODMxNmI3ZDQwNjFiIAEoATICZW46BkxvbmRvbkAASgBQAA%3D%3D&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=Lisbon&ssne=Toronto&ssne_untouched=Toronto&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-2167973&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=c9c2832ecb15080b&ac_meta=GhBjOWMyODMyZWNiMTUwODBiIAAoATICZW46Bkxpc2JvbkAASgBQAA%3D%3D&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=Rio+de+Janeiro%2C+Rio+de+Janeiro+State%2C+Brazil&ssne=Lisbon&ssne_untouched=Lisbon&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-666610&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=168b83435f32077d&ac_meta=GhAxNjhiODM0MzVmMzIwNzdkIAAoATICZW46CXJpbyBkZSBqYUAASgBQAA%3D%3D&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=San+Francisco%2C+California%2C+United+States&ssne=Rio+de+Janeiro&ssne_untouched=Rio+de+Janeiro&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=20015732&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=ccce834d979502a5&ac_meta=GhBjY2NlODM0ZDk3OTUwMmE1IAAoATICZW46DXNhbiBmcmFuY2lzY29AAEoAUAA%3D&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=New+York%2C+New+York%2C+United+States&ssne=New+York&ssne_untouched=New+York&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=20088325&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=2a5483da93850202&ac_meta=GhAyYTU0ODNkYTkzODUwMjAyIAAoATICZW46CE5ldyB5b3JrQABKAFAA&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=Miami%2C+Florida%2C+United+States&ssne=San+Francisco&ssne_untouched=San+Francisco&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=20023181&dest_type=city&ac_position=1&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=e03383573a2600bc&ac_meta=GhBlMDMzODM1NzNhMjYwMGJjIAEoATICZW46BW1pYW1pQABKAFAA&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=Canc%C3%BAn%2C+Quintana+Roo%2C+Mexico&ssne=Miami&ssne_untouched=Miami&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-1655011&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=1a21835f65f00a69&ac_meta=GhAxYTIxODM1ZjY1ZjAwYTY5IAAoATICZW46BmNhbmN1bkAASgBQAA%3D%3D&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=Barcelona%2C+Catalonia%2C+Spain&ssne=Canc%C3%BAn&ssne_untouched=Canc%C3%BAn&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-372490&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=b32a8368a76a06b8&ac_meta=GhBiMzJhODM2OGE3NmEwNmI4IAAoATICZW46CWJhcmNlbG9uYUAASgBQAA%3D%3D&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=Rome%2C+Lazio%2C+Italy&ssne=Barcelona&ssne_untouched=Barcelona&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-126693&dest_type=city&ac_position=1&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=9ba6837074390672&ac_meta=GhA5YmE2ODM3MDc0MzkwNjcyIAEoATICZW46BHJvbWVAAEoAUAA%3D&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=Paris%2C+Ile+de+France%2C+France&ssne=Rome&ssne_untouched=Rome&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-1456928&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=6b06837dc01f0a81&ac_meta=GhA2YjA2ODM3ZGMwMWYwYTgxIAAoATICZW46BXBhcmlzQABKAFAA&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=Hong+Kong%2C+Hong+Kong&ssne=Paris&ssne_untouched=Paris&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-1353149&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=f0df8385b41c0038&ac_meta=GhBmMGRmODM4NWI0MWMwMDM4IAAoATICZW46CWhvbmcga29uZ0AASgBQAA%3D%3D&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=Tokyo%2C+Tokyo-to%2C+Japan&ssne=Hong+Kong&ssne_untouched=Hong+Kong&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-246227&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=916b838dbbe102a8&ac_meta=GhA5MTZiODM4ZGJiZTEwMmE4IAAoATICZW46BnRva3lvIEAASgBQAA%3D%3D&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=Istanbul%2C+Marmara+Region%2C+Turkey&ssne=Tokyo&ssne_untouched=Tokyo&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-755070&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=4e6f839459d005b2&ac_meta=GhA0ZTZmODM5NDU5ZDAwNWIyIAAoATICZW46CGlzdGFuYnVsQABKAFAA&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=Dubai%2C+Dubai+Emirate%2C+United+Arab+Emirates&ssne=Istanbul&ssne_untouched=Istanbul&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-782831&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=eaf083a7b7e0001b&ac_meta=GhBlYWYwODNhN2I3ZTAwMDFiIAAoATICZW46BWR1YmFpQABKAFAA&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0',
    'https://www.booking.com/searchresults.html?ss=Bangkok%2C+Bangkok+Province%2C+Thailand&ssne=Dubai&ssne_untouched=Dubai&label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AtKn97gGwAIB0gIkZTIwMTkzYTQtYThkOC00NzI2LTk0MmQtNWJhMDFkZTYxYTEx2AIF4AIB&sid=05e4d987755a15f0db5469ac1111a57a&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-3414440&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=d4b283bb83a50294&ac_meta=GhBkNGIyODNiYjgzYTUwMjk0IAAoATICZW46B2Jhbmdrb2tAAEoAUAA%3D&checkin=2024-11-02&checkout=2024-11-03&group_adults=2&no_rooms=1&group_children=0'

]    

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

hotels_dataset = []

for url in urls:
    driver = webdriver.Chrome()
    driver.get(url)

    # response  = requests.get(url, headers=headers)
    # if response.status_code == 200:
    #     print("received response of hotels")

    # soup = BeautifulSoup(response.text, 'html.parser')
    # try:
    # # Replace with the correct selector for the popup close button
    #     time.sleep(7)
    #     driver.execute_script("document.querySelector('.b9720ed41e.cdf0a9297c').remove();")
    #     # close_button = WebDriverWait(driver, 10).until(
    #     #     EC.element_to_be_clickable((By.CSS_SELECTOR, "div.b9720ed41e.cdf0a9297c div.eb33ef7c47"))
    #     # )
    #     # close_button.click()
    #     # button = driver.find_element(By.CSS_SELECTOR, "button.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.f4552b6561")
    #     # driver.execute_script("arguments[0].scrollIntoView(true);", button)
    #     # time.sleep(1)  # allow time for scrolling
    #     # button.click()
    #     print("Popup closed.")
    # except (NoSuchElementException, TimeoutException):
    #     print("No popup appeared or was not found.")

    driver.refresh()

    try:
        print("Scrolling down to the bottom of the page")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)  # wait for the new results to load

    except Exception as e:
        print("No more results to load.")
        break

    while True:
        try:
            print("clicking 'load more' button")
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.a83ed08757.c21c56c305.bf0537ecb5.f671049264.af7297d90d.c0e0affd09"))
            )
            load_more_button.click()
            time.sleep(2)  # wait for more results to load
        except (NoSuchElementException, ElementClickInterceptedException):
            print("button not clickable")
            break
        except Exception as e:
            print("No more results to load.")
            break

    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    hotels = soup.findAll('a', {'data-testid': 'title-link'})

    for hotel in hotels:
        try:
            time.sleep(5)
            hotel_page_response = requests.get(hotel['href'], headers=headers, timeout=10)
            if hotel_page_response.status_code != 200:
                print("could not get hotel page")
                continue

            # time.sleep(10)

            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, 'hp_address_subtitle'))
            # )

            hotel_page_soup = BeautifulSoup(hotel_page_response.text, 'html.parser')
            
            hotel_name_element = hotel_page_soup.find('h2', {'class': 'pp-header__title'})
            hotel_name = hotel_name_element.text.strip() if hotel_name_element else 'N/A'

            hotel_location_element = hotel_page_soup.find('span', {'class': 'hp_address_subtitle'})
            hotel_location = hotel_location_element.text.strip() if hotel_location_element else 'N/A'
            if hotel_location == "N/A":
                print("location is N/A")

            hotel_rooms_table = hotel_page_soup.find('table', {'id': 'hprt-table'})
            hotel_price_rows = hotel_rooms_table.findAll('tr', {'class': 'js-rt-block-row'})
            hotel_room_prices = []
            room_name = ""
            for row in hotel_price_rows:
                find_room_name = row.find('span', {'class': 'hprt-roomtype-icon-link'})
                
                if find_room_name:
                    room_name = find_room_name.text.strip()

                capacity = len(row.find('div', {'class': 'c-occupancy-icons'}).findAll('i'))
                price = row.find('span', {'class': 'prco-valign-middle-helper'}).text.strip()

                price_listing = {
                    "room_name": room_name,
                    "capacity": capacity,
                    "price": price
                }

                hotel_room_prices.append(price_listing)

            # room_prices_elements = hotel_rooms.findAll('div', {'class': 'bui-price-display__value'})
            # room_prices = "|".join([price.find('span', {'class': 'prco-valign-middle-helper'}).text.strip() for price in room_prices_elements]) if room_prices_elements else 'N/A'
            
            hotel_rating_container = hotel_page_soup.find('div', {'id': 'js--hp-gallery-scorecard'})
            hotel_rating_element = hotel_rating_container.find('div', {'class': 'ac4a7896c7'})
            hotel_rating = hotel_rating_element.text.strip() if hotel_rating_element else 'N/A'

            num_reviews = hotel_page_soup.find('span', {'class': 'a3b8729ab1 f45d8e4c32 d935416c47'}).text.strip()
            
            property_reviews = hotel_page_soup.find('div', {'data-testid': 'PropertyReviewsRegionBlock'}).findAll('span', {'class': 'be887614c2'})
            cleanliness = ""
            staff_rating = ""
            value_for_money = ""
            for property in property_reviews:
                if property.text.strip() == "Cleanliness":
                    cleanliness = property.parent.parent.parent.find('div', {'class': 'ccb65902b2 bdc1ea4a28'}).text.strip()
                    print("GOT CLEANLINESS")
                elif property.text.strip() == "Staff":
                    staff_rating = property.parent.parent.parent.find('div', {'class': 'ccb65902b2 bdc1ea4a28'}).text.strip()
                    print("GOT STAFF")
                elif property.text.strip() == "Value for money":
                    value_for_money = property.parent.parent.parent.find('div', {'class': 'ccb65902b2 bdc1ea4a28'}).text.strip()
                    print("GOT VALUE")

            # print(cleanliness.find('span', string="Cleanliness").parent.parent.parent.find('div', {'id': ':r25:-label'}))
            
            # staff_rating = hotel_page_soup.find('div', {'data-testid': 'PropertyReviewsRegionBlock'}).find('span', string="Staff").parent.parent.parent.find('div', {'id': ':r23:-label'})

            # value_for_money = hotel_page_soup.find('div', {'data-testid': 'PropertyReviewsRegionBlock'}).find('span', string="Value for money").parent.parent.parent.find('div', {'id': ':r27:-label'})
            
            facilities = hotel_page_soup.find('div', {'data-testid': 'property-most-popular-facilities-wrapper'}).find('span')
            swimming_pool = False
            for facility in facilities:
                if facility.text:
                    if "swimming pool" in facility.text.lower():
                        swimming_pool = True

            # name_element = hotel.find('div', {'data-testid': 'title'})
            # name = name_element.text.strip()

            # location_element = hotel.find('span', {'data-testid': 'address'})
            # location = location_element.text.strip()

            # Extract the hotel price
            # price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
            # price = price_element.text.strip()
            
            # Extract the hotel rating
            # rating_element = hotel.find('div', {'class': 'b5cd09854e d10a6220b4'})
            # rating = rating_element.text.strip()
            
            # Append hotes_data with info about hotel
            for price_listing in hotel_room_prices:
                hotels_dataset.append({
                    'Hotel_Name': hotel_name,
                    'Location': hotel_location,
                    'Room_Name': price_listing['room_name'],
                    'Room_Occupancy': price_listing['capacity'],
                    'Room_Price': price_listing['price'],
                    'Rating': hotel_rating,
                    'Num_Reviews': num_reviews,
                    'Cleanliness': cleanliness,
                    'Staff_Quality': staff_rating,
                    'Value_For_Money': value_for_money,
                    'Swimming_Pool?': swimming_pool
                })

        except Exception as e:
            print(e)
            continue

        if len(hotels_dataset) % 10 == 0:
            hotels = pd.DataFrame(hotels_dataset)
            hotels.to_csv('hotels.csv', header=True, index=False)


hotels = pd.DataFrame(hotels_dataset)
hotels.head()

hotels.to_csv('hotels.csv', header=True, index=False)