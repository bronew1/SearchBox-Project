import xml.etree.ElementTree as ET

def parse_xml_and_extract_products(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    products = []
    for item in root.findall("item"):
        product = {
            "external_id": item.findtext("g:id", default=""),
            "sku": item.findtext("g:mpn", default=""),
            "title": item.findtext("title"),
            "description": item.findtext("description", default=""),
            "price": item.findtext("g:price", default="0").replace(" TRY", "").replace(",", ""),
            "image_url": item.findtext("g:image_link", default=""),
            "category": item.findtext("g:product_type", default=""),
            "product_url": item.findtext("link", default="")  # 🔥 en önemlisi bu
        }
        products.append(product)
    return products
