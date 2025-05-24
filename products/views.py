import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Product

@csrf_exempt
def upload_xml(request):
    if request.method == "POST":
        print("✅ POST geldi")
        print("📂 Gelen dosyalar:", request.FILES)

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
            count = 0

            for item in items:
                try:
                    external_id = item.find("{http://base.google.com/ns/1.0}id").text
                    title = item.find("title").text
                    price_raw = item.find("{http://base.google.com/ns/1.0}price").text
                    price = float(price_raw.split()[0])
                    image_url = item.find("{http://base.google.com/ns/1.0}image_link").text

                    Product.objects.update_or_create(
    external_id=external_id,
    defaults={
        "name": title,  # <-- DÜZELTİLDİ
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
                "message": f"{count} ürün başarıyla yüklendi.",
                "count": count
            })

        except Exception as e:
            print("❌ Parse hatası:", e)
            return JsonResponse({"status": "error", "error": str(e)}, status=500)

    return JsonResponse({"status": "error", "error": "POST methodu bekleniyor"}, status=405)
