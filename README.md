# Advanced Web Scraping Tool with AI Integration

## Overview

This Python-based web scraping tool leverages advanced techniques to extract structured data from web pages, utilizing proxy rotation, AI-powered parsing, and robust error handling. The script is designed for ethical web scraping, with comprehensive features for handling various scraping scenarios.

## Features

- 🌐 **Dynamic Web Scraping**
  - Supports multiple base URLs and search queries
  - Intelligent proxy rotation to avoid IP blocking
  - Multiple user-agent randomization

- 🤖 **AI-Powered Data Extraction**
  - Google Gemini AI integration for intelligent content parsing
  - Structured data extraction with configurable fields
  - Adaptive error handling and data recovery

- 🛡️ **Advanced Security and Reliability**
  - Proxy list fetching
  - Configurable retry mechanisms
  - Colorful console output for better readability

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KaulikMakwana/WebScrape.git
   cd WebScrape
   python WebScrape.py -h
   
   ```

2. Install dependencies:
   ```bash
	pip install -r requirements.txt
   ```

## Usage

### Basic Syntax
```bash
python WebScrap.py -burl <base_url> -q <query> -d <product_data> -o <output_file>
```

### Command-Line Arguments
```Bash
/bin/python WebScrap.py -h           
usage: WebScrap.py [-h] [-burl BASEURL] [-q QUERY] [-d PRODUCTDATA] [-o OUTPUT] [-retry MAX_RETRIES] [-delay RETRY_DELAY]

Web Scraping Project with AI Integration 

options:
  -h, --help            show this help message and exit
  -burl BASEURL, --baseurl BASEURL
                        Base URL for scraping
  -q QUERY, --query QUERY
                        Query parameter for the search URL
  -d PRODUCTDATA, --productdata PRODUCTDATA
                        Data to Parse From Service
  -o OUTPUT, --output OUTPUT
                        File name to save for Scraped Data
  -retry MAX_RETRIES, --max_retries MAX_RETRIES
                        Maximum Retry to request service
  -delay RETRY_DELAY, --retry_delay RETRY_DELAY
                        Retry Delay in between requests

```
### Example
```bash
python testai.py -burl 'https://www.amazon.in/s?k=' -q "laptop" -d "Title,Price,Reviews" -o laptop_data.txt
```

## Note

Use export export GEMINI_API_KEY=<'your api key'>

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Disclaimer

This tool is for educational and research purposes only. Misuse of web scraping tools can violate terms of service and potentially legal regulations.

## Contact

Project Maintainer - [KaulikMakwana/kaullik81@gmail.com]
