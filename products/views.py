import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from products.models import Product, WidgetProductSelection

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
            error_list = []

            for i, item in enumerate(items):
                try:
                    ns = "{http://base.google.com/ns/1.0}"
                    external_id = item.find(f"{ns}id").text.strip()
                    title = item.find("title").text.strip()
                    price_raw = item.find(f"{ns}price").text.strip()
                    price = float(price_raw.split()[0])
                    image_url = item.find(f"{ns}image_link").text.strip()
                    sku_elem = item.find(f"{ns}mpn")  # 🧠 DÜZENLENDİ
                    sku = sku_elem.text.strip() if sku_elem is not None else None

                    Product.objects.update_or_create(
                        external_id=external_id,
                        defaults={
                            "name": title[:255],
                            "sku": sku[:100] if sku else None,
                            "price": price,
                            "image_url": image_url[:2000],
                            "description": "",
                            "category": ""
                        }
                    )
                    success_count += 1

                except Exception as e:
                    error_msg = f"[{i}] {external_id if 'external_id' in locals() else 'N/A'}: {str(e)}"
                    print("❌", error_msg)
                    error_list.append(error_msg)

            return JsonResponse({
                "status": "success",
                "message": f"{success_count} ürün başarıyla yüklendi.",
                "errors": error_list[:10],
                "fail_count": len(error_list)
            })

        except Exception as e:
            print("🌋 Genel XML parse hatası:", e)
            return JsonResponse({"status": "error", "error": str(e)}, status=500)

    return JsonResponse({"status": "error", "error": "POST methodu bekleniyor"}, status=405)


def widget_products(request):
    selected = WidgetProductSelection.objects.select_related("product").all()
    data = [{
        "name": s.product.name,
        "image_url": s.product.image_url,
        "price": str(s.product.price),
        "sku": s.product.sku,
        "url": f"https://www.sinapirlanta.com/urun/{s.product.sku}"  # Gerçek URL yapınıza göre ayarla
    } for s in selected]
    return JsonResponse({"products": data})