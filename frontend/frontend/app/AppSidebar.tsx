'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Sidebar() {
  const [openMenus, setOpenMenus] = useState<{ [key: string]: boolean }>({});

  const toggleMenu = (menu: string) => {
    setOpenMenus(prev => ({ ...prev, [menu]: !prev[menu] }));
  };

  return (
    <aside className="w-64 h-screen bg-white shadow-md p-6 flex flex-col">
      {/* Logo */}
      <div className="text-2xl font-bold text-blue-600 mb-8">
  <img src="https://www.sinapirlanta.com/themes/custom/sina/logo.svg" alt="Logo" className="h-8" />
</div>


      {/* Sections */}
      <div className="text-xs text-gray-500 font-semibold uppercase mb-3">Aboneler</div>

      <nav className="space-y-2 text-sm">
        <SidebarItem label="Dashboard" active dropdown onClick={() => toggleMenu('dashboard')} isOpen={openMenus['dashboard']} />
        <SidebarItem label="Add-to-cart Mail İçerik" />
        <SidebarItem label="E mail Önerileri " />
        <SidebarItem label="Hoşgeldiniz Maili" dropdown onClick={() => toggleMenu('task')} isOpen={openMenus['task']} />
        <SidebarItem label="Aboneler" dropdown onClick={() => toggleMenu('forms')} isOpen={openMenus['forms']} />
        
      </nav>

      <div className="text-xs text-gray-500 font-semibold uppercase mt-8 mb-3">Kullanıcı İzleme</div>

      <nav className="space-y-2 text-sm">
        <SidebarItem label="Sepete Eklemeler" />
        <SidebarItem label="Kullanıcı Hareketleri" dropdown onClick={() => toggleMenu('email')} isOpen={openMenus['email']} />
        
      </nav>

     

    
    </aside>
  );
}

type SidebarItemProps = {
  label: string;
  active?: boolean;
  dropdown?: boolean;
  onClick?: () => void;
  isOpen?: boolean;
};

function SidebarItem({ label, active, dropdown, onClick, isOpen }: SidebarItemProps) {
  return (
    <div>
      <div
        className={`flex justify-between items-center cursor-pointer px-3 py-2 rounded-md hover:bg-gray-100 ${
          active ? 'bg-blue-50 text-blue-600 font-medium' : 'text-gray-800'
        }`}
        onClick={onClick}
      >
        <span>{label}</span>
        {dropdown && (
          <span className={`transition-transform ${isOpen ? 'rotate-90' : 'rotate-0'}`}>▶</span>
        )}
      </div>
      {dropdown && isOpen && (
        <div className="ml-4 mt-1 space-y-1 text-gray-600 text-sm">
          <Link href="#" className="block hover:text-black">Alt Menü 1</Link>
          <Link href="#" className="block hover:text-black">Alt Menü 2</Link>
        </div>
      )}
    </div>
  );
}
