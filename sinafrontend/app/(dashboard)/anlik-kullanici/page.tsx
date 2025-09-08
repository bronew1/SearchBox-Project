"use client";

import { useEffect, useMemo, useState, ReactNode } from "react";

type UserEvent = {
  id: number;
  event_name: string;
  product_id: string;
  user_id: string;
  event_value?: string | null;
  source?: string | null;
  utm_source?: string | null;
  utm_medium?: string | null;
  utm_campaign?: string | null;
  utm_term?: string | null;
  utm_content?: string | null;
  timestamp: string;
};

// Basit yardımcı hücreler
function Th({
  children,
  align = "left",
}: {
  children: ReactNode;
  align?: "left" | "center" | "right";
}) {
  const alignCls =
    align === "right" ? "text-right" : align === "center" ? "text-center" : "text-left";
  return <th className={`px-4 py-2 ${alignCls}`}>{children}</th>;
}

function Td({
  children,
  align = "left",
  className = "",
  title,
}: {
  children: ReactNode;
  align?: "left" | "center" | "right";
  className?: string;
  title?: string;
}) {
  const alignCls =
    align === "right" ? "text-right" : align === "center" ? "text-center" : "text-left";
  return (
    <td
      title={title}
      className={`px-4 py-2 text-[13px] text-gray-700 ${alignCls} ${className}`}
    >
      {children}
    </td>
  );
}

function formatCurrencyTRY(value?: string | null) {
  if (value == null || value === "") return "-";
  const num = Number(value);
  if (Number.isNaN(num)) return value;
  try {
    return new Intl.NumberFormat("tr-TR", {
      style: "currency",
      currency: "TRY",
      maximumFractionDigits: 2,
    }).format(num);
  } catch {
    return value;
  }
}

// ✅ Türkiye saatine göre formatlama
function formatTS(ts?: string | null) {
  if (!ts) return "-";

  try {
    const d = new Date(ts);
    if (Number.isNaN(d.getTime())) return ts;

    return d.toLocaleString("tr-TR", {
      timeZone: "Europe/Istanbul",
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  } catch {
    return ts;
  }
}

export default function UserEventsTable() {
  const [events, setEvents] = useState<UserEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://searchprojectdemo.com/api/user-events/")
      .then((res) => res.json())
      .then((data: UserEvent[]) => setEvents(Array.isArray(data) ? data : []))
      .catch((err) => console.error("Event fetch error:", err))
      .finally(() => setLoading(false));
  }, []);

  const rows = useMemo(
    () =>
      events.map((ev) => ({
        id: ev.id,
        event: ev.event_name,
        productId: ev.product_id || "-",
        userId: ev.user_id || "-",
        eventValue: formatCurrencyTRY(ev.event_value),
        source: ev.source || "-",
        utmSource: ev.utm_source,
        utmMedium: ev.utm_medium,
        utmCampaign: ev.utm_campaign,
        utmTerm: ev.utm_term,
        utmContent: ev.utm_content,
        timestamp: formatTS(ev.timestamp),
      })),
    [events]
  );

  return (
    <div className="rounded-2xl border border-gray-200 bg-white shadow-sm overflow-hidden">
      {/* Başlık */}
      <div className="px-5 py-4 border-b bg-white/70 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <h3 className="text-[15px] font-semibold text-gray-800">Kullanıcı Hareketleri</h3>
      </div>

      {/* Tablo alanı */}
      <div className="max-h-[70vh] overflow-auto">
        <table className="w-full text-sm">
          <thead className="sticky top-0 z-10 bg-white/80 backdrop-blur border-b">
            <tr className="text-[11px] uppercase tracking-wide text-gray-500">
              <Th>ID</Th>
              <Th>Event</Th>
              <Th>Product ID</Th>
              <Th>User ID</Th>
              <Th align="right">Event Value (Fiyat)</Th>
              <Th>Source</Th>
              <Th>UTM Source</Th>
              <Th>UTM Medium</Th>
              <Th>UTM Campaign</Th>
              <Th>UTM Term</Th>
              <Th>UTM Content</Th>
              <Th>Timestamp</Th>
            </tr>
          </thead>

          <tbody className="divide-y divide-gray-100">
            {loading && (
              <tr>
                <td colSpan={12} className="px-4 py-16 text-center">
                  <div className="flex justify-center">
                    <img
                      src="/sinagif.gif" // public/ klasöründe olmalı
                      alt="Yükleniyor..."
                      className="w-20 h-20"
                    />
                  </div>
                </td>
              </tr>
            )}

            {!loading && rows.length === 0 && (
              <tr>
                <td colSpan={12} className="px-4 py-8 text-center text-gray-500">
                  Kayıt bulunamadı
                </td>
              </tr>
            )}

            {!loading &&
              rows.map((r) => (
                <tr
                  key={String(r.id)}
                  className="odd:bg-gray-50/40 hover:bg-gray-50/70 transition-colors"
                >
                  <Td>
                    <span className="font-medium text-gray-900">{r.id}</span>
                  </Td>

                  <Td>
                    <span className="inline-flex items-center rounded-full bg-rose-50 px-2 py-0.5 text-[11px] font-medium text-rose-700">
                      {r.event}
                    </span>
                  </Td>

                  <Td className="max-w-[160px] truncate" title={r.productId}>
                    {r.productId}
                  </Td>

                  <Td className="max-w-[180px] truncate text-gray-700" title={r.userId}>
                    {r.userId}
                  </Td>

                  <Td align="right">
                    <span className="tabular-nums font-medium text-gray-900">
                      {r.eventValue}
                    </span>
                  </Td>

                  <Td>
                    <span className="inline-flex items-center rounded-full bg-emerald-50 px-2 py-0.5 text-[11px] font-medium text-emerald-700">
                      {r.source}
                    </span>
                  </Td>

                  <Td>{r.utmSource || <span className="text-gray-400">-</span>}</Td>
                  <Td>{r.utmMedium || <span className="text-gray-400">-</span>}</Td>

                  <Td className="max-w-[220px] truncate" title={r.utmCampaign || ""}>
                    {r.utmCampaign || <span className="text-gray-400">-</span>}
                  </Td>

                  <Td>{r.utmTerm || <span className="text-gray-400">-</span>}</Td>

                  <Td className="max-w-[200px] truncate" title={r.utmContent || ""}>
                    {r.utmContent || <span className="text-gray-400">-</span>}
                  </Td>

                  <Td>
                    <span className="whitespace-nowrap text-xs text-gray-500">
                      {r.timestamp}
                    </span>
                  </Td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
