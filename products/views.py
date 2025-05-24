import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from products.models import Product

@csrf_exempt
def upload_xml(request):
    if request.method == "POST":
        xml_file = request.FILES.get("file")
        if not xml_file:
            return JsonResponse({
                "status": "error",
                "error": "Dosya gelmedi. Lütfen 'file' adında form-data ile yükleyin."
            }, status=400)

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            items = root.find("channel").findall("item")
            success_count = 0
            error_count = 0
            errors = []

            for item in items:
                try:
                    external_id = item.find("{http://base.google.com/ns/1.0}id").text.strip()
                    name = item.find("title").text.strip()
                    price_raw = item.find("{http://base.google.com/ns/1.0}price").text
                    price = float(price_raw.split()[0])
                    image_url = item.find("{http://base.google.com/ns/1.0}image_link").text.strip()
                    sku_elem = item.find("{http://base.google.com/ns/1.0}sku")
                    sku = sku_elem.text.strip() if sku_elem is not None else None

                    Product.objects.update_or_create(
                        external_id=external_id,
                        defaults={
                            "name": name,
                            "sku": sku,
                            "price": price,
                            "image_url": image_url,
                            "description": "",
                            "category": ""
                        }
                    )
                    success_count += 1

                except Exception as e:
                    print(f"⚠️ Ürün hatası (id={external_id}):", e)
                    errors.append(f"id={external_id}: {e}")
                    error_count += 1
                    continue

            return JsonResponse({
                "status": "success",
                "message": f"{success_count} ürün başarıyla yüklendi, {error_count} ürün hatalı.",
                "success": success_count,
                "errors": errors[:5]  # ilk 5 hatayı dön
            })

        except Exception as e:
            print("❌ Parse hatası:", e)
            return JsonResponse({"status": "error", "error": str(e)}, status=500)

    return JsonResponse({"status": "error", "error": "POST methodu bekleniyor"}, status=405)
