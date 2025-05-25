from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import xml.etree.ElementTree as ET
from products.models import Product

@csrf_exempt
def upload_xml(request):
    if request.method == "POST":
        xml_file = request.FILES.get("file")
        if not xml_file:
            return JsonResponse({"status": "error", "error": "Dosya gelmedi"}, status=400)

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            items = root.find("channel").findall("item")

            count = 0
            for item in items:
                try:
                    external_id = item.find("{http://base.google.com/ns/1.0}id").text.strip()
                    name = item.find("title").text.strip()
                    price = float(item.find("{http://base.google.com/ns/1.0}price").text.strip().split()[0])
                    image_url = item.find("{http://base.google.com/ns/1.0}image_link").text.strip()
                    sku_elem = item.find("{http://base.google.com/ns/1.0}mpn")  # SKU yerine MPN (kullanıcıya görünen kod)
                    sku = sku_elem.text.strip() if sku_elem is not None else None

                    Product.objects.update_or_create(
                        external_id=external_id,
                        defaults={
                            "sku": sku,
                            "name": name,
                            "price": price,
                            "image_url": image_url,
                            "description": "",
                            "category": ""
                        }
                    )
                    count += 1
                except Exception as e:
                    print("⚠️ Ürün hatası:", e)
                    continue

            return JsonResponse({
                "status": "success",
                "message": f"{count} ürün başarıyla yüklendi."
            })

        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)}, status=500)

    return JsonResponse({"status": "error", "error": "POST methodu bekleniyor"}, status=405)
