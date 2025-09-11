from datetime import date
from typing import List, Dict
from django.conf import settings
from google.ads.googleads.client import GoogleAdsClient

def _client_from_refresh_token(refresh_token: str, login_customer_id: str | None = None) -> GoogleAdsClient:
    cfg = {
        "developer_token": settings.GOOGLE_ADS["developer_token"],
        "client_id": settings.GOOGLE_ADS["client_id"],
        "client_secret": settings.GOOGLE_ADS["client_secret"],
        "refresh_token": refresh_token,
        # ✅ MCC (manager account) ID her zaman zorunlu
        "login_customer_id": str(login_customer_id or settings.GOOGLE_ADS.get("login_customer_id")),
        "use_proto_plus": True,
    }
    return GoogleAdsClient.load_from_dict(cfg)

def list_accessible_customers(refresh_token: str) -> List[str]:
    client = _client_from_refresh_token(refresh_token, login_customer_id=settings.GOOGLE_ADS["login_customer_id"])
    service = client.get_service("CustomerService")
    res = service.list_accessible_customers()
    return [r.split("/")[-1] for r in res.resource_names]

def get_customer_metadata(refresh_token: str, customer_id: str) -> Dict:
    client = _client_from_refresh_token(refresh_token, login_customer_id=settings.GOOGLE_ADS["login_customer_id"])
    ga = client.get_service("GoogleAdsService")
    query = """
    SELECT customer.id, customer.descriptive_name, customer.currency_code
    FROM customer
    """
    rows = ga.search(customer_id=customer_id, query=query)
    for r in rows:
        return {
            "customer_id": str(r.customer.id),
            "descriptive_name": r.customer.descriptive_name,
            "currency_code": r.customer.currency_code,
        }
    return {"customer_id": customer_id, "descriptive_name": None, "currency_code": None}

def stream_campaign_daily(refresh_token: str, customer_id: str, start: date, end: date):
    client = _client_from_refresh_token(refresh_token, login_customer_id=settings.GOOGLE_ADS["login_customer_id"])
    ga = client.get_service("GoogleAdsService")
    query = f"""
    SELECT
      campaign.id,
      campaign.name,
      segments.date,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value
    FROM campaign
    WHERE segments.date BETWEEN '{start}' AND '{end}'
    """
    return ga.search_stream(customer_id=customer_id, query=query)
