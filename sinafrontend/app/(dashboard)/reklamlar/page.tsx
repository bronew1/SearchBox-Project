"use client";

import { useEffect, useState } from "react";

type Account = { id:number; customer_id:string; name:string; currency:string };
type MetricRow = {
  date: string; campaign_id: string; campaign_name: string;
  impressions: number; clicks: number; cost: number; conversions: number; revenue: number;
};

const BACKEND = process.env.NEXT_PUBLIC_BACKEND || "http://localhost:8000";

export default function GoogleAdsPage() {
  const [connected, setConnected] = useState(false);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [selected, setSelected] = useState<string>("");
  const [start, setStart] = useState<string>("");
  const [end, setEnd] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [rows, setRows] = useState<MetricRow[]>([]);
  const [summary, setSummary] = useState<{
    impressions:number; clicks:number; cost:number; revenue:number; roas:number|null
  }>();

  useEffect(() => {
    fetch(`${BACKEND}/api/ads/accounts/`, { credentials: "include" })
      .then(r => r.json())
      .then(d => {
        setConnected(!!d.connected);
        setAccounts(d.accounts || []);
        if (d.accounts?.[0]) setSelected(d.accounts[0].customer_id);
      });
  }, []);

  const connect = () => {
    // ✅ backend tarafındaki doğru endpoint: /api/ads/google-auth/
    window.location.href = `${BACKEND}/api/ads/google-auth/`;
  };

  const syncData = async () => {
    if (!selected) return;
    setLoading(true);
    await fetch(`${BACKEND}/api/ads/sync/`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ customer_id: selected, start: start || undefined, end: end || undefined }),
      credentials: "include"
    }).then(r => r.json());
    setLoading(false);
    await loadMetrics();
  };

  const loadMetrics = async () => {
    if (!selected) return;
    setLoading(true);
    const params = new URLSearchParams({ customer_id: selected });
    if (start) params.append("start", start);
    if (end) params.append("end", end);
    const d = await fetch(`${BACKEND}/api/ads/metrics/?${params.toString()}`, { credentials:"include" }).then(r => r.json());
    setRows(d.rows || []);
    setSummary(d.summary);
    setLoading(false);
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Google Ads</h1>
        {!connected ? (
          <button onClick={connect} className="px-4 py-2 rounded-xl bg-black text-white">
            Google ile Bağlan
          </button>
        ) : (
          <span className="text-green-700 font-medium">Bağlı</span>
        )}
      </div>

      <div className="grid md:grid-cols-4 gap-3">
        <div className="col-span-2">
          <label className="text-sm text-gray-600">Hesap</label>
          <select value={selected} onChange={e=>setSelected(e.target.value)} className="w-full rounded-xl border p-2">
            {accounts.map(a => (
              <option key={a.customer_id} value={a.customer_id}>
                {a.name || a.customer_id} ({a.currency || "?"})
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="text-sm text-gray-600">Başlangıç</label>
          <input type="date" value={start} onChange={e=>setStart(e.target.value)} className="w-full rounded-xl border p-2"/>
        </div>
        <div>
          <label className="text-sm text-gray-600">Bitiş</label>
          <input type="date" value={end} onChange={e=>setEnd(e.target.value)} className="w-full rounded-xl border p-2"/>
        </div>
      </div>

      <div className="flex gap-3">
        <button onClick={syncData} disabled={!selected || loading} className="px-4 py-2 rounded-xl bg-indigo-600 text-white disabled:opacity-50">
          {loading ? "İşleniyor..." : "Verileri Senkronize Et"}
        </button>
        <button onClick={loadMetrics} disabled={!selected || loading} className="px-4 py-2 rounded-xl border">
          Tabloyu Yükle
        </button>
      </div>

      {summary && (
        <div className="grid md:grid-cols-4 gap-4">
          <Stat title="Gösterim" value={summary.impressions.toLocaleString()} />
          <Stat title="Tıklama" value={summary.clicks.toLocaleString()} />
          <Stat title="Maliyet" value={summary.cost.toFixed(2)} />
          <Stat title="ROAS" value={summary.roas != null ? summary.roas.toFixed(2) : "-"} />
        </div>
      )}

      <div className="overflow-auto rounded-xl border">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <Th>Tarih</Th><Th>Kampanya</Th><Th>Imp</Th><Th>Clk</Th>
              <Th>Maliyet</Th><Th>Dönüşüm</Th><Th>Gelir</Th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i} className="odd:bg-white even:bg-gray-50">
                <Td>{r.date}</Td>
                <Td className="max-w-[360px] truncate" title={r.campaign_name}>
                  {r.campaign_name}
                </Td>
                <Td>{r.impressions}</Td>
                <Td>{r.clicks}</Td>
                <Td>{r.cost.toFixed(2)}</Td>
                <Td>{r.conversions}</Td>
                <Td>{r.revenue}</Td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr>
                <td className="p-4 text-gray-500" colSpan={7}>Henüz veri yok.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Stat({title, value}:{title:string; value:string}) {
  return (
    <div className="rounded-2xl border p-4">
      <div className="text-gray-500 text-sm">{title}</div>
      <div className="text-xl font-semibold">{value}</div>
    </div>
  );
}

function Th({children}:{children:React.ReactNode}) {
  return <th className="text-left p-3 font-semibold">{children}</th>;
}

function Td({children, className, title}:{
  children: React.ReactNode;
  className?: string;
  title?: string;
}) {
  return <td className={`p-3 ${className||""}`} title={title}>{children}</td>;
}
