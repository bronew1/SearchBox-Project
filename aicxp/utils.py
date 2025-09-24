from django.db import connection
from sentence_transformers import SentenceTransformer

# Yerel embedding modeli (384 boyutlu vektörler üretir)
_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def semantic_search(query: str, k: int = 5):
    """
    Kullanıcıdan gelen arama sorgusunu encode edip
    pgvector üzerinden en yakın ürünleri döndürür.
    """
    qvec = _model.encode([query], convert_to_numpy=True).tolist()[0]

    with connection.cursor() as cur:
        cur.execute("""
            SELECT id, title, content
            FROM ai_documents
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (str(qvec), k))
        rows = cur.fetchall()

    return [
        {"id": r[0], "title": r[1], "content": r[2]}
        for r in rows
    ]


def run_sql_metrics(metric: str, start_date: str, end_date: str, limit: int = 10):
    """
    Panelde topladığın event verilerini (view_item, add_to_cart, purchase, ads verileri)
    güvenli SQL ile sorgulamak için kullanılır.
    """
    metric_map = {
        "views": "SUM(CASE WHEN event_name='view_item' THEN event_count ELSE 0 END)",
        "adds": "SUM(CASE WHEN event_name='add_to_cart' THEN event_count ELSE 0 END)",
        "purchases": "SUM(CASE WHEN event_name='purchase' THEN event_count ELSE 0 END)",
        "roas": "AVG(roas)",
        "clicks": "SUM(clicks)",
        "cost": "SUM(cost)",
        "revenue": "SUM(revenue)",
    }

    if metric not in metric_map:
        return {"error": f"Desteklenmeyen metric: {metric}"}

    # Ads metrikleri ayrı tabloda tutuluyorsa kontrol
    if metric in ["roas", "clicks", "cost", "revenue"]:
        table = "daily_ads"
    else:
        table = "daily_events"

    sql = f"""
        SELECT day, {metric_map[metric]} AS value
        FROM {table}
        WHERE day BETWEEN %s AND %s
        GROUP BY 1
        ORDER BY 1 DESC
        LIMIT %s
    """

    with connection.cursor() as cur:
        cur.execute(sql, (start_date, end_date, limit))
        rows = cur.fetchall()

    return [
        {"day": str(r[0]), "value": float(r[1]) if r[1] is not None else None}
        for r in rows
    ]


def top_cart_product():
    """
    En çok sepete eklenen ürünü döndürür.
    """
    sql = """
        SELECT product_id, COUNT(*) as cnt
        FROM tracking_userevent
        WHERE event_name = 'add_to_cart'
        GROUP BY product_id
        ORDER BY cnt DESC
        LIMIT 1;
    """

    with connection.cursor() as cur:
        cur.execute(sql)
        row = cur.fetchone()

    if row:
        return {"product_id": row[0], "adds": row[1]}
    return None


def top_products(event_name: str = "add_to_cart", limit: int = 5):
    """
    Belirli bir evente göre (ör: add_to_cart, view_item, purchase)
    en çok yapılan ürünleri getirir.
    """
    sql = """
        SELECT product_id, COUNT(*) AS cnt
        FROM tracking_userevent
        WHERE event_name = %s
        GROUP BY product_id
        ORDER BY cnt DESC
        LIMIT %s
    """

    with connection.cursor() as cur:
        cur.execute(sql, [event_name, limit])
        rows = cur.fetchall()

    return [
        {"product_id": r[0], "count": r[1]}
        for r in rows
    ]
