import time
from crewai_tools import SerperDevTool
from crewai.tools import tool
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

search_tool = SerperDevTool(
    n_results=30,
)


@tool
def scrape_tool(url: str):
    """
    Use this when you need to read the content of a website
    Returns the content of a website, in case the website is not available, it return 'No Content'
    Input should be `url` sthring. for example (https://en.wikipedia.org/wiki/2025_Cambodia%E2%80%93Thailand_border_conflict)
    """

    print(f'Scrapping URL: ', {url})

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url)

        time.sleep(5)

        html = page.content()

        browser.close()

        soup = BeautifulSoup(html, "html.parser")

        unwanted_tags = [
            "header",
            "footer",
            "nav",
            "aside",
            "script",
            "style",
            "noscript",
            "iframe",
            "form",
            "button",
            "input",
            "select",
            "textarea",
            "img",
            "svg",
            "canvas",
            "audio",
            "video",
            "embed",
            "object",
        ]

        for tag in soup.find_all(unwanted_tags):
            tag.decompose()

        content = soup.get_text(separator=' ')

        return content if content != "" else "No Content"
