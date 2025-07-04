import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from products.models import Product, WidgetProduct
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from products.serializers import WidgetProductSerializer
from .models import WidgetProduct
import json

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




@csrf_exempt
def widget_products(request, id=None):
    if request.method == "GET":
        if id:
            try:
                p = WidgetProduct.objects.get(id=id)
                data = {
                    "id": p.id,
                    "name": p.name,
                    "image_url": p.image_url,
                    "hover_image_url": p.hover_image_url,
                    "price": p.price,
                    "product_url": p.product_url,
                    "sku": p.sku,
                    "order": p.order,
                }
                return JsonResponse(data)
            except WidgetProduct.DoesNotExist:
                return JsonResponse({"error": "Not found"}, status=404)
        else:
            products = WidgetProduct.objects.all()
            data = []
            for p in products:
                data.append({
                    "id": p.id,
                    "name": p.name,
                    "image_url": p.image_url,
                    "hover_image_url": p.hover_image_url,
                    "price": p.price,
                    "product_url": p.product_url,
                    "sku": p.sku,
                    "order": p.order,
                })
            return JsonResponse(data, safe=False)

    elif request.method == "POST":
        data = json.loads(request.body)
        p = WidgetProduct.objects.create(
            name=data.get("name"),
            image_url=data.get("image_url"),
            hover_image_url=data.get("hover_image_url"),
            price=data.get("price"),
            product_url=data.get("product_url"),
            sku=data.get("sku"),
            order=data.get("order", 0),
        )
        return JsonResponse({"status": "success", "id": p.id})

    elif request.method == "PUT":
        data = json.loads(request.body)
        p = WidgetProduct.objects.get(id=data.get("id"))
        p.name = data.get("name", p.name)
        p.image_url = data.get("image_url", p.image_url)
        p.hover_image_url = data.get("hover_image_url", p.hover_image_url)
        p.price = data.get("price", p.price)
        p.product_url = data.get("product_url", p.product_url)
        p.sku = data.get("sku", p.sku)
        p.order = data.get("order", p.order)
        p.save()
        return JsonResponse({"status": "success"})

    elif request.method == "DELETE":
        p = WidgetProduct.objects.get(id=id)
        p.delete()
        return JsonResponse({"status": "deleted"})

    return JsonResponse({"error": "Method not allowed"}, status=405)



class WidgetProductViewSet(viewsets.ModelViewSet):
    queryset = WidgetProduct.objects.all().order_by("order")
    serializer_class = WidgetProductSerializer