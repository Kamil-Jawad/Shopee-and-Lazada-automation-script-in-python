import pandas as pd
import numpy as np
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import sys
import platform
import random


def row_design():  # row design function
    print('\n')
    print('***************************************************')
    print('\n')


def get_url():  # get the url from user
    row_design()  # calling function
    print("*** Please control your browser from the terminal do not hit the component of website ***\n")
    url = input('Please enter the link of shopee with selected category :: ')
    return url


url = get_url()  # calling the function


def driver_and_option():
    options = webdriver.ChromeOptions()
    # for not close automatically
    options.add_experimental_option("detach", True)
    options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])  # for skipping the warning
    install_chrome = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=install_chrome, options=options)
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(20)
    time.sleep(3)
    return driver


driver = driver_and_option()  # calling function


def select_language():
    try:
        row_design()  # calling function
        language_selection = int(input(
            "Enter 1 for English, 2 for 简体中文 and 3 for Bahasa Melayu not other then these :: "))
        if language_selection == 1:
            language_english = driver.find_element(
                By.CSS_SELECTOR, "div[class='language-selection__list'] div.language-selection__list-item:nth-child(1) button")
            language_english.click()
        elif language_selection == 2:
            language_简体中文 = driver.find_element(
                By.CSS_SELECTOR, "div[class='language-selection__list'] div.language-selection__list-item:nth-child(2) button")
            language_简体中文.click()
        elif language_selection == 3:
            language_Bahasa_Melayu = driver.find_element(
                By.CSS_SELECTOR, "div[class='language-selection__list'] div.language-selection__list-item:nth-child(3) button")
            language_Bahasa_Melayu.click()
        else:
            row_design()  # calling function
            print("** Invalid choice retry **")
            time.sleep(3)
            sys.exit()
    except NoSuchElementException:
        pass
    # except:
    #     row_design()  # calling function
    #     print("** Invalid choice retry **")
    #     sys.exit()


select_language()  # calling function


def loading_page_content():  # function that Loads the all products on page
    for y in range(1000, 4800, 200):
        driver.execute_script("window.scrollTo(0,"+str(y)+")")
        time.sleep(1)


def top_of_page():  # set back to the start of page
    driver.execute_script("window.scrollTo(0,0)")
    time.sleep(1)


def page_count_fun():
    time.sleep(3)
    main_page_count = driver.find_element(By.XPATH,
                                          '/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[1]/div[2]/div')
    # print(main_page_count.text)
    current_page_count = main_page_count.find_element(
        By.CSS_SELECTOR, 'span[class="shopee-mini-page-controller__current"]').text.replace(' ', '')
    current_page_count = int(current_page_count)-1
    # print(current_page_count)
    total_page_count = main_page_count.find_element(
        By.CSS_SELECTOR, 'span[class="shopee-mini-page-controller__total"]').text.replace(' ', '')
    # print(total_page_count)
    availabe_pages = int(total_page_count)-int(current_page_count)
    # print(availabe_pages)
    row_design()  # calling function
    choice_page_count = input(
        f"{availabe_pages} pages are availabe how many pages do you want to scrape please do not exceeded from limit :: ")
    end_page_count = int(current_page_count)+int(choice_page_count)
    if (int(choice_page_count) > int(availabe_pages)):
        row_design()  # calling function
        print("** Invalid choice retry **")
        time.sleep(3)
        sys.exit()
    return current_page_count, end_page_count


current_page_count, end_page_count = page_count_fun()  # calling function

# dictionary to store product details
prodcut_dict = {'product_source': [],
                'product_discount': [],
                'Promotions': [],
                'product_wholesale': [],
                '_id': [],
                'additional_fields': [],
                'product_avg_rating': [],
                'product_brand': [],
                'Final Category': [],
                'breadcrumb_category': [],
                'breadcrumb_product': [],
                'category_url': [],
                'client_id': [],
                'created_at': [],
                'created_date': [],
                'extra_info': [],
                'media_entity_id': [],
                'media_source': [],
                'product_unit_sold': [],
                'offers': [],
                'product_price_before_discount': [],
                'product_description': [],
                'product_name': [],
                'product_price': [],
                'product_specification': [],
                'product_url': [],
                'propagation': [],
                'shop_location': [],
                'product_stock': [],
                'product_total_reviews': [],
                'type': [],
                'updated_at': [],
                'product_voucher': [],
                'seller_name': [],
                'seller_active': [],
                'seller_products': [],
                'seller_response_rate': [],
                'seller_response_time': [],
                'seller_followers': [],
                'seller_rating': [],
                'seller_joined': [],
                # 'product_shipping': [],
                # 'product_exclusive': [],
                # 'product_ship_return': [],
                # 'product_ship_cost': [],
                # 'product_auth': [],
                }
