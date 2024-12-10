#!/usr/bin/python3.12
''' Web Scraping Project To Scrape Name, Price, Reviews...'''

import requests, os, time, random, argparse
from urllib.parse import urlparse
import trafilatura as tf
from colorama import Fore, Style
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold



'''[*]-> Information [+]-> Success [-]-> Failed [?]-> Error '''
Info=Fore.BLUE
Success=Fore.GREEN
Failed=Fore.RED
Error=Fore.YELLOW
Text=Fore.MAGENTA
Reset=Style.RESET_ALL

def FilePath(dirname,filename):
    file_path = os.path.join(dirname,filename)
    return file_path

def SaveContent(content,filename,mode='w'):
    '''Save Content to file
      - content: content to save
      - filename: filename 
      - mode: w|a (default=w) Go for a mode for appending results
    '''
    with open(filename,mode) as file:
        file.write(content)  

def ReadFileContent(file):
    '''Read file content
      - file: File
    '''
    with open(file,'r') as file:
        return file.read()
    
def FetchReq(url,max_retries=10, retry_delay=5): 
    '''Fetch Page with retries.
     - max_retries: Number of times to retry before giving up
     - retry_delay: Time in seconds between retries
    '''
    ProxyUrl="https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"
    response=requests.get(ProxyUrl)
    proxy_list = response.text
    HTTPProxies=[]
    for proxy in proxy_list.splitlines():
        if proxy.startswith('http'):
            HTTPProxies.append(proxy)
        
    headers_list= [
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'},
        {'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'},
        {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'},
        {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2'},
        ]
    
    retries = 0
    while retries < max_retries:
        try:
            print(f"{Info}[*] Attempt {retries + 1}: Fetching page ...{Reset}")
            r = requests.get(url, headers=random.choice(headers_list),proxies={"http":random.choice(HTTPProxies)})
            if r.status_code == 200:
                print(f"{Success}[+] Success! Status code: {r.status_code}...{Reset}")
                return r.text
            else:
                print(f"{Failed}[-] Failed with status code: {r.status_code}. Retrying...{Reset}")
        except (requests.exceptions.RequestException) as e:
            print(f"{Error}[?] Error fetching the page: {e}. Retrying... {Reset}")

        retries += 1
        time.sleep(retry_delay)

def RunModel(apikey,Prompt,SystemInstruction,SaveResponseFileName='index.html',FileMode='w'):
    '''Run Gemini API Model
     - apikey:  Your Api Key
     - Prompt:  Your Prompt to process
     - SystemInstruction: System Instructions...
     - Model:   Gemini Model to use (Stable: gemini-1.5-flash-002) (default:gemini-1.5-flash-001) Else is (gemini-1.5-pro,gemini-1.5-flash,etc..)
     - SaveResponseFileName:    File name to save model's response
    '''
    genai.configure(api_key=(apikey))
    models=["gemini-1.5-flash-001","gemini-1.5-flash-002"]


    try:
        model=genai.GenerativeModel(model_name=random.choice(models),
        system_instruction=SystemInstruction,)
        safe = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
             ]
        response=model.generate_content(Prompt,safety_settings=safe,stream=True)
        time.sleep(4)
        print(f"{Info}[*] Using Model {model.model_name}...{Reset}")
        for chunk in response:
            print(f"{Info}[>>]{Reset} {Text}{chunk.text} {Reset}")
        print("[+]________________________[*]________________________________[+]")
        SaveContent(response.text,SaveResponseFileName,FileMode)

    except Exception as e:
        print(f"{Error}[?] Error In AI Model........{e} {Reset}")

def main(baseurl,query,ProductData,OutPut,max_retries,retry_delay):
    apikey=os.environ['GEMINI_API_KEY']
    SystemInstruction = f'''
- You are an expert web scraping assistant with advanced knowledge in extracting structured data from unstructured HTML and web pages.
- Your primary responsibility is to parse specific data fields provided as input (like {ProductData}) from raw webpage content with exceptional precision.
- Output the results in a structured and clean format, ready for downstream processing.
- Maintain data integrity and avoid any irrelevant or noisy information in the extraction process.

Key Responsibilities:
1. **URLs**:
   - Extract clean, fully-formed product URLs, omitting unnecessary tracking or session parameters.
   - Ensure URLs are properly reconstructed using the base URL if they are relative links.

2. **Data Fields**:
   - For each entry, extract the details specified in {ProductData}.
   - Ensure data is clearly and consistently formatted, avoiding irrelevant or duplicate information.

3. **Output Format**:
   - Save all extracted data in a plain text file, structured ..:
   - Include headers in the saved file to improve readability, such as:
     Data Extracted from {Dir}
     Date: {time.strftime("%y-%m-%d")}
     ----------------------------------------------------
   - When Parse links just give links in output.
   - Ensure the data is consistently formatted and free of additional comments, debug symbols, or irrelevant content.

4. **Reliability**:
   - Maintain clarity and consistency in the output format for every entry.
   - Avoid including any additional comments, metadata, or commentary in the response.

Additional Notes:
- Do not provide any explanations or comments in the output.
- Ensure that the output data is consistently structured and clean for every entry.
- While generating output do not make any signs like ```  something just give me pure answer as i need to save it in file for data processing.
'''

    IndexPagePrompt = '''
- Extract and list all product URLs from the uploaded webpage.
- Ensure that only full product links are included, excluding any unrelated data.
- Additionally, clean the links to remove unnecessary parameters or tracking information,
    retaining only the essential parts of the URLs.
- When extracting product details, focus on obtaining clean, structured names
    and relevant data without unnecessary elements. 
- In Response Just give me Link 
    Example:- https://www.amazon.in/../link        
- Note:- do not give any kind of explanation also give accurate response.
'''


    DataParsePrompt = f'''
- Parse the provided content and extract the following data:
  {ProductData}.
- Ensure the output is well-structured and formatted like this:
  No: <Serial Number>   Title: Value1   Price: Value2 or any other if mention in prompt ...
- Additional Notes:
  - Maintain clarity and consistency in the output format.
  - Exclude any irrelevant information, boilerplate content, or page navigation data.
  - Handle edge cases gracefully where data fields (e.g., {ProductData}) may be missing.
- Do not include any explanations, metadata, or commentary in the response.
'''

    ComplateUrl=f"{baseurl}{query}"
    parsed_url = urlparse(ComplateUrl) 
    Dir=parsed_url.netloc
    try:
    
        os.makedirs(Dir, exist_ok=True)
        ChildDir=os.path.join(Dir,'ProductData')
        os.makedirs(ChildDir, exist_ok=True)

        indexfile=FilePath(Dir,'index.html')
        filelinks=FilePath(ChildDir,'links.txt')
        
        if os.path.isdir(Dir) and os.path.exists(Dir):
            print(f"{Info}[*] Geting Index Page...{Reset}")
            IndexPage=FetchReq(ComplateUrl,max_retries,retry_delay)   
            SaveContent(IndexPage,indexfile,'w') if IndexPage else print("[-] index.html File Not Found..")
           
        if os.path.isfile(indexfile):
            RunModel(apikey,f"{IndexPagePrompt}, {ReadFileContent(indexfile)}",SystemInstruction,filelinks,'w')
            time.sleep(4)

        if os.path.isfile(filelinks):
            print(f"{Info}[*] Getting Links......{Reset}")
            with open(filelinks,'r') as file:
                
                ExtractedData=[]
                for num,link in enumerate(file.readlines()):
                    link=link.strip()
                    if not link: continue
                    print(f'{Info}[{num}]- {link}{Reset}')
                    pages=FetchReq(link,max_retries,retry_delay)
                    if not pages:
                       print(f"{Failed}[-] Failed to fetch content for {link}. Skipping...{Reset}")
                       continue

                    ExtractTXT=tf.extract(pages)
                    if not ExtractTXT:
                        print(f"{Failed}[-] No extractable text found on {link}. Skipping...{Reset}")
                        continue
                    else:
                        print(f"{Success}[+] Downloaded WebPage...{Reset}")
                    productdata=FilePath(Dir,f'data{num}.txt')
                    SaveContent(ExtractTXT,productdata,'w')
                    ExtractedData.append(productdata)
                
                for data in ExtractedData:
                    RunModel(apikey,f"{DataParsePrompt}, {ReadFileContent(data)}",SystemInstruction,
                        FilePath(ChildDir,OutPut),'a')
                    time.sleep(4)

    except FileNotFoundError :
        print(f"{Error}[?] File Not Found...{Reset}")
    except FileExistsError :
        print(f"{Error}[?] File Already Exists.. {Reset}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"{Info}Web Scraping Project with AI Integration {Reset}")
    
    parser.add_argument("-burl","--baseurl",type=str, help="Base URL for scraping")
    parser.add_argument("-q","--query",default="monitor",type=str, help="Query parameter for the search URL")
    parser.add_argument("-d","--productdata",type=str,action='store',default="Title,Price",help="Data to Parse From Service")
    parser.add_argument("-o","--output",type=str,default="ProductData.txt",help="File name to save for Scraped Data")
    parser.add_argument("-retry","--max_retries",type=int,default=10,help="Maximum Retry to request service")
    parser.add_argument("-delay","--retry_delay",type=int,default=5,help="Retry Delay in between requests")

    args=parser.parse_args()
    baseurl=args.baseurl
    query=args.query
    productdata=args.productdata
    output=args.output
    max_retries=args.max_retries
    retry_delay=args.retry_delay

    try:
        if baseurl:
            print(f"{Info}......Web Scraper.......{Reset}")
            main(baseurl,query,productdata,output,max_retries,retry_delay)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print(f"{Failed}[-] Pressed ctrl^c...{Reset}")