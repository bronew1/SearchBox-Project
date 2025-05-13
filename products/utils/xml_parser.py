import xml.etree.ElementTree as ET

def parse_xml_and_extract_products(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    products = []
    for item in root.findall("product"):
        product = {
            "external_id": item.findtext("id", default=""),  # Eğer id yoksa boş bırak
            "title": item.findtext("name"),
            "description": item.findtext("description", default=""),
            "price": item.findtext("price"),
            "image_url": item.findtext("image"),
            "category": item.findtext("category", default=""),
        }
        products.append(product)
    return products
