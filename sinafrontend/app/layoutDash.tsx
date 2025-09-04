"use client";
import { ReactNode, useState } from "react";
import Link from "next/link";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div
        className={`bg-pink-200 text-white w-64 p-6 space-y-4 fixed h-full transition-transform duration-300 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-64"
        } md:translate-x-0`}
      >
        
        <img 
  src="https://www.sinapirlanta.com/themes/custom/sina/logo.svg" 
  alt="Sina Pırlanta" 
  className="h-12 mb-6"
/>

    <nav className="flex flex-col gap-3">
  <Link href="/dashboard" className="hover:bg-gray-700 p-2 rounded text-black">
    Dashboard
  </Link>
  <Link href="/sepete-eklemeler" className="hover:bg-gray-700 p-2 rounded text-black">
    Sepete Eklemeler
  </Link>
  <Link href="/reports" className="hover:bg-gray-700 p-2 rounded text-black">
    Aboneler
  </Link>
  <Link href="/settings" className="hover:bg-gray-700 p-2 rounded text-black">
    Hoşgedin Mail 
  </Link>
  <Link href="/settings" className="hover:bg-gray-700 p-2 rounded text-black">
    Sepetinde Ürün Kaldı 
  </Link>
</nav>

      </div>

      {/* Main Content */}
      <div className="flex-1 ml-0 md:ml-64 flex flex-col">
        {/* Navbar */}
        <div className="flex items-center justify-between bg-white shadow px-6 py-4">
          {/* Sidebar toggle button (mobil) */}
          <button
            className="md:hidden bg-gray-800 text-white px-3 py-1 rounded"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? "Kapat" : "Menü"}
          </button>
          <h1 className="text-xl font-bold">Dashboard Başlığı</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">Hoşgeldin, Berk</span>
            <img
              src="https://via.placeholder.com/32"
              alt="Avatar"
              className="rounded-full"
            />
          </div>
        </div>

        {/* Page Content */}
        <main className="p-6 overflow-y-auto flex-1 bg-gray-50">{children}</main>
      </div>
    </div>
  );
}
