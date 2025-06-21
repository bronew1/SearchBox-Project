import xml.etree.ElementTree as ET

def parse_xml_and_extract_products(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    products = []
    for item in root.findall("item"):
        product = {
            "external_id": item.findtext("g:id", default=""),
            "sku": item.findtext("g:mpn", default=""),
            "name": item.findtext("title", default=""),
            "description": item.findtext("description", default=""),
            "price": item.findtext("g:price", default="").replace(" TRY", ""),
            "image_url": item.findtext("g:image_link", default=""),
            "product_url": item.findtext("link", default=""),
            "category": item.findtext("g:product_type", default=""),
        }
        products.append(product)
    return products