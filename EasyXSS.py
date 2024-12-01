import requests #HTTP requests (Post and get requests)
import urllib #Encodes URLS
import beautifulsoup4 #Parse html and locate input forms
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
    with open(args.payloads, 'r') as f:
        customPayloads = [line.strip() for line in f.readlines()]
        payloads = customPayloads
else:
        payloads = defaultPayload
