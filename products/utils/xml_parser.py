import xml.etree.ElementTree as ET

def parse_xml_and_extract_products(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'g': 'http://base.google.com/ns/1.0'}

    products = []

    for item in root.findall("channel/item"):
        product = {
            "external_id": item.findtext("g:id", default="", namespaces=ns),
            "sku": item.findtext("g:mpn", default="", namespaces=ns),
            "name": item.findtext("title", default=""),
            "description": item.findtext("description", default=""),
            "price": item.findtext("g:price", default="", namespaces=ns).replace("TRY", "").strip(),
            "image_url": item.findtext("g:image_link", default="", namespaces=ns),
            "product_url": item.findtext("link", default=""),
            "category": item.findtext("g:product_type", default="", namespaces=ns),
        }
        products.append(product)

    return products

