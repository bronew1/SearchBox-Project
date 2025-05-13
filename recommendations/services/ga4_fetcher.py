from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, Dimension, RunReportRequest
from google.oauth2 import service_account
from products.models import Product

GA4_JSON_KEY_PATH = "credentials/ga4-service-account.json"
PROPERTY_ID = "313316187"  # Buraya gerçek GA4 Property ID'ni koy

credentials = service_account.Credentials.from_service_account_file(
    GA4_JSON_KEY_PATH,
    scopes=["https://www.googleapis.com/auth/analytics.readonly"],
)

client = BetaAnalyticsDataClient(credentials=credentials)

def get_top_products(event_type="purchase", limit=10):
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[
            Dimension(name="customEvent:event_title"),
            Dimension(name="customEvent:event_action"),
        ],
        metrics=[
            Metric(name="eventCount")
        ],
        date_ranges=[
            DateRange(start_date="28daysAgo", end_date="today")
        ],
        limit=limit
    )

    response = client.run_report(request)

    results = []

    for row in response.rows:
        product_title = row.dimension_values[0].value
        event_action = row.dimension_values[1].value

        print(f"[GA4] {event_action} → {product_title}")

        product = Product.objects.filter(title__icontains=product_title).first()

        if not product:
            print(f"Eşleşmeyen ürün: {product_title}")
            continue

        results.append({
            "title": product.title,
            "price": float(product.price),
            "image_url": product.image_url,
            "product_id": product.external_id,
        })

    return results