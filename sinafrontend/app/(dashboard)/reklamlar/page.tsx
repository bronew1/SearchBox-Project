from django.conf import settings
from google.ads.googleads.client import GoogleAdsClient

def get_client() -> GoogleAdsClient:
    cfg = {
        "developer_token": settings.GOOGLE_ADS["developer_token"],
        "client_id": settings.GOOGLE_ADS["client_id"],
        "client_secret": settings.GOOGLE_ADS["client_secret"],
        "refresh_token": settings.GOOGLE_ADS["refresh_token"],
        "login_customer_id": settings.GOOGLE_ADS["login_customer_id"],
        "use_proto_plus": True,
    }
    return GoogleAdsClient.load_from_dict(cfg)

def get_campaign_metrics(start_date: str, end_date: str):
    client = get_client()
    ga_service = client.get_service("GoogleAdsService")

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
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
    """

    rows = ga_service.search(
        customer_id=settings.GOOGLE_ADS["customer_id"],
        query=query
    )

    results = []
    for r in rows:
        results.append({
            "date": r.segments.date,
            "campaign_id": r.campaign.id,
            "campaign_name": r.campaign.name,
            "impressions": r.metrics.impressions,
            "clicks": r.metrics.clicks,
            "cost": r.metrics.cost_micros / 1_000_000,
            "conversions": r.metrics.conversions,
            "revenue": r.metrics.conversions_value,
        })
    return results
