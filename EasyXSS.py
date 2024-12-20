import requests  # HTTP requests (Post and get requests)
import urllib  # Encodes URLs
from bs4 import BeautifulSoup  # Parse html and locate input forms
import argparse  # Handles command line prompts

# commit notes: fixed naming conventions because im a dummy

def form_finder(url):
    """
    Fetches and parses forms
    """
    try:
        response = requests.get(url, timeout=10)  # Add timeout here
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.find_all("form")
    except requests.exceptions.Timeout:
        print("Request timed out while fetching forms.")
    except Exception as e:
        print(f"Error finding forms: {e}")
    return []


def submit_form(form, url, payload):
    """
    Submits form and payload to the given URL
    """
    try:
        action = form.attrs.get("action")
        method = form.attrs.get("method", "get").lower()
        form_url = urllib.parse.urljoin(url, action)

        inputs = form.find_all("input")
        data = {}
        for input_tag in inputs:
            name = input_tag.attrs.get("name")
            input_type = input_tag.attrs.get("type", "text")
            value = payload if input_type == "text" else input_tag.attrs.get("value", "")
            if name:
                data[name] = value

        # Send request based on form method
        if method == "post":
            response = requests.post(form_url, data=data, timeout=10)  # Add timeout here
        else:
            response = requests.get(form_url, params=data, timeout=10)  # Add timeout here

        return response
    except requests.exceptions.Timeout:
        print("Request timed out while submitting the form.")
    except Exception as e:
        print(f"Error submitting form: {e}")
    return None


def scan_xss(url, payloads):
    """
    Scans the target URL for XSS vulnerabilities using the given payloads.
    """
    forms = form_finder(url)  
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
    parser = argparse.ArgumentParser(description="Easy XSS")

    # The following 2 lines of code just define the necessary flags in the script
    parser.add_argument('-u', '--url', required=True, help='Target for the XSS scanner')
    parser.add_argument('-p', '--payloads', required=True, help='Payload file with XSS scripts')

    # Parses the flags and stores them in args
    args = parser.parse_args()

    default.payloads = [
        "<script>alert(1)</script>",
        "<svg/onload=alert(1)>",
        "<script>alert('XSS')</script>",
    ]

    # Load payloads from file or use default
    if args.payloads:
        try:
            with open(args.payloads, 'r') as f:
                payloads = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print("Payload file not found. Using default payloads.")
            payloads = default.payloads
    else:
        payloads = default.payloads

    # Start scanning for XSS vulnerabilities
    print(f"Scanning URL: {args.url}")
    scan_xss(args.url, payloads)


# Run the script
if __name__ == "__main__":
    main()

