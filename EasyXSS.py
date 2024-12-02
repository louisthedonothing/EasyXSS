import requests #HTTP requests (Post and get requests)
import urllib #Encodes URLS
from bs4 import beautifulsoup #Parse html and locate input forms
import mechanize # making a browser to interact with xss forms
import selenium # inject payloads
import pyppeteer # websocketing
import scrapy #locates multiple input points
import argparse # Handles command line prompts


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

def submitForm(form, url, payload):
'''
submits form and payload to the given url
'''
    try:
        action = form.attrs.get("action")
        method = form.attrs.get("Method", "get").lower()
        form_url = urllib.parse.urljoin(join, action)
        
        
        inputs = form.find_all("input")
        data = {}
        for input_tag in inputs:
            name = input_tag.attrs.get("name")
            input_type = input_tag.attrs.get("type", "text")
            value = payload if input_type == "text" else input_tag.attrs.get("value", "")
            if name:
                data[name] = value

#send request based on form method
if method == "post":
    response =  requests.post(form_url, data=data)
else:
    response = requests.get(form_url, params=data)

    return response
except Exception as e:
       print(f"Error submitting form:{e}")
       return None

def scan_xss(url, payloads):
    """
    Scans the target URL for XSS vulnerabilities using the given payloads.
    """
    forms = find_forms(url)
    if not forms:
        print("No forms found on the URL.")
        return

    print(f"Found {len(forms)} forms on {url}.")
    for i, form in enumerate(forms):
        print(f"\nScanning form #{i + 1}...")
        for payload in payloads:
            print(f"Testing payload: {payload}")
            response = submit_form(form, url, payload)
            if response and payload in response.text:
                print(f"XSS vulnerability detected with payload: {payload}")
                break
        else:
            print("No vulnerabilities detected for this form.")



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


