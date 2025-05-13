import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from google.oauth2 import service_account

def fetch_search_terms(property_id: str):
    key_path = os.path.join(os.path.dirname(__file__), "ga4-key.json")  # JSON dosyanı buraya koy
    credentials = service_account.Credentials.from_service_account_file(key_path)

    client = BetaAnalyticsDataClient(credentials=credentials)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="searchTerm")],
        metrics=[Metric(name="eventCount")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
    )

    response = client.run_report(request)

    return [
        {
            "search_term": row.dimension_values[0].value,
            "count": row.metric_values[0].value
        }
        for row in response.rows
    ]
