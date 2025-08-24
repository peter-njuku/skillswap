import { useState } from "react";
import { Menu, X } from "lucide-react";
import logo from '../assets/logo.png';
import { useAuthStore } from '../store/authStore';

export default function NavBar() {
  const [isOpen, setIsOpen] = useState(false);
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  return (
    <nav className="fixed top-0 left-0 w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-md z-50">
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <img src={logo} alt="Logo" className="h-10 w-auto" />
          <h1 className="text-2xl font-bold">SkillSwaps</h1>
        </div>

        {/* Desktop Menu */}
        {user ? (
          <ul className="hidden md:flex space-x-6">
            <li><a href="/dashboard" className="hover:text-purple-300">Dashboard</a></li>
            <li><a href="/skills" className="hover:text-purple-300">Skills</a></li>
            <li><a href="/find" className="hover:text-purple-300">Find People</a></li>
            <li><a href="/messages" className="hover:text-purple-300">Messages</a></li>
            <li><a href="/settings" className="hover:text-purple-300">Settings</a></li>
            <li><button onClick={logout} className="hover:text-red-300">Logout</button></li>
          </ul>
        ) : (
          <ul className="hidden md:flex space-x-6">
            <li><a href="/login" className="hover:text-purple-300">Login</a></li>
            <li><a href="/register" className="hover:text-purple-300">Register</a></li>
          </ul>
        )}

        {/* Mobile Hamburger */}
        <button className="md:hidden" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <X size={28} /> : <Menu size={28} />}
        </button>
      </div>

      {/* Mobile Dropdown */}
      {isOpen && (
        <ul className="flex flex-col mt-4 space-y-4 md:hidden px-4 pb-4">
          {user ? (
            <>
              <li><a href="/dashboard">Dashboard</a></li>
              <li><a href="/skills">Skills</a></li>
              <li><a href="/find">Find People</a></li>
              <li><a href="/messages">Messages</a></li>
              <li><a href="/settings">Settings</a></li>
              <li><button onClick={logout}>Logout</button></li>
            </>
          ) : (
            <>
              <li><a href="/login">Login</a></li>
              <li><a href="/register">Register</a></li>
            </>
          )}
        </ul>
      )}
    </nav>
  );
}
