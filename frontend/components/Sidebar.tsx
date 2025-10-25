'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BiPackage } from 'react-icons/bi';
import { FaChartBar, FaFolder, FaRuler } from 'react-icons/fa';

const navItems = [
  { label: 'Dashboard', href: '/dashboard', icon: <FaChartBar /> },
  { label: 'Categories', href: '/dashboard/categories', icon: <FaFolder /> },
  { label: 'Products', href: '/dashboard/products', icon: <BiPackage /> },
  { label: 'Sizes', href: '/dashboard/sizes', icon: <FaRuler /> },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold">SimpleStorage</h1>
        <p className="text-sm text-gray-400">Admin Panel</p>
      </div>

      <nav className="space-y-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
