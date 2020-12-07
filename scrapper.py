import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse

import sqlite3
import pymysql.cursors
import os
import contextlib
from tqdm import notebook


def check_status():
    """Checks status of webpage"""
    r = requests.get('https://www.trustpilot.com')
    print(r.status_code)
    print(r.status_code == requests.codes.ok)
    print(requests.codes['temporary_redirect'])
    print(requests.codes.teapot)
    print(requests.codes['o/'])


def scrap(company, num_pages):
    """Scrap a company's reviews from their TrustPilot page."""
    names = []
    ratings = []
    titles = []
    contents = []
    rev_wrote = []
    replies = []
    company_names = []
    num_reviews = []
    company_ratings = []
    website = []
    urls = []

    for p in range(1, int(num_pages)):

        page_url = requests.get('https://www.trustpilot.com/review/' + company + '?page=' + str(p))
        soup = BeautifulSoup(page_url.content, 'html.parser')
        review_card = soup.find_all('div', class_='review-card')

        # find website of the company
        # I do it just one time
        # TODO LOOK AT THIS we need to put
        if p == 1:
            web_tag = soup.find_all('a', class_="badge-card__section badge-card__section--hoverable company_website")
            for a in web_tag:
                website.append(a['href'])
            company_name = soup.find('span', class_='multi-size-header__big').get_text(strip=True)
            company_names.append(company_name)
            num_review = soup.find('h2', class_='header--inline').get_text(strip=True)
            num_review = ''.join(filter(str.isdigit, num_review))
            num_reviews.append(num_review)
            company_rating = soup.find('p', class_='header_trustscore').get_text()
            company_ratings.append(company_rating)

        # get url for each user
        user_url = soup.find_all('a', href=True)
        for a in user_url:
            user_id = a['href']
            if '/users/5' in user_id and user_id not in urls:
                urls.append(user_id)

        for review in review_card:

            # Username
            name = review.find('div', class_='consumer-information__name').get_text(strip=True)
            names.append(name)
            # Rating
            rating = review.find('img').attrs.get('alt')
            ratings.append(rating)
            # Review title
            title = review.find('a', class_='link link--large link--dark').get_text()
            titles.append(title)
            # Review content
            if review.find('p', class_='review-content__text'):
                content = review.find('p', class_='review-content__text').get_text(strip=True)
            else:
                content = None
            contents.append(content)
            # Number of reviews wrote by user
            rev_written = review.span.get_text()
            rev_wrote.append(rev_written)
            # Replied received
            reply = review.find('div', class_='review__company-reply')
            if reply:
                replies.append(True)
            else:
                replies.append(False)

            # country and parse another page
    countries = parse_another_page(urls)

    reviews_dict = {'ratings': ratings,
                    'titles': titles,
                    'contents': contents,
                    'replies': replies
                    }

    users_dict = {'names': names,
                  'countries': countries,
                  'rev_wrote': rev_wrote
                  }

    companies_dict = {'company_names': company_names,
                      'company_ratings': company_ratings,
                      'website': website,
                      'num_reviews': num_reviews
                      }

    return reviews_dict, users_dict, companies_dict


def parse_another_page(urls):
    lst = []
    for url in urls:
        page_url = requests.get('https://www.trustpilot.com/' + url)
        soup = BeautifulSoup(page_url.content, 'html.parser')
        countries = soup.find('div', class_='user-summary-location')
        if countries is not None:
            lst.append(countries.text.strip().strip('\n'))
    return lst


def export_csv(company, num_pages):
    """Stores results to pandas df and creates a csv file."""
    reviews_dict, users_dict, companies_dict = scrap(company, num_pages)
    reviews_df = pd.DataFrame(reviews_dict)
    users_df = pd.DataFrame(users_dict)
    companies_df = pd.DataFrame(companies_dict)
    reviews_df.to_csv('reviews.csv')
    users_df.to_csv('users.csv')
    companies_df.to_csv('companies.csv')


# def export_sql(company, num_pages):
#     """Stores results to pandas df and creates a csv file."""
#     reviews_dict, users_dict, companies_dict = scrap(company, num_pages)
#     reviews_df = pd.DataFrame(reviews_dict)
#     users_df = pd.DataFrame(users_dict)
#     companies_df = pd.DataFrame(companies_dict)
#
#     connection = pymysql.connect(host='localhost',
#                                  user='root',
#                                  password='123456',
#                                  db='TestDB1.db',
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)
#
#     c = connection.cursor()
#     users_table = """
#         CREATE TABLE Users (
#           user_name varchar(255),
#           country varchar(255),
#           rev_wrote int,
#           PRIMARY KEY (user_id)
#           );
#         """
#     with connection.cursor() as cursor:
#         cursor.execute(users_table)
#         connection.commit()
#
#     users_df.to_sql('USERS', connection, if_exists='replace', index=False)
#
#     c.execute('''
#     SELECT * FROM USERS
#               ''')
#
#     for row in c.fetchall():
#         print(row)



def main():
    # CLI
    parser = argparse.ArgumentParser()
    parser.add_argument('company', help='company_name')
    parser.add_argument('num_pages', help='page limit')
    args = parser.parse_args()

    company = args.company
    num_pages = args.num_pages
    print('Scrapping data from ' + company)
    # scrap(company, num_pages)
    export_csv(company, num_pages)







if __name__ == '__main__':
    main()
