import os
import requests
import time
import random
from urllib.parse import urlparse, parse_qs

# List of common User-Agent strings
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.17017',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1',
]

# Function to extract the target URL from query parameters (e.g., 'u=' or 'url=')
def get_redirect_target(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    # Check for common redirect parameters like 'u', 'url', or 'redirect'
    redirect_url = None
    if 'u' in query_params:
        redirect_url = query_params['u'][0]
    elif 'url' in query_params:
        redirect_url = query_params['url'][0]
    elif 'redirect' in query_params:
        redirect_url = query_params['redirect'][0]
    
    return redirect_url

# Function to extract the domain name after following redirects
def extract_domain(url):
    try:
        # Pick a random User-Agent
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        
        # Follow the redirect and get the final URL
        response = requests.get(url, headers=headers, allow_redirects=True)
        final_url = response.url
        
        # If there's a query redirect (like in your case), follow it
        redirect_target = get_redirect_target(final_url)
        if redirect_target:
            print(f"Redirecting to: {redirect_target}")
            response = requests.get(redirect_target, headers=headers, allow_redirects=True)
            final_url = response.url
        
        # Parse the final URL to get the domain
        parsed_url = urlparse(final_url)
        domain = parsed_url.netloc
        return domain
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None

# Main function to read URLs from a file and append domains to an output file
def process_urls(input_file, output_file):
    # Ensure input file exists
    if not os.path.isfile(input_file):
        print(f"Input file '{input_file}' does not exist.")
        return
    
    with open(input_file, 'r') as infile:
        urls = infile.readlines()
        for url in urls:
            url = url.strip()
            domain = extract_domain(url)
            if domain:
                with open(output_file, 'a') as outfile:
                    outfile.write(domain + '\n')
                print(f"Extracted domain: {domain}")
            else:
                print(f"Failed to extract domain from: {url}")
            
            # Add a random delay between 2 to 5 seconds
            delay = random.uniform(2, 5)
            print(f"Waiting for {delay:.2f} seconds before the next request...")
            time.sleep(delay)

# Prompt user for input and output filenames
input_file = input("Enter the input .txt filename (with path if needed): ")
output_file = input("Enter the output .txt filename (with path if needed): ")

# Process URLs
process_urls(input_file, output_file)
