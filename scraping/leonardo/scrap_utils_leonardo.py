from playwright.sync_api import sync_playwright
from xml_utils_leonardo import save_data_in_xml

def scraping_section_details(page,content_details_selectors,path,type):
    try:
        title = page.query_selector('h1').inner_text()
        subtitle = page.query_selector(content_details_selectors["subtitle"]).inner_text() if content_details_selectors["subtitle"] else ""
        date = page.query_selector(content_details_selectors["date"]).inner_text() if content_details_selectors["date"] else ""
        content = page.query_selector(content_details_selectors["content"]).inner_text() if content_details_selectors["content"] else ""

        news = {
            "type": type,
            "title": title,
            "subtitle": subtitle,
            "date": date,
            "content": content
        }

        save_data_in_xml(news,path)
    except AttributeError as e:
        pass
        print(e)      

def scrap_section(type,content_selector,content_details_selectors,path,url,n_bug_annunci_ripetuti):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        new_url = url + f'&_com_leonardocompany_list_content_viewer_portlet_ListContentViewerPortlet_page=1'

        page.goto(url)

        pages = int(page.query_selector_all('li.leo-pagination--item a.leo-pagination--item--link')[-2].inner_text())
        print('pages:',pages)
        page.close()

        for page_num in range(1,pages+1):
            page = context.new_page()
            new_url = url + f'&_com_leonardocompany_list_content_viewer_portlet_ListContentViewerPortlet_page={page_num}'
            page.goto(new_url)
            contenuti = page.query_selector_all(content_selector)

            urls = [c.query_selector('a').get_attribute('href') for c in contenuti][n_bug_annunci_ripetuti:]
            for uri in urls:
                print('page:',page_num,'url:',uri)
                page.goto(uri)
                scraping_section_details(page, content_details_selectors,path,type)
            page.close()
