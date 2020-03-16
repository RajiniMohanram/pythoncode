import re
from lxml import html
from json import dump,loads
from requests import get
import json
from re import sub
from dateutil import parser as dateparser
from time import sleep
import certifi
import urllib3

def scrape(n,url):
    urllib3.contrib.pyopenssl.inject_into_urllib3()
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    # This script has only been tested with Amazon.com
    amazon_url  = url+str(n)
    # Add some recent user agent to prevent amazon from blocking the request 
    # Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome
    #headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    for i in range(5):
        response = http.request('GET', amazon_url, timeout=5)
        if response.status == 404:
            return {"url": amazon_url, "error": "page not found"}
        if response.status != 200:
            continue
        
        # Removing the null bytes from the response.
        cleaned_response = response.data
        
        parser = html.fromstring(cleaned_response)
        #XPATH_AGGREGATE = '//span[@id="acrCustomerReviewText"]'
        XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'#
        XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'
        XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'#
        XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
        XPATH_PRODUCT_PRICE = '//span[@id="priceblock_ourprice"]/text()'

        raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
        raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
        total_ratings  = parser.xpath(XPATH_AGGREGATE_RATING)
        reviews = parser.xpath(XPATH_REVIEW_SECTION_1)

        product_price = ''.join(raw_product_price).replace(',', '')
        product_name = ''.join(raw_product_name).strip()

        if not reviews:
            reviews = parser.xpath(XPATH_REVIEW_SECTION_2)
        ratings_dict = {}
        rev_comm=[]
        # Grabing the rating  section in product page
        for ratings in total_ratings:
            extracted_rating = ratings.xpath('./td//a//text()')
            if extracted_rating:
                rating_key = extracted_rating[0] 
                raw_raing_value = extracted_rating[1]
                rating_value = raw_raing_value
                if rating_key:
                    ratings_dict.update({rating_key: rating_value})
        # Parsing individual reviews
        for review in reviews:
            #XPATH_RATING  = './/i[@data-hook="review-star-rating"]//text()'
            XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
            #XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
            #XPATH_REVIEW_TEXT_1 = './/div[@data-hook="review-collapsed"]//text()'
            #XPATH_REVIEW_TEXT_2 = './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview'
            #XPATH_REVIEW_TEXT_2 = './/div//span[@class="a-row a-spacing-small review-data"]/@data-hook=review-body'
            #XPATH_REVIEW_COMMENTS = './/span[@data-hook="review-comment"]//text()'
            #XPATH_AUTHOR = './/span[contains(@class,"profile-name")]//text()'
            #XPATH_REVIEW_TEXT_3 = './/div[contains(@id,"dpReviews")]/div/text()'
            
            #raw_review_author = review.xpath(XPATH_AUTHOR)
            #raw_review_rating = review.xpath(XPATH_RATING)
            raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
            
            # Cleaning data
            #author = ' '.join(' '.join(raw_review_author).split())
            #review_rating = ''.join(raw_review_rating).replace('out of 5 stars', '')
            review_header = ' '.join(' '.join(raw_review_header).split())

            rev_comm.append(review_header)
            
    return rev_comm