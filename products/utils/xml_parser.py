import xml.etree.ElementTree as ET

def parse_xml_and_extract_products(xml_file):
    import xml.etree.ElementTree as ET
    tree = ET.parse(xml_file)
    root = tree.getroot()

    products = []
    for item in root.findall("product"):
        product = {
            "external_id": item.findtext("id", default=""),
            "sku": item.findtext("sku") or item.findtext("mpn") or item.findtext("id"),
            "title": item.findtext("name"),
            "description": item.findtext("description", default=""),
            "price": item.findtext("price"),
            "image_url": item.findtext("image"),
            "category": item.findtext("category", default=""),
            "product_url": item.findtext("product_url") or item.findtext("link") or "",  # 🟢 buraya dikkat
        }
        products.append(product)
    return products