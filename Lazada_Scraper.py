import uuid
import pandas as pd
import numpy as np
import time
from datetime import datetime
import re
from re import search
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import platform
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options


def row_design():  # row design function
    print('\n')
    print('***************************************************')
    print('\n')


def get_url():  # get the url from user
    row_design()  # calling function
    print("*** Please control your browser from the terminal do not hit the component of website ***\n")
    url = input(
        'Please enter the link of Lazada Diapering & Potties category  :: ')
    print(url)
    return url


url = get_url()  # calling the function


def driver_and_option():
    # options1 = Options()
    options = webdriver.ChromeOptions()
    # for not close automatically
    options.add_experimental_option("detach", True)
    options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])  # for skipping the warning
    install_chrome = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=install_chrome,
                              options=options)
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(20)
    time.sleep(3)
    return driver


driver = driver_and_option()  # calling function


def loading_page_content():  # function that Loads the all products on page
    for y in range(1000, 1900, 300):
        driver.execute_script("window.scrollTo(0,"+str(y)+")")
        time.sleep(1)


def top_of_page():  # set back to the start of page
    driver.execute_script("window.scrollTo(0,0)")
    time.sleep(1)


def page_count_fun():
    row_design()  # calling function
    page_count = int(input(
        "How many next pages do you want to extract, please do not exceeded from limit :: "))
    return page_count


page_count = page_count_fun()  # calling function
time.sleep(5)
products_main_div = driver.find_element(By.CSS_SELECTOR, "div[class='_17mcb']")
# print(products_main_div.text)

# dictionary to store product level and seller data
prodcut_dict = {'product_source': [],
                '_id': [],
                'avg_rating': [],
                'Brand': [],
                'Final Category': [],
                'breadcrumb(category_level)': [],
                'breadcrumb(product_level)': [],
                'category_url': [],
                'client_id': [],
                'created_at': [],
                'created_date': [],
                'discount_percentage': [],
                'discount_price': [],
                'extra_info': [],
                'flavors': [],
                'media_entity_id': [],
                'media_source': [],
                'no_of_unites_sold': [],
                'product_description': [],
                'product_info(options)': [],
                'product_info(selected)': [],
                'product_name': [],
                'product_price': [],
                'product_specifications(additional_fields)': [],
                'product_url': [],
                'promotions': [],
                'propagation': [],
                'sale_price': [],
                'scent': [],
                'shop_vouchers': [],
                'size': [],
                'SKU': [],
                'total_reviews': [],
                'treats': [],
                'type': [],
                'updated_at': [],
                'variation': [],
                'wholesale': [],
                'Promotion Name': [],
                'Model': [],
                'Diaper Type': [],
                'shelf_expiry': [],
                'Recommended Gender': [],
                'Warranty Type': [],
                'Diaper Pack': [],
                'Delivery Options': [],
                'Sold by': [],
                'Seller ratings': [],
                'Ship On Time': [],
                'Chat Response': [],
                }
#  dictionary to store review level data
review_dict = {
    '#': [],
    'ID': [],
    'Product Raw ID': [],
    'product_name': [],
    'Ecom Site': [],
    'Country/Market': [],
    'Master Brand': [],
    'Sale Price': [],
    'Original Price': [],
    'Availability': [],
    'Discount': [],
    'Seller Name': [],
    'seller_ratings': [],
    'Has Sold': [],
    'Location': [],
    'Promotions': [],
    'Review Rate ID': [],
    'Rating': [],
    'product_rating': [],
    "Review Content": [],
    "Zoned Review Time": [],
    'Sentiment': []
    # "customer_name": [],
}

matched = re.search("page=", url)
is_match = bool(matched)
if (is_match == True):
    # print("yes it is")
    try:
        text = url.split("page=")
        # print(text)
        n = int(text[1])
        next_click = n
    except:
        text = url.split("page=")
        # print(text)
        text = text[1].split('&')
        n = int(text[0])
        next_click = n
