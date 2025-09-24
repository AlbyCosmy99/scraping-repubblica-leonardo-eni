from playwright.sync_api import sync_playwright, Error
from xml_utils import save_article_in_xml
import os
from dotenv import load_dotenv

def scraping_articolo_digitale(page):
    article = {
        "type": "digitale"
    }

    if page.query_selector('h1.story__title'):
        article["title"] = page.locator('h1.story__title').text_content()
    else:
        article["title"] = ""

    if page.query_selector('.story__summary p'):
        article["subtitle"] = page.locator('.story__summary p').first.text_content()
    else:
        article["subtitle"] = ""

    if page.query_selector('em.story__author'):
        article["author"] = page.locator('em.story__author').first.text_content()
    else:
        article["author"] = ""

    if page.query_selector('div time.story__date'):
        article["date"] = " ".join(page.locator('div time.story__date').text_content().split(' ')[:3])
    else:
        article["date"] = ""

    if page.query_selector('div.story__text'):
        article["content"] = page.locator('div.story__text').first.text_content()
    else:
        article["content"] = ""

    save_article_in_xml(article)

def scraping_articolo_cartaceo(page):
    article = {
        "type": "cartaceo"
    }

    article["title"] = page.locator('h1').first.text_content()
    article["subtitle"] = ""
    article["author"] = ""

    if page.query_selector('article .edizione'):
        article["date"] = page.locator('article .edizione').text_content().split(',')[0]
    else:
        article["date"] = ""

    paragraphs = []
    for p in page.query_selector_all('article p'):
        paragraph = p.text_content().strip()
        if paragraph:
            paragraphs.append(paragraph)

    article["content"] = "\n\n".join(paragraphs)

    save_article_in_xml(article)


def get_search_link(start_date, end_date = None, step = 5, page = 1):
    return f"https://ricerca.repubblica.it/ricerca/repubblica?query=climatico+climatica&fromdate={start_date}&todate={end_date if end_date != None else build_date_from_step(start_date, step)}&sortby=adate&author=&mode=any&page={page}"

def build_date_from_step(start_date, step):
    l_date_str = start_date.split('-')
    l_date_str[0] = str(int(l_date_str[0]) + step)
    return "-".join(l_date_str)

load_dotenv()

email_google = os.getenv("GOOGLE_EMAIL")
pass_google = os.getenv("GOOGLE_PASSWORD")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://ricerca.repubblica.it/ricerca/repubblica")

    #google login
    page.wait_for_selector("#iub_cmp_subscribe_custom_btn")
    page.click("#iub_cmp_subscribe_custom_btn")

    with context.expect_page() as google_popup_info:
        page.click("#Google_btn")

    google_popup = google_popup_info.value
    google_popup.fill('input[type="email"]',email_google)
    google_popup.click("text='Avanti'")
    google_popup.fill('input[type="password"]',pass_google)
    google_popup.click("text='Avanti'")

    page.wait_for_selector(".iubenda-cs-accept-btn")
    page.click('.iubenda-cs-accept-btn')
    
    page.wait_for_selector("text='Continua senza accettare'")
    page.click("text='Continua senza accettare'")

    start_date = '2024-06-19'

    page.goto(get_search_link(start_date, '2025-06-29'))

    VINCOLO_PAGINE_REPUBBLICA = 50
  
    pages  = int(page.locator('.pagination p').text_content().split(' ')[-1])
    page_num = 1
    while page_num <= pages:
        print('page:',page_num)

        url = get_search_link(start_date, step=5,page=str(page_num))
        page.goto(url)

        try:
            page.wait_for_selector('section#lista-risultati article h1 a')
        except Error as e:
            print(e)
            continue
 
        times_container = page.locator('section#lista-risultati article time')
        times = times_container.evaluate_all("elements => elements.map(el => el.getAttribute('datetime'))")

        times_file = open('times.txt','w')
        line = f"page: {page_num}, times: {times}, last time: {times[-1]}\n"
        times_file.write(line)
        times_file.close()

        if page_num%VINCOLO_PAGINE_REPUBBLICA==0:
            page_num = 1
            page.close()
            page = context.new_page()
            start_date=times[-1]
            link_ricerca = get_search_link(start_date, step=5)
            page.goto(link_ricerca)
        else: 
            page_num+=1
        links = page.locator('section#lista-risultati article h1 a')
        hrefs = links.evaluate_all("links => links.map(link => link.href)")

        for href in hrefs:
            print('link:',href)
            if 'video.repubblica.it' in href:
                continue
            try:
                page.goto(href)
                isDigitale = page.locator('main article.story').count() > 0
                isCartaceo = page.locator('body.premium-template').count() > 0
                
                if isDigitale:
                    scraping_articolo_digitale(page)
                    print('articolo digitale')
                elif isCartaceo:
                    scraping_articolo_cartaceo(page)
                    print('articolo cartaceo')
                else:
                    print('altro tipo di articolo')
            except Error as e:
                print("Errore di playwright su ", href, "-", e)
            finally:
                page.go_back()

    while True:
        pass