# reviews_dict to store review level data
reviews_dict = {
    '#': [],
    'ID': [],
    'Product Raw ID': [],
    'Product Name': [],
    'Ecom Site': [],
    'Country/Market': [],
    'Master Brand': [],
    'Sale Price': [],
    'Original Price': [],
    'Availability': [],
    'Discount': [],
    'seller_name': [],
    'seller_rating': [],
    'Has Sold': [],
    'Location': [],
    'Promotions': [],
    'Review Rate ID': [],
    'Rating': [],
    'Review Content': [],
    'Zoned Review Time': [],
    'Sentiment': [],
    'Phrases': [], }

language1 = driver.find_element(
    By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/ul/li[2]/div/div/div/span').text

page_index = 0
comment_row = 100
for _ in np.arange(int(current_page_count), int(end_page_count)):
    page_index = page_index+1
    print('Extrating page {0}'.format(page_index))
    loading_page_content()  # loading_page_content()

    main_div = driver.find_element(By.CSS_SELECTOR,
                                   'div[class="row shopee-search-item-result__items"]')
    time.sleep(1)
    product_cards = main_div.find_elements(By.CSS_SELECTOR,
                                           'div[class="col-xs-2-4 shopee-search-item-result__item"]')

    action = ActionChains(driver)
    # get one product card every time from all product cards
    for i, product_card in enumerate(product_cards):
        time.sleep(2)

        # getting new tab with action chain
        sys1 = platform.system()
        if sys1 == 'Darwin':
            action.key_down(Keys.COMMAND).click(
                product_card).key_up(Keys.COMMAND).perform()  # for mac
        elif sys1 == 'Windows':
            action.key_down(Keys.CONTROL).click(
                product_card).key_up(Keys.CONTROL).perform()  # for windows

        # getting new tab in javascript
        # product_link = product_card.get_attribute(' href')
        # driver.execute_script(
        #     "window.open('"+str(product_link)+"','_blank')")
        try:
            # obtain parent window handle
            p = driver.window_handles[0]
            time.sleep(5)
            driver.implicitly_wait(20)
            # obtain browser tab window
            c = driver.window_handles[1]
            time.sleep(3)
            driver.implicitly_wait(20)
            # switch to tab browser
            driver.switch_to.window(c)
            # print("Page title :")
            # print(driver.title)
            driver.implicitly_wait(5)
            # time.sleep(1)
        except:
            # next_page_count = driver.find_element(
            #     By.CSS_SELECTOR, "button[class='shopee-icon-button shopee-icon-button--right ']")
            # next_page_count.click()
            # time.sleep(5)
            # break
            continue
        # getting product data
        time.sleep(3)
        loading_page_content()  # calling function
        time.sleep(1)
        main_product_description = driver.find_element(
            By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div._3A8xof > div > div.page-product > div.container")  # main div
        # time.sleep(1)
        website_source = 'Shopee'
        media_source = 'shopee_my_products'
        category_url = url
        date_time = datetime.now()
        # date_time1 = pd.Timestamp(date_time)
        y_1 = str(date_time.year)
        m_1 = str(date_time.month)
        d_1 = str(date_time.day)
        h_1 = str(date_time.hour)
        minute = str(date_time.strftime('%M'))
        # print(minute)
        s_1 = str(date_time.second)
        date_time1 = y_1 + ':' + m_1 + ':' + d_1 + ' ' + h_1 + ':' + minute + ':' + s_1
        prodcut_dict['type'].append('product_details')
        prodcut_dict['propagation'].append('filtering')
        prodcut_dict['media_source'].append(media_source)
        prodcut_dict['product_source'].append(website_source)
        prodcut_dict['category_url'].append(category_url)
        prodcut_dict['created_at'].append(date_time1)
        prodcut_dict['created_date'].append(date_time1)
        prodcut_dict['updated_at'].append(date_time1)
        prodcut_dict['Promotions'].append(None)
        prodcut_dict['offers'].append(None)
        # print(date_time1)
        # print(prodcut_dict['updated_at'])
        prodcut_dict['extra_info'].append('{'+'}')
        # print('extra_info : ', prodcut_dict['extra_info'])

        product_url = driver.current_url
        prodcut_dict['product_url'].append(product_url)
        # print('product url : ', prodcut_dict['product_url'])
        try:
            product_url = product_url.split('-i.')
            product_url1 = product_url[1].split('?sp_atk=')
            media_entity_ids = product_url1[0].split('.')
            media1 = str(media_entity_ids[0])
            media2 = str(media_entity_ids[1])
            media_entity_id = str(media1 + '.' + media2 + ',')
            p_id = product_url1[1].replace('-', '')
            prodcut_dict['media_entity_id'].append(media_entity_id)
            prodcut_dict['_id'].append(p_id)
            # print('id ', p_id),
            # print('media_entity_id ', media_entity_id)
            # print(prodcut_dict['media_entity_id'])
        except:
            prodcut_dict['media_entity_id'] = '[]'
            prodcut_dict['_id'] = '[]'
        try:
            avg_rating = main_product_description.find_element(
                By.CSS_SELECTOR, "div[class='_3uBhVI URjL1D']").text  # avg_rating
            # p_avg_rating.append(avg_rating)
            # print(avg_rating)
            prodcut_dict['product_avg_rating'].append(avg_rating)
            if avg_rating is None:
                avg_rating = 'nan'
                prodcut_dict['product_avg_rating'].append(avg_rating)

        except:
            avg_rating = '[]'
            prodcut_dict['product_avg_rating'].append(avg_rating)
        try:
            unit_sold = main_product_description.find_element(
                By.CSS_SELECTOR, "div[class='_3b2Btx']").text  # unit sold
            # print(unit_sold)
            # p_unit_sold.append(unit_sold)
            prodcut_dict['product_unit_sold'].append(unit_sold)
            if unit_sold is None:
                unit_sold = 'nan'
                prodcut_dict['product_unit_sold'].append(unit_sold)
        except:
            unit_sold = '[]'
            prodcut_dict['product_unit_sold'].append(unit_sold)
        try:
            product_name = main_product_description.find_element(
                By.CSS_SELECTOR, "div[class='_3g8My-'] > span").text  # product name
            # print(' product name :', product_name)
            # p_name.append(product_name)
            product_name = product_name.replace('\n', ' ')
            prodcut_dict['product_name'].append(product_name)
            if product_name is None:
                product_name = '[]'
                prodcut_dict['product_name'].append(product_name)
        except:
            product_name = '[]'
            prodcut_dict['product_name'].append(product_name)

        try:
            product_stock = driver.find_element(
                By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div._3A8xof > div > div.page-product > div.container > div.product-briefing.flex.card._1j7uGn > div.flex.flex-auto._3qq4y7 > div > div._7c-I_e > div > div.flex._3qYU_y._6Orsg5 > div > div > div.flex.items-center > div:nth-child(2)").text  # product stock
            # p_stock.append(product_stock)
            # print(product_stock)
            prodcut_dict['product_stock'].append(product_stock)
            if product_stock is None:
                product_stock = 'nan'
                prodcut_dict['product_stock'].append(product_stock)
        except:
            product_stock = '[]'
            prodcut_dict['product_stock'].append(product_stock)
        try:
            total_reviews = main_product_description.find_element(
                By.CSS_SELECTOR, "div[class='_3uBhVI']").text  # product total review
            # p_total_reviews.append(total_reviews)
            # print('total reviews : ', total_reviews)
            prodcut_dict['product_total_reviews'].append(total_reviews)
            if total_reviews is None:
                total_reviews = 'nan'
                prodcut_dict['product_total_reviews'].append(total_reviews)
        except:
            total_reviews = '[]'
            prodcut_dict['product_total_reviews'].append(total_reviews)

        try:
            shop_location = driver.find_element(
                By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div._3A8xof > div > div.page-product > div.container > div.S_agbT > div.page-product__content > div.page-product__content--left > div.product-detail.page-product__detail > div:nth-child(1) > div.Fo12Im > div[class='_1pEVDa']:last-child > div").text  # product shop location
            # print('shop_location : ', shop_location)
            if shop_location is None:
                shop_location = 'nan'
            prodcut_dict['shop_location'].append(shop_location)
        except:
            shop_location = '[]'
            prodcut_dict['shop_location'].append(shop_location)
        # try:
        product_specification = driver.find_elements(
            By.CSS_SELECTOR, '#main > div > div:nth-child(3) > div._3A8xof > div > div.page-product > div.container > div.S_agbT > div.page-product__content > div.page-product__content--left > div.product-detail.page-product__detail > div:nth-child(1) > div.Fo12Im > div[class="_1pEVDa"]')
        specification = []
        for pro_spec in product_specification:
            pro_spec = pro_spec.text
            pro_spec = ':'.join(pro_spec.split("\n", 1))
            pro_spec = pro_spec.replace('\n', ',')
            specification.append(pro_spec)
        prodcut_dict['product_specification'].append(specification)
        # print('specification : ', specification)
        # except:
        #     prodcut_dict['product_specification'].append('[]')
        try:
            product_description = driver.find_element(
                By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div._3A8xof > div > div.page-product > div.container > div.S_agbT > div.page-product__content > div.page-product__content--left > div.product-detail.page-product__detail > div:nth-child(2) > div.Fo12Im > div > span").text  # product description
            # p_description.append(product_description)
            product_description = product_description.replace('\n', ',')
            # print('description : ', product_description)
            prodcut_dict['product_description'].append(product_description)
            if product_description is None:
                product_description = 'nan'
                prodcut_dict['product_description'].append(product_description)
        except:
            product_description = '[]'
            prodcut_dict['product_description'].append(product_description)

        try:
            product_wholesale = main_product_description .find_element(
                By.CSS_SELECTOR, "div[class='flex _3qYU_y'] > div[class='flex'] > div:nth-child(1)").text  # product wholesale
            # p_wholesale.append(product_wholesale)
            # print("product wholesale : ", product_wholesale)
            prodcut_dict['product_wholesale'].append(product_wholesale)
            if product_wholesale is None:
                product_wholesale = 'nan'
                prodcut_dict['product_wholesale'].append(product_wholesale)
        except:
            product_wholesale = '[]'
            # p_wholesale.append(product_wholesale)
            prodcut_dict['product_wholesale'].append(product_wholesale)
            # print("product wholesale : ", product_wholesale)

        try:
            complete_voucher = main_product_description.find_element(
                By.CSS_SELECTOR, "div[class='product-shop-vouchers__list']").text  # complete vouchers
            # p_complete_voucher.append(complete_voucher)
            complete_voucher = complete_voucher.replace('\n', ',')
            # print('vouchers : ', complete_voucher)
            prodcut_dict['product_voucher'].append(complete_voucher)
            if complete_voucher is None:
                complete_voucher = 'nan'
                prodcut_dict['product_voucher'].append(
                    complete_voucher)
        except:
            complete_voucher = '[]'
            # p_complete_voucher.append(complete_voucher)
            prodcut_dict['product_voucher'].append(complete_voucher)

        try:
            variation = main_product_description.find_elements(
                By.CSS_SELECTOR, "div[class='flex _3qYU_y _6Orsg5'] > div[class='flex flex-column'] > div[class='flex items-center']")  # variation
            # p_variation.append(variation)
            var = []
            for v in variation:
                v = v.text
                v = ':'.join(v.split("\n", 1))
                v = v.replace('\n', ',')
                if v is None:
                    v = 'nan'
                var.append(v)
            # print('additional_fields: ', var)
            prodcut_dict['additional_fields'].append(var)
        except:
            var = '[]'
            # p_variation.append(variation)
            prodcut_dict['additional_fields'].append(var)
        # try:
        #     shipping = main_product_description.find_element(
        #         By.CSS_SELECTOR, "div[class='_2pq-2z k2VzJg']").text  # shipping
        #     # p_shipping.append(shipping)
        #     shipping = shipping.replace('\n', ',')
        #     print('shipping : ', shipping)
        #     prodcut_dict['product_shipping'].append(shipping)
        #     if shipping is None:
        #         shipping = 'nan'
        #         prodcut_dict['product_shipping'].append(shipping)
        # except:
        #     shipping = '[]'
        #     # p_shipping.append(shipping)
        #     prodcut_dict['product_shipping'].append(shipping)

        try:
            price_before_discount = main_product_description.find_element(
                By.CSS_SELECTOR, "div[class='_2Csw3W']").text  # price before discount
            # p_price_before_discount.append(price_before_discount)
            # print('product price before discount :', price_before_discount)
            prodcut_dict['product_price_before_discount'].append(
                price_before_discount)
            if price_before_discount is None:
                price_before_discount = 'nan'
                prodcut_dict['product_price_before_discount'].append(
                    price_before_discount)
        except:
            price_before_discount = "[]"
            # p_price_before_discount.append(price_before_discount)
            prodcut_dict['product_price_before_discount'].append(
                price_before_discount)

        try:
            price = main_product_description.find_element(
                By.CSS_SELECTOR, "div[class='_2v0Hgx']").text  # price
            # p_price.append(price)
            prodcut_dict['product_price'].append(price)
            if price is None:
                price = 'nan'
                prodcut_dict['product_price'].append(price)
        except:
            price = "[]"
            # p_price.append(price)
            prodcut_dict['product_price'].append(price)

        try:
            discount = main_product_description.find_element(
                By.CSS_SELECTOR, "div[class='_1kpF5Y']").text  # discount
            # p_discount.append(discount)
            # print(discount)
            prodcut_dict['product_discount'].append(discount)
            if discount is None:
                discount = 'nan'
                prodcut_dict['product_discount'].append(discount)
        except:
            discount = "[]"
            # p_discount.append(discount)
            prodcut_dict['product_discount'].append(discount)

        try:
            breadcrumb = driver.find_elements(
                By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div._3A8xof > div > div.page-product > div.container > div.flex.items-center._3bDXqx.page-product__breadcrumb")  # breadcrumb
            final_category = []
            for i in breadcrumb:
                # print('{} >'.format(i.text))
                i = i.text
                i = i.replace('\n', ',')
                final_category.append(i)
             # p_breadcrumb.append(final_category)
            prodcut_dict['breadcrumb_product'].append(final_category)
            # print('breadcrumb : ', final_category)

        except:
            breadcrumb = '[]'
            prodcut_dict['breadcrumb_product'].append(breadcrumb)
        try:
            for crumb in final_category:
                crumb = crumb.split(',')
                prodcut_dict['breadcrumb_category'].append(crumb[2])
                prodcut_dict['Final Category'].append(crumb[2])
                # print('Final cartegory ', crumb[2])
                client_id = 'shopee_my_'+crumb[1]+'_final_3_url'
                client_id = client_id.replace(' ', '_')
                # print('client_id : ', client_id)
                prodcut_dict['client_id'].append(client_id)
        except:
            prodcut_dict['breadcrumb_category'].append('[]')
            prodcut_dict['Final Category'].append('[]')
            prodcut_dict['client_id'].append('[]')
# ***
#         try:
#             exclusive_product = main_product_description.find_element(
#                 By.CSS_SELECTOR, "div[class='_2PFcsI']").text  # exclusive product
#             # p_exclusive_product.append(exclusive_product)
#             prodcut_dict['product_exclusive'].append(exclusive_product)
#             if exclusive_product is None:
#                 exclusive_product = 'nan'
#                 prodcut_dict['product_exclusive'].append(exclusive_product)
#         except:
#             exclusive_product = '[]'
#             # p_exclusive_product.append(exclusive_product)
#             prodcut_dict['product_exclusive'].append(exclusive_product)

#         try:
#             authentic = main_product_description.find_element(
#                 By.CSS_SELECTOR, "div[class='p3E4Hq flex items-center'] div._1Ztchk:nth-child(1)").text  # product authentication
#             # p_auth.append(authentic)
#             prodcut_dict['product_auth'].append(authentic)
#             if authentic is None:
#                 authentic = 'nan'
#                 prodcut_dict['product_auth'].append(authentic)
#         except:
#             authentic = '[]'
#             # p_auth.append(authentic)
#             prodcut_dict['product_auth'].append(authentic)

#         try:
#             ship_return = main_product_description.find_element(
#                 By.CSS_SELECTOR, "div[class='p3E4Hq flex items-center'] div._1Ztchk:nth-child(2)").text  # ship return
#             # p_ship_return.append(ship_return)
#             prodcut_dict['product_ship_return'].append(ship_return)
#             if ship_return is None:
#                 ship_return = 'nan'
#                 prodcut_dict['product_ship_return'].append(ship_return)
#         except:
#             ship_return = '[]'  # ship return
#             # p_ship_return.append(ship_return)
#             prodcut_dict['product_ship_return'].append(ship_return)
# # ***
#         try:
#             ship_cost = main_product_description.find_element(
#                 By.CSS_SELECTOR, "div[class='p3E4Hq flex items-center'] div._1Ztchk:nth-child(3)").text  # shipping cost
#             # p_ship_cost.append(ship_cost)
#             prodcut_dict['product_ship_cost'].append(ship_cost)
#             if ship_cost is None:
#                 ship_cost = 'nan'
#                 prodcut_dict['product_ship_cost'].append(ship_cost)
#         except:
#             ship_cost = '[]'
#             # p_ship_cost.append(ship_cost)
#             prodcut_dict['product_ship_cost'].append(ship_cost)
        try:
            brand = driver.find_element(
                By.CSS_SELECTOR, "#main > div > div:nth-child(3) > div._3A8xof > div > div.page-product > div.container > div.S_agbT > div.page-product__content > div.page-product__content--left > div.product-detail.page-product__detail > div:nth-child(1) > div.Fo12Im > div:nth-child(2) > a").text  # brand name
            # p_brand.append(brand)
            prodcut_dict['product_brand'].append(brand)
            if brand is None:
                brand = 'nan'
                prodcut_dict['product_brand'].append(brand)
            # print('brand : ', brand)
        except:
            brand = '[]'
            # p_brand.append(brand)
            prodcut_dict['product_brand'].append(brand)
        # seller level data
        try:
            seller_name = main_product_description.find_element(
                By.CSS_SELECTOR, "div[class='_1wVLAc']").text  # seller name
            # s_name.append(seller_name)
            prodcut_dict['seller_name'].append(seller_name)
            if seller_name is None:
                seller_name = 'nan'
                prodcut_dict['seller_name'].append(seller_name)
            # print(seller_name)
        except:
            seller_name = '[]'
            prodcut_dict['seller_name'].append(seller_name)

        try:
            seller_active = main_product_description.find_element(
                By.CSS_SELECTOR, "div[class='WvDg_k']").text  # seller status
            # s_active.append(seller_active)
            prodcut_dict['seller_active'].append(seller_active)
            if seller_active is None:
                seller_active = 'nan'
                prodcut_dict['seller_active'].append(seller_active)
            # print(seller_active)
        except:
            seller_active = 'online'
            # s_active.append(seller_active)
            prodcut_dict['seller_active'].append(seller_active)
        try:
            seller_rating = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/div/span").text  # seller rating
            # s_rating.append(seller_rating)
            prodcut_dict['seller_rating'].append(seller_rating)
            if seller_rating is None:
                seller_rating = 'nan'
                prodcut_dict['seller_rating'].append(seller_rating)
            # print(seller_rating)
        except:
            seller_rating = '[]'
            prodcut_dict['seller_rating'].append(seller_rating)

        try:
            seller_product = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/a/span").text  # seller products
            # s_products.append(seller_product)
            prodcut_dict['seller_products'].append(seller_product)
            # print(seller_product)
            if seller_product is None:
                seller_product = 'nan'
                prodcut_dict['seller_products'].append(seller_product)
        except:
            seller_product = '[]'
            prodcut_dict['seller_products'].append(seller_product)
        try:
            seller_response_rate = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]/span").text  # seller response rate
        # s_response_rate.append(seller_response_rate)
            prodcut_dict['seller_response_rate'].append(seller_response_rate)
            # print(seller_response_rate)
            if seller_response_rate is None:
                seller_response_rate = 'nan'
                prodcut_dict['seller_response_rate'].append(
                    seller_response_rate)
        except:
            seller_response_rate = '[]'
            prodcut_dict['seller_response_rate'].append(seller_response_rate)

        try:
            seller_response_time = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/span").text  # seller response time
            # s_response_time.append(seller_response_time)
            prodcut_dict['seller_response_time'].append(seller_response_time)
            # print(seller_response_time)
            if seller_response_time is None:
                seller_response_time = 'nan'
                prodcut_dict['seller_response_time'].append(
                    seller_response_time)
        except:
            seller_response_time = '[]'
            prodcut_dict['seller_response_time'].append(seller_response_time)

        try:
            seller_joined = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[1]/div[2]/div[3]/div[1]/span").text  # seller joined
            # s_joined.append(seller_joined)
            prodcut_dict['seller_joined'].append(seller_joined)
            # print(seller_joined)
            if seller_joined is None:
                seller_joined = 'nan'
                prodcut_dict['seller_joined'].append(seller_joined)
        except:
            seller_joined = '[]'
            prodcut_dict['seller_joined'].append(seller_joined)
        try:
            seller_followers = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[1]/div[2]/div[3]/div[2]/span").text  # seller followers
            # s_followers.append(seller_followers)
            prodcut_dict['seller_followers'].append(seller_followers)
            # print(seller_followers)
            if seller_followers is None:
                seller_followers = 'nan'
                prodcut_dict['seller_followers'].append(seller_followers)
        except:
            seller_followers = '[]'
            prodcut_dict['seller_followers'].append(seller_followers)

        # ***reviews
        # print(language1)
        id1 = random.randint(10000, 100000)
        p_id = random.randint(1000, 10000)
        time.sleep(10)
        driver.implicitly_wait(20)
        try:
            if (language1 == 'Bahasa Indonesia'):
                total_comment_count = driver.find_element(
                    By.CSS_SELECTOR, 'div[class="product-rating-overview"]')

                string1 = total_comment_count.text
                # print(string1)
                comment_count = string1.split('Dengan Komentar (')
                # print(comment_count[1])
                try:
                    comment_count = comment_count[1].split(')Dengan Media')
                    comment_count = int(comment_count[0])
                    # print('page count  : ', comment_count)
                except:
                    comment_count = comment_count[1].split('RB)Dengan Media')
                    comment_count = comment_count[0].replace(',', '')
                    # print('page count  , : ', comment_count)
                    comment_count = int(comment_count)

            else:
                total_comment_count = driver.find_element(
                    By.CSS_SELECTOR, 'div[class="product-rating-overview"]')
                # print('else')
                string1 = total_comment_count.text
                comment_count = string1.split('With Comments (')
                comment_count = comment_count[1].split(')With Media')
                comment_count = int(comment_count[0])
                # print(comment_count)
            if comment_count == 0:
                print('-> There are no comments for this product')
                time.sleep(3)
                # close browser tab window
                driver.close()
                # switch to parent window
                driver.switch_to.window(p)
                time.sleep(5)
                continue
            elif (comment_count >= 1) and (comment_count <= 11):
                next_comments = 1
                print('-> There are some comments for this product please wait.')
            elif comment_count >= 12:
                next_comments = int(comment_count/6)
                print(
                    f'-> This Product contains {next_comments} pages of comments. Please wait it will take time.')
        except:
            print('-> There are no more comments for this product')
            # print('expected')
            time.sleep(3)
            # close browser tab window
            driver.close()
            # switch to parent window
            driver.switch_to.window(p)
            time.sleep(5)
            continue

        time.sleep(5)
        for _ in range(next_comments):
            time.sleep(2)
            # print('scrape reviews')
            comments = driver.find_elements(
                By.CSS_SELECTOR, 'div[class="shopee-product-rating"] > div[class="shopee-product-rating__main"]')
            # print(len(comments))
            for comment in comments:
                id2 = random.randint(1000000000, 10000000000)
                comment_row = comment_row+1
                reviews_dict['#'].append(comment_row)
                reviews_dict['ID'].append(id1)
                reviews_dict['Product Raw ID'].append(p_id)
                reviews_dict['Product Name'].append(product_name)
                reviews_dict['Ecom Site'].append('Shopee MY')
                reviews_dict['Country/Market'].append('MY')
                reviews_dict['Master Brand'].append(brand)
                reviews_dict['Sale Price'].append(price)
                reviews_dict['Original Price'].append(price_before_discount)
                reviews_dict['Availability'].append(product_stock)
                reviews_dict['Discount'].append(discount)
                reviews_dict['seller_name'].append(seller_name)
                reviews_dict['seller_rating'].append(seller_rating)
                reviews_dict['Has Sold'].append(unit_sold)
                reviews_dict['Location'].append(shop_location)
                reviews_dict['Promotions'].append(None)
                reviews_dict['Review Rate ID'].append(id2)
                reviews_dict['Sentiment'].append(None)

                time.sleep(0.5)
                # try:
                #     customer_name = comment.find_element(
                #         By.CSS_SELECTOR, '.shopee-product-rating__author-name').text
                #     reviews_dict['Author name'].append(customer_name)
                #     # print("customer name :", customer_name)
                # except:
                #     customer_name = '[]'
                #     reviews_dict['Author name'].append(customer_name)
                #     # print("customer name :", customer_name)
                # time.sleep(0.5)
                # try:
                #     variation = comment.find_element(
                #         By.CSS_SELECTOR, '.shopee-product-rating__variation').text
                #     reviews_dict['Variations'].append(variation)
                #     # print("variation :", variation)
                # except:
                #     variation = '[]'
                #     reviews_dict['Variations'].append(variation)
                # print("variation :", variation)
                # time.sleep(0.5)
                try:
                    rate1 = comment.find_elements(
                        By.CSS_SELECTOR, 'div[class="repeat-purchase-con"] > div[class="shopee-product-rating__rating"] > svg[class="shopee-svg-icon icon-rating-solid--active icon-rating-solid"]')
                    rate1 = len(rate1)
                    # print('rating : ', rate1)
                    reviews_dict['Rating'].append(rate1)
                except:
                    reviews_dict['Rating'].append('[]')
                time.sleep(0.5)
                try:
                    content = comment.find_element(
                        By.CSS_SELECTOR, '.shopee-product-rating__content').text
                    content = content.replace('\n', ' ')
                    reviews_dict['Review Content'].append(content)
                    # print("content :", content)
                except:
                    content = '[]'
                    reviews_dict['Review Content'].append(content)
                    # print("content :", content)
                time.sleep(0.5)
                try:
                    tags = comment.find_element(
                        By.CSS_SELECTOR, '.shopee-product-rating__tags').text
                    tags = tags.replace('\n', ',')
                    reviews_dict['Phrases'].append(tags)
                    # print("tags :", tags)
                except:
                    tags = '[]'
                    reviews_dict['Phrases'].append(tags)
                    # print("tags :", tags)
                time.sleep(0.5)
                try:
                    comment_time = comment.find_element(
                        By.CSS_SELECTOR, '.shopee-product-rating__time').text
                    reviews_dict['Zoned Review Time'].append(comment_time)
                    # print("time :", comment_time)
                except:
                    comment_time = '[]'
                    reviews_dict['Zoned Review Time'].append(comment_time)
                    # print("time :", comment_time)
                time.sleep(2)
            #     print(comment.text)
            #     print('::::::')
            # print('**----**')
            comment_row = comment_row
            time.sleep(3)
            comment_page_click = driver.find_element(
                By.CSS_SELECTOR, '#main > div > div:nth-child(3) > div._3A8xof > div > div.page-product > div > div.S_agbT > div.page-product__content > div.page-product__content--left > div:nth-child(2) > div > div.product-ratings__list > div.shopee-page-controller.product-ratings__page-controller > button.shopee-icon-button.shopee-icon-button--right')
            comment_page_click.click()

        time.sleep(3)
        # close browser tab window
        driver.close()
        # switch to parent window
        driver.switch_to.window(p)
        # print("Current page title:")
        # print(driver.title)
        time.sleep(2)
        # print(i)
        # choose = int(input('enter 1 to continue and 2 to stop :: '))
        # if choose == 1:
        #     continue
        # elif choose == 2:
        #     break
    next_page_count = driver.find_element(
        By.CSS_SELECTOR, "button[class='shopee-icon-button shopee-icon-button--right ']")
    next_page_count.click()
    time.sleep(5)


product_dataframe = pd.DataFrame(prodcut_dict)

file_name1 = input(
    "Please enter your file name (product and seller level data) :: ")
time.sleep(1)
product_dataframe.to_csv(file_name1 + '.csv', index=False)
time.sleep(1)
reviews_dataframe = pd.DataFrame(reviews_dict)
file_name2 = input(
    "Please enter your file name (review level data) :: ")
reviews_dataframe.to_csv(file_name2 + '.csv', index=False)
print("data saved Successfully, Program is going to close")
time.sleep(3)
driver.quit()
