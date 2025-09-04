"use client";
import { useEffect, useState } from "react";
import * as XLSX from "xlsx";

interface Subscriber {
  email: string;
  subscribed_at: string;
}

export default function AbonelerPage() {
  const [subscribers, setSubscribers] = useState<Subscriber[]>([]);
  const [filteredSubscribers, setFilteredSubscribers] = useState<Subscriber[]>([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  useEffect(() => {
    fetch("https://searchprojectdemo.com/api/subscribe/")
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setSubscribers(data);
          setFilteredSubscribers(data); // İlk yüklemede tümünü göster
        } else {
          setSubscribers([]);
          setFilteredSubscribers([]);
        }
      })
      .catch((err) => {
        console.error("API error:", err);
        setSubscribers([]);
        setFilteredSubscribers([]);
      });
  }, []);

  const applyDateFilter = () => {
    if (!startDate || !endDate) {
      setFilteredSubscribers(subscribers);
      return;
    }

    const start = new Date(startDate);
    const end = new Date(endDate);

    const filtered = subscribers.filter((sub) => {
      const date = new Date(sub.subscribed_at);
      return date >= start && date <= end;
    });

    setFilteredSubscribers(filtered);
  };

  const exportToExcel = () => {
    const data = filteredSubscribers.map((sub, index) => ({
      "#": index + 1,
      Email: sub.email,
      "Kayıt Tarihi": new Date(sub.subscribed_at).toLocaleString("tr-TR"),
    }));

    const worksheet = XLSX.utils.json_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Aboneler");

    XLSX.writeFile(workbook, "aboneler.xlsx");
  };

  return (
    <div className="max-w-4xl mx-auto py-10 bg-white rounded-lg shadow-lg p-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Abone Olan Kullanıcılar</h2>
        <button
          onClick={exportToExcel}
          className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
        >
          Excel'e Aktar
        </button>
      </div>

      {/* Tarih Aralığı */}
      <div className="flex gap-4 mb-4">
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="border rounded p-2"
        />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="border rounded p-2"
        />
        <button
          onClick={applyDateFilter}
          className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded"
        >
          Uygula
        </button>
      </div>

      {/* Liste */}
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead>
            <tr>
              <th className="py-3 px-4 border-b text-left">#</th>
              <th className="py-3 px-4 border-b text-left">E-mail</th>
              <th className="py-3 px-4 border-b text-left">Kayıt Tarihi</th>
            </tr>
          </thead>
          <tbody>
            {filteredSubscribers.map((sub, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="py-2 px-4 border-b">{index + 1}</td>
                <td className="py-2 px-4 border-b">{sub.email}</td>
                <td className="py-2 px-4 border-b">
                  {new Date(sub.subscribed_at).toLocaleString("tr-TR", {
                    year: "numeric",
                    month: "2-digit",
                    day: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </td>
              </tr>
            ))}
            {filteredSubscribers.length === 0 && (
              <tr>
                <td className="py-2 px-4 text-center" colSpan={3}>
                  Kayıtlı abone bulunamadı.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
