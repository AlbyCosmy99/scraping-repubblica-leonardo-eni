from playwright.sync_api import sync_playwright
from xml_utils_eni import save_data_in_xml

website = 'https://www.eni.com/'

def scraping_section_details(page,content_type):
    titolo = page.query_selector('h1').inner_text()
    sottotitolo = ''

    contenuti_parziali_nodes = page.query_selector_all('.wrapper-template > div:not(.html-box):not(.contatti):not(.launch):not(.mail-alert)')
    contenuto = "".join([c.inner_text() for c in contenuti_parziali_nodes])
    autore = ''
    data = page.query_selector('div.container-date-and-shdo time').inner_text().split('-')[0].strip()

    save_data_in_xml({"type": content_type, "title": titolo,"subtitle": sottotitolo, "author": autore,"date":data,"content":contenuto}, f"scraping/eni/{content_type}")


    print('data',data)

def scrap_content(content_type, url_type):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        base_url = f'{website}it-IT/media/{url_type}.html?data-date-from=1577833200&data-date-to=1756850399&'
        url = base_url + 'page=0'
        page.goto(url)

        page.wait_for_selector('ul.pagination li.page-item')
        pages = int(page.query_selector_all('ul.pagination li.page-item')[-2].inner_text())
        print('pages:',pages)
        page.close()

        for page_num in range(pages):
            page = context.new_page()
            url = base_url + f'page={page_num}'
            page.goto(url)

            page.wait_for_selector('a.container-card')
            contents = page.query_selector_all('a.container-card')
            
            urls = [node.get_attribute('href') for node in contents]
        
            for url in urls:
                full_url = website + url
                print('page:',page_num,'url:',full_url)
                page.goto(full_url)
                scraping_section_details(page, content_type)
            page.close()


# scrap_content("stampa",'comunicati-stampa')
scrap_content("news",'news')