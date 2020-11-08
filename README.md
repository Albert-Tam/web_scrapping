# Trustpilot.com web scrapping
Scraps reviews from Trustpilot.

## Table of contents
* [Introduction](#introduction)
* [Language](#language)
* [Requirements](#requirements)
* [Setup](#setup)
* [Usage](#usage)

## Introduction
We are scrapping the reviews of companies on Trustpilot.com.  For each review we get information such as rating, username, review title, review content, numbers of reviews written by the user and whether the user recieved a reply by the company. 

## Language

`python 3.7.4`


## Requirements
```
beautifulsoup4 == 4.9.3
pandas == 1.1.3
requests == 2.24.0

```

## Setup
```
$ pip install -r requirements.txt
```

## Usage
- Set the company's review to scrap by setting the variable `COMPANY` and the number of pages to scrap by setting the variable `PAGES`.
- Run the jupyter notebook web_scrapping.ipynb.
