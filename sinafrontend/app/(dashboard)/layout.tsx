"use client";

import { ReactNode, useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import type { Route } from "next";
import {
  LayoutDashboard,
  Users,
  Megaphone,
  BarChart3,
  UserCheck,
  ShoppingCart,
  Mail,
  Puzzle,
  Menu,
  X,
} from "lucide-react";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [username, setUsername] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const cookies = document.cookie.split(";").map((c) => c.trim());
    const token = cookies.find((c) => c.startsWith("accessToken="));
    if (!token) router.replace("/login");

    const storedUsername = localStorage.getItem("username");
    if (storedUsername) setUsername(storedUsername);
  }, [router]);

  return (
    <div className="flex h-screen bg-gray-50 p-4 gap-4">
      {/* Sidebar */}
      <div
        className={`bg-white shadow rounded-2xl transition-all duration-300 flex flex-col border border-gray-200 ${
          sidebarOpen ? "w-64" : "w-20"
        }`}
      >
        {/* Logo */}
        <div className="flex justify-center py-6">
          {sidebarOpen ? (
            <img
              src="https://www.sinapirlanta.com/themes/custom/sina/logo.svg"
              alt="Sina Pırlanta"
              className="h-12"
            />
          ) : (
            <img src="/vercel.svg" alt="Mini Logo" className="h-8" />
          )}
        </div>

        {/* Menu Links */}
        {/* Küçükken gap-6: ikonlar arası mesafe büyür */}
        <nav className={`flex flex-col px-3 mt-4 ${sidebarOpen ? "gap-4" : "gap-6"}`}>
          <SidebarLink
            href="/dashboard"
            icon={<LayoutDashboard size={20} />}
            text="Dashboard"
            open={sidebarOpen}
          />
          <SidebarLink
            href="/anlik-kullanici"
            icon={<Users size={20} />}
            text="Anlık Kullanıcılar"
            open={sidebarOpen}
          />
          <SidebarLink
            href="/campaigns"
            icon={<Megaphone size={20} />}
            text="Kampanyalar"
            open={sidebarOpen}
          />
          <SidebarLink
            href="/reklamlar"
            icon={<BarChart3 size={20} />}
            text="Reklamlar"
            open={sidebarOpen}
          />
          <SidebarLink
            href="/aboneler"
            icon={<UserCheck size={20} />}
            text="Aboneler"
            open={sidebarOpen}
          />
          <SidebarLink
            href="/sepete-eklemeler"
            icon={<ShoppingCart size={20} />}
            text="Sepete Eklemeler"
            open={sidebarOpen}
          />
          <SidebarLink
            href="/welcome-template"
            icon={<Mail size={20} />}
            text="Hoşgeldin Maili"
            open={sidebarOpen}
          />
          <SidebarLink
            href="/widgets"
            icon={<Puzzle size={20} />}
            text="Widgets"
            open={sidebarOpen}
          />
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col gap-4">
        {/* Navbar */}
        <div className="flex items-center justify-between bg-white shadow px-6 py-3 rounded-2xl border border-gray-200">
          <button
            className="p-2 rounded-lg hover:bg-gray-100 transition"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Sidebar toggle"
            title={sidebarOpen ? "Menüyü daralt" : "Menüyü genişlet"}
          >
            {sidebarOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
          <h1 className="text-lg font-semibold text-gray-800">
            Sina Pırlanta Customer Experience Platform
          </h1>
          <div className="flex items-center space-x-3">
            <span className="text-gray-700">Hoşgeldin, {username || "Kullanıcı"}</span>
            <img src="https://via.placeholder.com/32" alt="Avatar" className="rounded-full" />
          </div>
        </div>

        {/* Page Content */}
        <main className="p-6 overflow-y-auto flex-1 bg-white shadow rounded-2xl border border-gray-200">
          {children}
        </main>
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
  icon: ReactNode;
  text: string;
  open: boolean;
}) {
  return (
    <Link
      href={href as Route}
      className={`flex items-center rounded-xl transition
        ${
          open
            // Açıkken: daha iri yazı ve iç boşluk
            ? "gap-4 px-4 py-3 text-[15px] font-medium"
            // Kapalıyken: kare buton + sabit yükseklik → ikonlar arası mesafe hissedilir
            : "justify-center h-12 w-full px-0 py-0"
        }
        text-gray-700 hover:bg-pink-100 hover:text-pink-600`}
      title={open ? undefined : text}
      aria-label={text}
    >
      {/* İkonu ortalamak için bir kapsayıcı; kapalıyken kare görünür */}
      <span className={`grid place-items-center ${open ? "" : "h-10 w-10 rounded-xl"}`}>
        {icon}
      </span>
      {open && <span className="leading-[1.15]">{text}</span>}
    </Link>
  );
}
