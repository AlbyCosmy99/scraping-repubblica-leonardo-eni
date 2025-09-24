import xml.etree.ElementTree as ET

i = 1

def save_data_in_xml(news, path):
    global i 

    root = ET.Element("news")
    ET.SubElement(root, "type").text = news["type"]
    ET.SubElement(root, "title").text = news["title"]
    ET.SubElement(root, "subtitle").text = news['subtitle']
    ET.SubElement(root, "author").text = ''
    ET.SubElement(root, "date").text = news["date"]
    ET.SubElement(root, "content").text = news["content"]


    filename = f"{path}/leo_{i}.xml"
    i = i+1

    tree = ET.ElementTree(root)

    with open(filename, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

     