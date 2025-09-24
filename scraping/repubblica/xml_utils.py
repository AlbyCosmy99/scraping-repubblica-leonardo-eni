import xml.etree.ElementTree as ET

i = 1

def save_article_in_xml(article):
    global i 

    root = ET.Element("article")
    ET.SubElement(root, "type").text = article["type"]
    ET.SubElement(root, "title").text = article["title"]
    ET.SubElement(root, "subtitle").text = article["subtitle"]
    ET.SubElement(root, "author").text = article["author"]
    ET.SubElement(root, "date").text = article["date"]
    ET.SubElement(root, "content").text = article["content"]


    filename = f"articles/rp_{i}.xml"
    i = i+1

    tree = ET.ElementTree(root)

    with open(filename, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

     