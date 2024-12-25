#!/usr/bin/python3.12
"""
Refactored Web Scraping Script with AI Integration
- Extracts names, prices, reviews, and other information from web pages.
"""

import os
import time
import random
import argparse
import requests
import pandas as pd
from urllib.parse import urlparse
from colorama import Fore, Style
from google.api_core import retry
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# Terminal output styles
INFO = Fore.BLUE
SUCCESS = Fore.GREEN
FAILED = Fore.RED
ERROR = Fore.YELLOW
TEXT = Fore.MAGENTA
RESET = Style.RESET_ALL

def save_content(content, filename, mode='w'):
    """Save content to a file."""
    try:
        with open(filename, mode) as file:
            file.write(content)
        print(f"{SUCCESS}[+] Successfully saved to {filename}{RESET}")
    except Exception as e:
        print(f"{ERROR}[?] Failed to save content: {e}{RESET}")

def read_file_content(file):
    """Read content from a file."""
    try:
        with open(file, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"{ERROR}[?] Error reading file: {e}{RESET}")
        return None

def fetch_request(url, max_retries=10, retry_delay=5):
    """Fetch a webpage with retries."""
    proxy_url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"
    try:
        response = requests.get(proxy_url)
        proxy_list = response.text.splitlines()
        http_proxies = [proxy for proxy in proxy_list if proxy.startswith('http')]
    except Exception as e:
        print(f"{ERROR}[?] Error fetching proxies: {e}{RESET}")
        http_proxies = []

    headers_list = [
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2'},
    ]

    for attempt in range(max_retries):
        try:
            print(f"{INFO}[*] Attempt {attempt + 1}: Fetching page...{RESET}")
            proxy = random.choice(http_proxies) if http_proxies else None
            proxies = {"http": proxy} if proxy else None
            response = requests.get(url, headers=random.choice(headers_list), proxies=proxies)
            if response.status_code == 200:
                print(f"{SUCCESS}[+] Success! Status code: {response.status_code}{RESET}")
                return response.text
            print(f"{FAILED}[-] Failed with status code: {response.status_code}. Retrying...{RESET}")
        except requests.exceptions.RequestException as e:
            print(f"{ERROR}[?] Error fetching the page: {e}. Retrying...{RESET}")
        time.sleep(retry_delay)
    return None

def run_model(prompt, system_instruction, save_response_filename,model_to_use,filemode='a'):
    """Run the Gemini API Model.
     - prompt: Your Prompt
     - system_instruction: system instruction for gemini to behave like that
     - save_response_filename: gemini output file name
     - model_to_use: default: gemini-1.5-flash-002
     - filemode: 'w' or 'a' (a for appending)

     - note : compitable gemini api model: 
              - gemini-1.5-flash-001    - gemini-1.5-flash-002    - gemini-1.5-flash-8b
              - gemini-1.5-pro-latest   
        - Experimental: - gemini-2.0-flash-exp  - gemini-1.5-flash-8b-exp-0924
    """
    try:
        genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        model = genai.GenerativeModel(model_name=model_to_use,
                                      system_instruction=system_instruction)

        print(f"{INFO}[*] Using Model {model.model_name}...{RESET}")
        response = model.generate_content(
            [prompt],
            safety_settings=safety_settings,
            stream=True,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.7),
            request_options=RequestOptions(
                retry=retry.Retry(initial=10, multiplier=2, maximum=60, timeout=300),))

        full_text = ""
        for chunk in response:
            print(f"{TEXT}{chunk.text}{RESET}")
            full_text += chunk.text
        save_content(full_text, save_response_filename, filemode)

    except Exception as e:
        print(f"{ERROR}[?] Error in AI Model: {e}{RESET}")

def only_url_passed(url,max_retries,retry_delay,prompt,system_instruction,output_filename,model_to_use,filemode):
    """Function if only url parameter passed..."""
    domain_name=urlparse(url).netloc
    os.makedirs(domain_name, exist_ok=True)
    output_path=os.path.join(domain_name,output_filename)
    closed_prompt = "and make sure to close JSON syntax with }]}"
    webpage=fetch_request(url,max_retries,retry_delay)
    
    if webpage:
        run_model(f"{prompt} {closed_prompt}, {webpage}",
                  system_instruction,output_path,model_to_use,filemode)
    else:
        print(f"{ERROR}[?] Error fetching webpage.{RESET}")
    
