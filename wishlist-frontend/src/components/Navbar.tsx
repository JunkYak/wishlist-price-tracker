import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ProfileMenu from './ProfileMenu';

interface NavbarProps {
  onLogout: () => void;
}

const Navbar = ({ onLogout }: NavbarProps) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = () => {
    setIsMenuOpen(false);
    onLogout();
    navigate('/auth');
  };

  return (
    <nav className="glass-card sticky top-4 mx-4 z-50 px-6 py-3 shadow-[0_4px_24px_rgba(0,0,0,0.5)]">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <button 
          onClick={() => navigate('/')}
          className="text-2xl font-semibold text-gray-100 hover:text-[#c58cff] transition-colors"
        >
          cOpit
        </button>
        
        <div className="relative" ref={menuRef}>
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="w-9 h-9 rounded-full bg-gradient-to-br from-[#c58cff]/30 to-[#8b5cf6]/30 border border-white/10 hover:shadow-[0_0_18px_3px_rgba(197,140,255,0.35)] transition-all hover:scale-105 flex items-center justify-center text-[#c58cff] font-medium"
          >
            U
          </button>
          
          {isMenuOpen && (
            <ProfileMenu 
              onClose={() => setIsMenuOpen(false)} 
              onLogout={handleLogout}
            />
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
