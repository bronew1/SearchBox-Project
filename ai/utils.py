from django.db import connection
from sentence_transformers import SentenceTransformer

# Yerel model (384 boyutlu)
_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def semantic_search(query: str, k: int = 5):
    """Kullanıcı sorusunu encode edip pgvector üzerinden en yakın içerikleri getirir"""
    qvec = _model.encode([query], convert_to_numpy=True).tolist()[0]

    with connection.cursor() as cur:
        cur.execute("""
            select id, title, content
            from ai_documents
            order by embedding <=> %s::vector
            limit %s
        """, (str(qvec), k))
        rows = cur.fetchall()

    return [{"id": r[0], "title": r[1], "content": r[2]} for r in rows]


def run_sql_metrics(metric: str, start_date: str, end_date: str, limit: int = 10):
    """Ön tanımlı metrikler için güvenli SQL sorgusu"""
    metric_map = {
        "views": "sum(case when event_name='view_item' then event_count else 0 end)",
        "adds": "sum(case when event_name='add_to_cart' then event_count else 0 end)",
        "purchases": "sum(case when event_name='purchase' then event_count else 0 end)",
        "roas": "avg(roas)",
        "clicks": "sum(clicks)",
        "cost": "sum(cost)",
        "revenue": "sum(revenue)",
    }

    if metric not in metric_map:
        return {"error": "Desteklenmeyen metric"}

    if metric in ["roas","clicks","cost","revenue"]:
        table = "daily_ads"
    else:
        table = "daily_events"

    sql = f"""
        select day, {metric_map[metric]} as value
        from {table}
        where day between %s and %s
        group by 1
        order by 1 desc
        limit %s
    """

    with connection.cursor() as cur:
        cur.execute(sql, (start_date, end_date, limit))
        rows = cur.fetchall()

    return [{"day": str(r[0]), "value": float(r[1]) if r[1] is not None else None} for r in rows]
