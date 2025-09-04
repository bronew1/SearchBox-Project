"use client";

import { useEffect, useState } from "react";

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

export default function UserEventsTable() {
  const [events, setEvents] = useState<UserEvent[]>([]);

  useEffect(() => {
    fetch("https://searchprojectdemo.com/api/user-events/")
      .then((res) => res.json())
      .then((data) => setEvents(data))
      .catch((err) => console.error("Event fetch error:", err));
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Kullanıcı Hareketleri</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full border text-sm">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-2 py-1">ID</th>
              <th className="border px-2 py-1">Event</th>
              <th className="border px-2 py-1">Product ID</th>
              <th className="border px-2 py-1">User ID</th>
              <th className="border px-2 py-1">Event Value (Fiyat)</th>
              <th className="border px-2 py-1">Source</th>
              <th className="border px-2 py-1">UTM Source</th>
              <th className="border px-2 py-1">UTM Medium</th>
              <th className="border px-2 py-1">UTM Campaign</th>
              <th className="border px-2 py-1">UTM Term</th>
              <th className="border px-2 py-1">UTM Content</th>
              <th className="border px-2 py-1">Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {events.length === 0 ? (
              <tr>
                <td colSpan={12} className="border px-2 py-2 text-center">
                  Kayıt bulunamadı
                </td>
              </tr>
            ) : (
              events.map((ev) => (
                <tr key={ev.id}>
                  <td className="border px-2 py-1">{ev.id}</td>
                  <td className="border px-2 py-1">{ev.event_name}</td>
                  <td className="border px-2 py-1">{ev.product_id || "-"}</td>
                  <td className="border px-2 py-1">{ev.user_id || "-"}</td>
                  <td className="border px-2 py-1">{ev.event_value || "-"}</td>
                  <td className="border px-2 py-1">{ev.source || "-"}</td>
                  <td className="border px-2 py-1">{ev.utm_source || "-"}</td>
                  <td className="border px-2 py-1">{ev.utm_medium || "-"}</td>
                  <td className="border px-2 py-1">{ev.utm_campaign || "-"}</td>
                  <td className="border px-2 py-1">{ev.utm_term || "-"}</td>
                  <td className="border px-2 py-1">{ev.utm_content || "-"}</td>
                  <td className="border px-2 py-1">
                    {ev.timestamp
                      ? new Date(ev.timestamp).toLocaleString("tr-TR", {
                          timeZone: "Europe/Istanbul",
                        })
                      : "-"}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
