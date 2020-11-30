import requests
from bs4 import BeautifulSoup
from constants import constant
from reviewer import Reviewer
import sys
import csv
import argparse

list_string_reviewer = []


def create_csv():
    """ create csv column titles"""

    row = ['name', 'rating', 'title', 'content', 'rev_wrote', 'reply', 'class instance']
    with open('reviewer.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        csvFile.write(",")
        writer.writerow(row)
    csvFile.close()


def sort_review_card(review_card, run):
    """creates object of reviewer and saves to spreadsheet"""

    for review in review_card:
        name = review.find('div', class_='consumer-information__name').get_text(strip=True)
        rating = review.find('img').attrs.get('alt')
        title = review.find('a', class_='link link--large link--dark').get_text()

        if review.find('p', class_='review-content__text'):
            content = review.find('p', class_='review-content__text').get_text(strip=True)
        else:
            content = ' '

        rev_written = review.span.get_text()

        reply = review.find('div', class_='review__company-reply')

        reviewer = Reviewer(name, rating, title, content, rev_written, reply)
        review_string = str(name) + str(rating) + str(title) + str(content) + str(rev_written)
        if review_string in list_string_reviewer:
            return False
        else:
            list_string_reviewer.append(review_string)
            reviewer.save_to_csv()
            reviewer.save_to_sql()

    return run


def scrap(company, num_pages):
    """Scrap a company's reviews from their TrustPilot page."""
    p = 1
    run = True
    if num_pages.isdigit():
        page_limit = int(num_pages)
    else:
        page_limit = 10000

    while run and p <= page_limit:
        page_url = requests.get('https://www.trustpilot.com/review/' + company + '?page=' + str(p))
        soup = BeautifulSoup(page_url.content, 'html.parser')
        review_card = soup.find_all('div', class_='review-card')
        run = sort_review_card(review_card, run)
        p += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('company', help='company_name')
    parser.add_argument('num_pages', help='page limit')
    # parser.add_argument('-h', action='store_true', help='message')
    args = parser.parse_args()

    # if args.h is True:
    #     print("Enter company name followed by page limit.\
    #           Entre 'all' if you would like to scrape all pages.")

    company = args.company
    num_pages = args.num_pages

    create_csv()
    print('Scrapping data from ' + company)
    scrap(company, num_pages)


if __name__ == '__main__':
    main()
