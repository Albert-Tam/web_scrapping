import requests
from bs4 import BeautifulSoup
import pandas as pd


def check_status():
    """Checks status of webpage"""
    r = requests.get('https://www.trustpilot.com')
    print(r.status_code)
    print(r.status_code == requests.codes.ok)
    print(requests.codes['temporary_redirect'])
    print(requests.codes.teapot)
    print(requests.codes['o/'])


def scrap():
    """Scrap a company's reviews from their TrustPilot page."""
    names = []
    ratings = []
    titles = []
    contents = []
    rev_wrote = []
    replies = []
    website = []
    urls = []
    PAGES = 10
    COMPANY = 'www.monday.com'

    for p in range(1, PAGES):

        page_url = requests.get('https://www.trustpilot.com/review/' + COMPANY + '?page=' + str(p))
        soup = BeautifulSoup(page_url.content, 'html.parser')
        review_card = soup.find_all('div', class_='review-card')

        # find website of the company
        # I do it just one time
        # TODO website name, you can use it if you want
        if p == 1:
            web_tag = soup.find_all('a', class_="badge-card__section badge-card__section--hoverable company_website")
            for a in web_tag:
                website.append(a['href'])

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

    # get the id of each user
    # TODO you can use it if you want
    id = []
    for i in urls:
        id.append(i.replace('/users/', ''))

    reviews_dict = {'names': names,
                    'ratings': ratings,
                    'titles': titles,
                    'contents': contents,
                    'rev_wrote': rev_wrote,
                    'replies': replies,
                    'countries': countries
                    }

    return reviews_dict


def parse_another_page(urls):
    lst = []
    for url in urls:
        page_url = requests.get('https://www.trustpilot.com/' + url)
        soup = BeautifulSoup(page_url.content, 'html.parser')
        countries = soup.find('div', class_='user-summary-location')
        if countries is not None:
            lst.append(countries.text.strip().strip('\n'))
    return lst


def export_csv():
    """Stores results to pandas df and creates a csv file."""
    rev_dict = scrap()
    reviews_df = pd.DataFrame(rev_dict)
    reviews_df.to_csv('reviews.csv')


def main():
    # print(scrap())
    export_csv()


if __name__ == '__main__':
    main()
