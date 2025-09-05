"use client";

import { ReactNode, useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import type { Route } from "next"; // ✅ Route tipini import ettik

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const cookies = document.cookie.split(";").map((c) => c.trim());
    const token = cookies.find((c) => c.startsWith("accessToken="));

    if (!token) {
      router.replace("/login"); // token yoksa login'e yönlendir
    }
  }, [router]);

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div
        className={`bg-pink-200 text-white p-4 space-y-4 transition-all duration-300 flex flex-col ${
          sidebarOpen ? "w-64" : "w-20"
        }`}
      >
        <img
          src="https://www.sinapirlanta.com/themes/custom/sina/logo.svg"
          alt="Sina Pırlanta"
          className={`h-12 mx-auto transition-opacity duration-300 ${
            sidebarOpen ? "opacity-100" : "opacity-0"
          }`}
        />
        <nav className="flex flex-col gap-3 mt-4">
          <SidebarLink href="/dashboard" icon="🏠" text="Dashboard" open={sidebarOpen} />
          <SidebarLink href="/anlik-kullanici" icon="👤" text="Anlık Kullanıcılar" open={sidebarOpen} />
          <SidebarLink href="/campaigns" icon="📣" text="Kampanyalar" open={sidebarOpen} />
          <SidebarLink href="/reklamlar" icon="📊" text="Reklamlar" open={sidebarOpen} />
          <SidebarLink href="/aboneler" icon="👥" text="Aboneler" open={sidebarOpen} />
          <SidebarLink href="/sepete-eklemeler" icon="🛒" text="Sepete Eklemeler" open={sidebarOpen} />
          <SidebarLink href="/welcome-template" icon="✉️" text="Hoşgeldin Maili" open={sidebarOpen} />
          <SidebarLink href="/widgets" icon="🧩" text="Widgets" open={sidebarOpen} />
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Navbar */}
        <div className="flex items-center justify-between bg-white shadow px-4 py-3">
          <button
            className="bg-gray-800 text-white px-3 py-1 rounded"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? "✖" : "☰"}
          </button>
          <h1 className="text-lg font-bold">Sina Pırlanta Customer Experience Platform</h1>
          <div className="flex items-center space-x-3">
            <span className="text-gray-700">Hoşgeldin, Berk</span>
            <img src="https://via.placeholder.com/32" alt="Avatar" className="rounded-full" />
          </div>
        </div>

        {/* Page Content */}
        <main className="p-6 overflow-y-auto flex-1 bg-gray-50">{children}</main>
      </div>
    </div>
  );
}

function SidebarLink({
  href,
  icon,
  text,
  open,
}: {
  href: string;
  icon: string;
  text: string;
  open: boolean;
}) {
  return (
    <Link
      href={href as Route} // ✅ string’i Route tipine dönüştürdük
      className="hover:bg-gray-700 p-2 rounded text-black flex items-center gap-2"
    >
      <span>{icon}</span>
      {open && <span>{text}</span>}
    </Link>
  );
}