else:
    next_click = 1
test = 0
print('Extracting Data...')
for _ in np.arange(page_count):

    loading_page_content()  # loading_page_content()
    time.sleep(2)

    Final_Category = driver.find_element(
        By.CSS_SELECTOR, '#J_breadcrumb > li:nth-child(3)').text

    breadcrumb_category = driver.find_elements(
        By.CSS_SELECTOR, '#J_breadcrumb > li')
    temp1 = []
    for b in breadcrumb_category:
        if b.text is None:
            temp1.append('[]')
        temp1.append(b.text)
    main_div = driver.find_element(By.CSS_SELECTOR,
                                   'div[class="_17mcb"]')

    time.sleep(1)
    product_cards = main_div.find_elements(By.CSS_SELECTOR,
                                           'div[class="Bm3ON"]')

    action = ActionChains(driver)
    # # get one product card every time from all product cards

    for i, product_card in enumerate(product_cards):
        time.sleep(5)

        # getting new tab with cation chain
        sys1 = platform.system()
        if sys1 == 'Darwin':
            action.key_down(Keys.COMMAND).click(
                product_card).key_up(Keys.COMMAND).perform()  # for mac
        elif sys1 == 'Windows':
            action.key_down(Keys.CONTROL).click(
                product_card).key_up(Keys.CONTROL).perform()  # for windows

        try:
            # obtain parent window handle
            p = driver.window_handles[0]
            time.sleep(5)
            driver.implicitly_wait(20)
            # # obtain browser tab window
            c = driver.window_handles[1]
            time.sleep(3)
            driver.implicitly_wait(20)
            # # switch to tab browser
            driver.switch_to.window(c)
            driver.implicitly_wait(5)
        except:
            time.sleep(5)
            continue

    # '''
    # getting product data

        loading_page_content()  # calling function

        main_product_description = driver.find_element(
            By.CSS_SELECTOR, "#block-o3rjJP8Rj1")  # main div

        website_source = 'Lazada'
        prodcut_dict['product_source'].append(website_source)  # source
        id_12 = str(uuid.uuid4())[:28]   # str(uuid.uuid4().fields[-1])[:5]
        id_12 = id_12.replace('-', '')
        prodcut_dict['_id'].append(id_12)  # id
        # print('_id : ', id_12)
        category_url = url
        prodcut_dict['category_url'].append(category_url)  # category url
        prodcut_dict['client_id'].append(
            str('Diapering_Potties_scraping').upper())
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
        prodcut_dict['created_at'].append(date_time1)
        prodcut_dict['created_date'].append(date_time1)
        prodcut_dict['updated_at'].append(date_time1)
        # print('datetime : ', date_time1)
        prodcut_dict['extra_info'].append('{'+'}')
        prodcut_dict['flavors'].append(None)
        media = str(uuid.uuid4().fields[-1])[:10]
        # print('media_entity_id : ', media)
        prodcut_dict['media_entity_id'].append(media)
        prodcut_dict['media_source'] = 'lazada_my_products'
        prodcut_dict['no_of_unites_sold'].append(np.nan)
        product_url = driver.current_url
        prodcut_dict['product_url'].append(product_url)
        prodcut_dict['propagation'].append('filtering')
        prodcut_dict['scent'].append(None)
        prodcut_dict['shop_vouchers'].append(None)
        prodcut_dict['size'].append(None)
        prodcut_dict['treats'].append(None)
        prodcut_dict['type'].append('product_details')
        prodcut_dict['variation'].append(None)
        prodcut_dict['wholesale'].append(None)
        prodcut_dict['Promotion Name'].append(None)
        try:
            prodcut_dict['Final Category'].append(Final_Category)
            if Final_Category is None:
                Final_Category = '[]'
                prodcut_dict['Final Category'].append(Final_Category)
        except:
            Final_Category = '[]'
            prodcut_dict['Final Category'].append(Final_Category)

        try:
            prodcut_dict['breadcrumb(category_level)'].append(temp1)
        except:
            temp1 = '[]'
            prodcut_dict['breadcrumb(category_level)'].append(temp1)
        # J_breadcrumb
        time.sleep(2)
        try:
            breadcrumb_product = driver.find_elements(
                By.CSS_SELECTOR, '#J_breadcrumb > li')
            temp2 = []
            for p1 in breadcrumb_product:
                temp2.append(p1.text)
                if p1.text is None:
                    p1 = '[]'
                    temp2.append(p1)
            prodcut_dict['breadcrumb(product_level)'].append(temp2)
        except:
            p1 = '[]'
            prodcut_dict['breadcrumb(product_level)'].append(p1)

        try:
            product_name = main_product_description.find_element(
                By.CSS_SELECTOR, "div[class='pdp-mod-product-badge-wrapper']").text  # product name
            product_name = product_name.replace('\n', ' ')
            prodcut_dict['product_name'].append(product_name)
            if product_name is None:
                product_name = '[]'
                prodcut_dict['product_name'].append(product_name)
        except:
            product_name = '[]'
            prodcut_dict['product_name'].append(product_name)
        test = test+1
        # print(f' {test} , {product_name}')

        try:
            review_12 = main_product_description.find_element(
                By.CSS_SELECTOR, 'div[class="pdp-review-summary"] > a[class="pdp-link pdp-link_size_s pdp-link_theme_blue pdp-review-summary__link"]').text
            review_12 = review_12.split(' ')
            review123 = review_12[0]
            prodcut_dict['total_reviews'].append(review123)
            # print('total reviews : ', review123)
        except:
            prodcut_dict['total_reviews'].append('[]')

        try:
            price = main_product_description.find_element(
                By.CSS_SELECTOR, "#module_product_price_1 > div > div > span").text  # price
            prodcut_dict['discount_price'].append(price)
            prodcut_dict['sale_price'].append(price)
            if price is None:
                price = '[]'
                prodcut_dict['discount_price'].append(price)
                prodcut_dict['sale_price'].append(price)
        except:
            price = "[]"
            # p_price.append(price)
            prodcut_dict['discount_price'].append(price)
            prodcut_dict['sale_price'].append(price)

        try:
            price_before_discount = main_product_description.find_element(
                By.CSS_SELECTOR, "#module_product_price_1 > div > div > div > span.pdp-price.pdp-price_type_deleted.pdp-price_color_lightgray.pdp-price_size_xs").text  # price before discount
            # print('bfd', price_before_discount)
            prodcut_dict['product_price'].append(
                price_before_discount)
            if price_before_discount is None:
                price_before_discount = '[]'
                prodcut_dict['product_price'].append(
                    price_before_discount)
        except:
            price_before_discount = "[]"
            # p_price_before_discount.append(price_before_discount)
            prodcut_dict['product_price'].append(
                price_before_discount)

        try:
            discount = main_product_description.find_element(
                By.CSS_SELECTOR, "#module_product_price_1 > div > div > div > span.pdp-product-price__discount").text  # discount
            # print('discount', discount)
            prodcut_dict['discount_percentage'].append(discount)
            if discount is None:
                discount = 'nan'
                prodcut_dict['discount_percentage'].append(discount)
        except:
            discount = "[]"
            # p_discount.append(discount)
            prodcut_dict['discount_percentage'].append(discount)

        try:
            promotion = main_product_description.find_element(
                By.CSS_SELECTOR, 'div[id="module_promotion_tags"] > div[class="pdp-mod-product-info-section pdp-mod-promotion-tags"] > div[class="section-content"] > div[data-spm="promotion_bar"]').text
            promotion = promotion.replace('\n', ',')
            prodcut_dict['promotions'].append(promotion)
            # print('promotions : ', promotion)
        except:
            prodcut_dict['promotions'].append('[]')

        time.sleep(1)
        try:
            info1 = main_product_description.find_elements(
                By.CSS_SELECTOR, "div[class='sku-selector'] > div[class='sku-prop']")  # product_info(options)
            info_list = []
            for info_1 in info1:
                info_1 = info_1.text
                info_1 = ':'.join(info_1.split("\n", 1))
                info_1 = info_1.replace('\n', ',')
                info_list.append(info_1)
            prodcut_dict['product_info(options)'].append(info_list)
            # print('product_info(options) : ', info_list)
        except:
            prodcut_dict['product_info(options)'].append('[]')

        try:
            # info_selected = main_product_description.find_elements(
            #     By.CSS_SELECTOR, "div[class='sku-selector'] > div[class='sku-prop'] > div[class='pdp-mod-product-info-section sku-prop-selection'] > div[class='section-content'] > div[class='sku-prop-content'] > span[class='sku-variable-name-selected']")  # product_info(selected)
            info_list1 = []
            for infos in info_list:
                # infos = infos.text
                infos = infos.split(",")
                infos = infos[0]
                info_list1.append(infos)
            prodcut_dict['product_info(selected)'].append(info_list1)
            # print('product_info(selected) : ', info_list1)
        except:
            prodcut_dict['product_info(selected)'].append('[]')

        try:
            Delivery_Options = main_product_description.find_element(
                By.CSS_SELECTOR, "#module_seller_delivery > div > div > div.delivery__content").text  # delivery_option
            Delivery_Options = Delivery_Options.replace('\n', ',')
            # print("delvery o", Delivery_Options)
            prodcut_dict['Delivery Options'].append(Delivery_Options)
            if Delivery_Options is None:
                Delivery_Options = '[]'
                prodcut_dict['Delivery Options'].append(Delivery_Options)
        except:
            Delivery_Options = "[]"
            # p_discount.append(discount)
            prodcut_dict['Delivery Options'].append(Delivery_Options)
        time.sleep(1.5)
        try:
            product_description = driver.find_element(
                By.CSS_SELECTOR, "#module_product_detail > div > div > div > div.html-content.detail-content").text  # product description
            # p_description.append(product_description)
            # print('description', product_description)
            product_description = product_description.replace('\n', ',')
            prodcut_dict['product_description'].append(product_description)
            if product_description is None:
                product_description = '[]'
                prodcut_dict['product_description'].append(
                    product_description)
        except:
            product_description = '[]'
            prodcut_dict['product_description'].append(product_description)

        try:
            Sold_by = driver.find_element(
                By.CSS_SELECTOR, '#module_seller_info > div > div.seller-name-retail > div.seller-name__wrapper > div.seller-name__detail > a.pdp-link.pdp-link_size_l.pdp-link_theme_black.seller-name__detail-name').text  # Sold_by
            # print('sold by', Sold_by)
            prodcut_dict['Sold by'].append(Sold_by)
            if Sold_by is None:
                Sold_by = '[]'
                prodcut_dict['Sold by'].append(Sold_by)
        except:
            Sold_by = '[]'
            prodcut_dict['Sold by'].append(Sold_by)

        try:
            seller_ratings = driver.find_element(
                By.CSS_SELECTOR, '#module_seller_info > div > div.pdp-seller-info-pc > div:nth-child(1) > div.seller-info-value.rating-positive').text  # seller rating
            # print('seller_ratings : ', seller_ratings)
            prodcut_dict['Seller ratings'].append(seller_ratings)
            if seller_ratings is None:
                seller_ratings = '[]'
                prodcut_dict['Seller ratings'].append(seller_ratings)
        except:
            seller_ratings = '[]'
            prodcut_dict['Seller ratings'].append(seller_ratings)

        try:
            Ship_On_Time = driver.find_element(
                By.CSS_SELECTOR, '#module_seller_info > div > div.pdp-seller-info-pc > div:nth-child(2) > div.seller-info-value').text  # Ship_On_Time
            # print('sold by', Ship_On_Time)
            prodcut_dict['Ship On Time'].append(Ship_On_Time)
            if Ship_On_Time is None:
                Ship_On_Time = 'nan'
                prodcut_dict['Ship On Time'].append(Ship_On_Time)
        except:
            Ship_On_Time = '[]'
            prodcut_dict['Ship On Time'].append(Ship_On_Time)

        try:
            Chat_Response = driver.find_element(
                By.CSS_SELECTOR, '#module_seller_info > div > div.pdp-seller-info-pc > div:nth-child(3) > div.seller-info-value').text  # Chat_Response
            # print('Chat_Response ', Chat_Response)
            prodcut_dict['Chat Response'].append(Chat_Response)
            if Chat_Response is None:
                Chat_Response = 'nan'
                prodcut_dict['Chat Response'].append(Chat_Response)
        except:
            Chat_Response = '[]'
            prodcut_dict['Chat Response'].append(Chat_Response)

        try:
            product_rating = driver.find_element(
                By.CSS_SELECTOR, '#module_product_review > div > div > div:nth-child(1) > div.mod-rating > div > div > div.summary > div.score > span.score-average').text  # Chat_Response
            # print('product_rating ', product_rating)
            prodcut_dict['avg_rating'].append(product_rating)
            if product_rating is None:
                product_rating = 'nan'
                prodcut_dict['avg_rating'].append(product_rating)
        except:
            product_rating = '[]'
            prodcut_dict['avg_rating'].append(product_rating)

        time.sleep(0.5)
        try:
            spec_c = driver.find_element(
                By.CSS_SELECTOR, '#module_product_detail > div > div > div.pdp-product-desc > div.pdp-mod-specification > div.pdp-general-features > ul').text
            spec_c = spec_c.replace('\n', ',')
            prodcut_dict['product_specifications(additional_fields)'].append(
                spec_c)
            # print('complete specification : ', spec_c)
        except:
            prodcut_dict['product_specifications(additional_fields)'].append(
                '[]')

        # getting specifications
        web_items = []
        spec_list = ["Brand", "SKU", "Model",
                     "Warranty Type", "Diaper Type", "Recommended Gender", "Diaper Pack", "shelf_expiry"]
        time.sleep(1)
        try:  # this try and its except is for show_more button
            show_more = driver.find_element(
                By.CSS_SELECTOR, 'div[class="expand-button expand-cursor"] > button')
            show_more.click()
            # print('button clicked')
            y = 0
            time.sleep(3)
            t1 = driver.find_elements(
                By.CSS_SELECTOR, 'div[class="pdp-mod-specification"] > div[class="pdp-general-features"] > ul > li > span')
            for i in t1:
                web_items.append(i.text)  # append in list

            for i in range(len(spec_list)):
                for j in range(len(t1)):
                    if spec_list[i] == t1[j].text:
                        y = j+1
                        v1 = driver.find_element(
                            By.CSS_SELECTOR, f'div[class="pdp-mod-specification"] > div[class="pdp-general-features"] > ul > li:nth-child({y}) > div').text
                        prodcut_dict[t1[j].text].append(v1)

            for spec1 in spec_list:
                if spec1 not in web_items:
                    prodcut_dict[spec1].append('[]')
            # print('\n::::::::\n')
        except:  # this execpt is when button is not on the page
            # print('button not clicked')
            time.sleep(0.5)
            y = 0
            t1 = driver.find_elements(
                By.CSS_SELECTOR, 'div[class="pdp-mod-specification"] > div[class="pdp-general-features"] > ul > li > span')
            for i in t1:
                web_items.append(i.text)

            for i in range(len(spec_list)):
                time.sleep(3)
                for j in range(len(t1)):
                    if spec_list[i] == t1[j].text:
                        y = j+1
                        v1 = driver.find_element(
                            By.CSS_SELECTOR, f'div[class="pdp-mod-specification"] > div[class="pdp-general-features"] > ul > li:nth-child({y}) > div').text
                        prodcut_dict[t1[j].text].append(v1)
            for spec1 in spec_list:
                if spec1 not in web_items:
                    prodcut_dict[spec1].append('[]')
            # print('\n::::::::\n')
            pass

    #   '''
   #  ******** reviews *********

        time.sleep(5)
        pro_id1 = str(uuid.uuid4().fields[-1])[:4]
        try:
            review_brand = main_product_description.find_element(
                By.CSS_SELECTOR, 'div[id="module_product_brand_1"] > div[class="pdp-product-brand"] > a[class="pdp-link pdp-link_size_s pdp-link_theme_blue pdp-product-brand__brand-link"]').text
        except:
            review_brand = '[]'
        try:
            av = main_product_description.find_element(
                By.CSS_SELECTOR, '#module_quantity-input > div > div > span').text
        except:
            av = '[]'
        try:
            reviews_main_div = driver.find_element(
                By.CSS_SELECTOR, '#module_product_review > div > div > div:nth-child(3) > div.mod-reviews')
            sum_reviews = int(review123)
            if (sum_reviews < 5):
                print('-> There are no more reviews for this product')
                time.sleep(3)
                # close browser tab window
                driver.close()
                # switch to parent window
                driver.switch_to.window(p)
                time.sleep(5)
                continue

            elif (sum_reviews >= 5):
                next_sum_reviews = int(sum_reviews/5)
                print(
                    '-> Reviews found for this product, Please wait it will take time ')

        except:
            print('-> There are no more reviews for this product')
            time.sleep(3)
            # close browser tab window
            driver.close()
            # switch to parent window
            driver.switch_to.window(p)
            time.sleep(5)
            continue
        time.sleep(3)
        try:
            review_time = reviews_main_div.find_elements(By.CSS_SELECTOR,
                                                         "div[class='item'] > div[class='top'] > span")  # review time
        except:
            print('-> There are no more reviews for this product')
            time.sleep(3)
            # close browser tab window
            driver.close()
            # switch to parent window
            driver.switch_to.window(p)
            time.sleep(5)
            continue

        review_by = reviews_main_div.find_elements(By.CSS_SELECTOR,
                                                   "div[class='item'] > div[class='middle'] > span:nth-child(1)")  # review by
        time.sleep(1)
        comment = reviews_main_div.find_elements(By.CSS_SELECTOR,
                                                 "div[class='item'] > div[class='item-content'] > div:nth-child(1)")  # comment
        for _ in range(next_sum_reviews):
            loading_page_content()  # calling function
            time.sleep(3)
            for i in range(len(review_time)):
                id_no1 = str(uuid.uuid4().fields[-1])[:5]
                review_dict['#'].append(id_no1)
                id3 = str(uuid.uuid4().fields[-1])[:5]
                review_dict['ID'].append(id3)
                review_dict['Product Raw ID'].append(pro_id1)
                review_dict['Ecom Site'].append('Lazada MY')
                review_dict['Country/Market'].append('MY')
                review_dict['Master Brand'].append(review_brand)
                review_dict['Sale Price'].append(price)
                review_dict['Original Price'].append(price_before_discount)
                review_dict['Availability'].append(av)
                review_dict['Discount'].append(discount)
                review_dict['Seller Name'].append(Sold_by)
                review_dict['Has Sold'].append(None)
                review_dict['Location'].append(None)
                review_dict['Promotions'].append(promotion)
                rate_id = str(uuid.uuid4().fields[-1])[:15]
                review_dict['Review Rate ID'].append(rate_id)
                review_dict['Sentiment'].append(None)
                review_dict['product_name'].append(
                    product_name)  # product name
                review_dict['product_rating'].append(
                    product_rating)  # product rating
                review_dict['seller_ratings'].append(seller_ratings)
                reviews_main_div = driver.find_element(
                    By.CSS_SELECTOR, '#module_product_review > div > div > div:nth-child(3) > div.mod-reviews')
                try:
                    customer_rate = reviews_main_div.find_elements(
                        By.CSS_SELECTOR, 'div[class="item"] > div[class="top"] > div[class="container-star starCtn left"]')
                    customer_rate_list = []
                    for _ in customer_rate:
                        customer_rate_list.append(1)
                    review_dict['Rating'].append(len(customer_rate_list))
                    # print('customer rating : ', len(customer_rate_list))
                except:
                    review_dict['Rating'].append('[]')
                try:
                    review_time = reviews_main_div.find_elements(By.CSS_SELECTOR,
                                                                 "div[class='item'] > div[class='top'] > span")  # review time
                    review_time1 = review_time[i].text
                    review_dict['Zoned Review Time'].append(
                        review_time1)  # review time
                    # print('review time :', review_time1)
                except:
                    review_dict['Zoned Review Time'].append('[]')
                # try:
                #     review_by = reviews_main_div.find_elements(By.CSS_SELECTOR,
                #                                                "div[class='item'] > div[class='middle'] > span:nth-child(1)")  # review by
                #     review_by1 = review_by[i].text  # review by
                #     review_by1 = review_by1.replace('by', '')
                #     review_dict['customer_name'].append(review_by1)
                # except:
                #     review_dict['customer_name'].append('[]')

                time.sleep(1)
                try:
                    comment = reviews_main_div.find_elements(By.CSS_SELECTOR,
                                                             "div[class='item'] > div[class='item-content'] > div:nth-child(1)")  # comment

                    comment1 = comment[i].text  # comment
                    comment1 = comment1.replace('\n', '')
                    review_dict['Review Content'].append(comment1)
                    # print('comment : ', comment1)
                except:
                    review_dict['Review Content'].append('[]')
                time.sleep(2)
            try:
                time.sleep(7)
                driver.find_element(By.CSS_SELECTOR, '#nc_1__scale_text')
                break
            except:
                try:
                    time.sleep(5)
                    next_comments = driver.find_element(
                        By.CSS_SELECTOR, 'div[class="next-pagination-pages"] > button[class="next-btn next-btn-normal next-btn-medium next-pagination-item next"]')
                    next_comments.click()
                    continue
                except:
                    time.sleep(7)
                    break

        time.sleep(3)
        # close browser tab window
        driver.close()
        # switch to parent window
        driver.switch_to.window(p)
        time.sleep(5)
        # print('product scraped')
        # n1 = int(input('enter 1 for continue and 2 to stop :: '))
        # if n1 == 1:
        #     continue
        # elif n1 == 2:
        #     break

    next_click = next_click + 1
    time.sleep(2)
    if (next_click >= 100):
        print(
            f"sorry, page number {next_click} is out of index run this page separately")
        break
    next_page = driver.find_element(
        By.CSS_SELECTOR, f"div[class='b7FXJ'] > div.e5J1n > ul > li[title='{next_click}']")  # click next page

    next_page.click()
    # link.click()
    time.sleep(5)

# convert product and seller level data into dataframe
# print(prodcut_dict)
product_dataframe = pd.DataFrame(prodcut_dict)

file_name1 = input(
    "Please enter your file name (product and seller level data) :: ")
product_dataframe.to_csv(file_name1 + '.csv', index=False)
time.sleep(1)
reviews_dataframe = pd.DataFrame(review_dict)
file_name2 = input(
    "Please enter your file name (review level data) :: ")
reviews_dataframe.to_csv(file_name2 + '.csv', index=False)

print("data saved Successfully, Program is going to close")
time.sleep(3)
driver.quit()