def scraper(link_file_json,prompt, output_filename, max_retries, retry_delay, system_instruction,model_to_use):
    """Main scraper function."""
    closed_prompt = "and make sure to close JSON syntax with }]}"

    try:
        print(f"{INFO}[*] Reading extracted links...{RESET}")
        json_data = pd.read_json(link_file_json, orient='records')
        
        for col in json_data.columns:
            for no, link in enumerate(json_data[col]):
                domain_name = urlparse(link).netloc
                
                if not domain_name:
                    print(f"{ERROR}[?] Invalid URL: {link}{RESET}")
                    continue
                os.makedirs(domain_name, exist_ok=True)
                print(f"[{no}] {link}")
                page_content = fetch_request(link, max_retries, retry_delay)
               
                if page_content:
                    print(f"{SUCCESS}[+] Processing page data...{RESET}")
                    output_path = os.path.join(domain_name,output_filename)
                    run_model(f"{prompt} {closed_prompt}, {page_content}", system_instruction,output_path,model_to_use,'a')
                else:
                    print(f"{ERROR}[?] Error loading page: {link}{RESET}")
    
    except FileNotFoundError as e:
        print(f"{ERROR}[?] File not found: {e}{RESET}")
    except Exception as e:
        print(f"{FAILED}[-] Failed to parse JSON results: {e}{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"{INFO}Web Scraping Project with AI Integration{RESET}",
    usage="""

python3 WebScrap.py -u 'https://example.com/' -p 'Extract usefull linux commands from webpage' -o command.json
python3 WebScrap.py -scrap -f links.json -p 'Extract product title,price,ratings from webpages' 

supported model.. 1) flash: - gemini-1.5-flash-001    - gemini-1.5-flash-002    - gemini-1.5-flash-8b
                  2) pro: - gemini-1.5-pro-latest
                  3) Experimental: - gemini-2.0-flash-exp  - gemini-1.5-flash-8b-exp-0924
    """)

    parser.add_argument("-url", "--url", type=str, help="Base URL for scraping")
    parser.add_argument("-scrap", "--scraper", action='store_true', help="Enable data scraping mode")
    parser.add_argument("-f","--file",type=str,help="json file contains target links...")
    parser.add_argument("-p", "--prompt", type=str, default="Extract product links from webpage", help="Prompt for AI model")
    parser.add_argument("-m","--model",type=str,default="gemini-1.5-flash-002",
                        help="gemini genai model to use.. default: gemini-1.5-flash-002")
    parser.add_argument("-o", "--output", type=str, default="ProductData.json", help="Output filename")
    parser.add_argument("-retry", "--max_retries", type=int, default=10, help="Maximum retries for HTTP requests")
    parser.add_argument("-delay", "--retry_delay", type=int, default=5, help="Delay between retries")

    args = parser.parse_args()

    system_instruction = (
        "You are an expert web scraper. Parse product links and product details from HTML sources. "
        "While extracting links, ensure to provide full URLs and remove unwanted tracking elements. "
        "Example: https://www.example.com/../product. "
        "Note: Do not forget to close JSON syntax with }]}."
    )

    try:
        
        if args.scraper:
            print(f"{INFO}[*] Starting scraping process...{RESET}")
            if not args.file:
                print(f"{ERROR}[?] No JSON file provided. Use the -f argument.{RESET}")
                exit(1)
            scraper(args.file,args.prompt, args.output, args.max_retries, 
                    args.retry_delay, system_instruction,args.model,'a')
        elif args.url:
            only_url_passed(args.url,args.max_retries,args.retry_delay,
                            args.prompt,system_instruction,args.output,args.model)
        else:
            parser.print_help()

    except KeyboardInterrupt:
        print(f"{FAILED}[-] Process interrupted by user.{RESET}")
    except Exception as e:
        print(f"{ERROR}[?] Unexpected error: {e}{RESET}")
