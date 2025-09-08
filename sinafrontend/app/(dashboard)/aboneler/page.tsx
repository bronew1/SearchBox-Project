"use client";

import { useEffect, useState } from "react";

type Subscriber = {
  id: number;
  email: string;
  created_at: string;
};

export default function SubscribersPage() {
  const [subscribers, setSubscribers] = useState<Subscriber[]>([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  // Sayfa ilk açıldığında tüm aboneleri çek
  useEffect(() => {
    fetch("https://searchprojectdemo.com/api/subscribers/")
      .then((res) => res.json())
      .then((data) => setSubscribers(data))
      .catch((err) => console.error(err));
  }, []);

  const handleExport = () => {
    alert("Excel'e aktarma işlemi burada çalışacak.");
  };

  // ✅ Tarih aralığına göre filtreli aboneleri çek
  const handleApply = () => {
    if (!startDate || !endDate) {
      alert("Lütfen başlangıç ve bitiş tarihi seçin.");
      return;
    }

    fetch(
      `https://searchprojectdemo.com/api/subscribers/?start_date=${startDate}&end_date=${endDate}`
    )
      .then((res) => res.json())
      .then((data) => setSubscribers(data))
      .catch((err) => console.error(err));
  };

  return (
    <div className="p-6">
      {/* Başlık ve filtre */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <h1 className="text-2xl font-semibold text-gray-800">
          Abone Olan Kullanıcılar
        </h1>

        <div className="flex items-center gap-3">
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="border rounded-lg p-2 text-sm shadow-sm focus:ring-2 focus:ring-pink-400 focus:outline-none"
          />
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="border rounded-lg p-2 text-sm shadow-sm focus:ring-2 focus:ring-pink-400 focus:outline-none"
          />
          <button
            onClick={handleApply}
            className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded-lg text-sm shadow transition"
          >
            Uygula
          </button>
          <button
            onClick={handleExport}
            className="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg text-sm shadow transition"
          >
            Excel'e Aktar
          </button>
        </div>
      </div>

      {/* Tablo */}
      <div className="bg-white rounded-xl shadow border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                #
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                E-mail
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Kayıt Tarihi
              </th>
            </tr>
          </thead>
          <tbody>
            {subscribers.length === 0 ? (
              <tr>
                <td
                  colSpan={3}
                  className="px-4 py-6 text-center text-gray-500 text-sm"
                >
                  Henüz abone bulunmuyor
                </td>
              </tr>
            ) : (
              subscribers.map((s, idx) => (
                <tr
                  key={s.id}
                  className="border-b hover:bg-gray-50 transition-colors"
                >
                  <td className="px-4 py-3 text-gray-700">{idx + 1}</td>
                  <td className="px-4 py-3 font-medium text-gray-900">
                    {s.email}
                  </td>
                  <td className="px-4 py-3 text-gray-600">
                    {new Date(s.created_at).toLocaleString("tr-TR")}
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
