# WebScrapAI: Web Scraping with AI Integration

WebScrapAI is a powerful Python-based web scraping tool that integrates AI to extract data such as names, prices, reviews, and other relevant information from web pages. The tool supports scraping from a single URL or a JSON list of URLs and leverages Google's Generative AI API for advanced content parsing and extraction.

## Features
- Fetch web pages using robust retry mechanisms with proxy support.
- Extract useful links and relevant content from web pages.
- Leverage Google's Generative AI to parse and process webpage data.
- Support for single URL or JSON file-based scraping.
- Save extracted data in a structured format.

## Prerequisites
- Python 3.12 or higher
- Google Generative AI credentials (GEMINI API Key)

Installation:
```bash
git clone https://github.com/KaulikMakwana/WebScrap.git
cd WebScrap
pip install -r requirements.txt
python3 WebScrap.py -h
```

## Usage
Run the script using the command-line interface (CLI). The tool supports two modes of operation:

### 1. Scraping with a JSON File
If you have a JSON file containing a list of URLs, use the following command:
```bash
python WebScrapAI.py --scraper -f <json_file> -p "<AI_prompt>" -o <output_file>
```
#### Arguments:
- `--scraper`: Enables the scraping mode.
- `-f, --file`: Path to the JSON file containing target URLs.
- `-p, --prompt`: Custom prompt for the AI to parse webpage data.
- `-o, --output`: Output filename for scraped data.

### 2. Scraping a Single URL
To scrape data from a single URL, use the following command:
```bash
python WebScrapAI.py --url <webpage_url> -p "<AI_prompt>" -o <output_file>
```
#### Arguments:
- `--url`: URL of the webpage to scrape.
- `-p, --prompt`: Custom prompt for the AI to parse webpage data.
- `-o, --output`: Output filename for scraped data.

### Optional Arguments:
- `--max_retries`: Maximum number of retries for fetching web pages (default: 10).
- `--retry_delay`: Delay between retries in seconds (default: 5).

## Example Commands
### JSON File Scraping
```bash
python WebScrapAI.py --scraper -f links.json -p "Extract product details" -o ProductData.txt
```

### Single URL Scraping
```bash
python WebScrapAI.py --url https://example.com -p "Extract usefull linux commands from webpage" -o commands.json
```

## Environment Variables
Ensure the `GEMINI_API_KEY` is set in your environment to use Google's Generative AI:
```bash
export GEMINI_API_KEY=<your_api_key>
```

## License
This project is licensed under the MIT License.

## Author
Developed by Kaulik Makwana. Contributions and feedback are welcome!

