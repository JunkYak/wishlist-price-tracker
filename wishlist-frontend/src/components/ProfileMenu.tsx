import { LogOut, User, Users } from 'lucide-react';

interface ProfileMenuProps {
  onClose: () => void;
  onLogout: () => void;
}

const ProfileMenu = ({ onClose, onLogout }: ProfileMenuProps) => {
  return (
    <div className="absolute right-0 top-12 w-56 glass-card p-2 z-50">
      <button
        className="w-full px-4 py-2.5 text-left text-sm rounded-lg hover:bg-white/15 transition-colors flex items-center gap-3 text-gray-100"
        onClick={onClose}
      >
        <User size={16} />
        View Account
      </button>
      
      <button
        className="w-full px-4 py-2.5 text-left text-sm rounded-lg hover:bg-white/15 transition-colors flex items-center gap-3 text-gray-100"
        onClick={onClose}
      >
        <Users size={16} />
        Switch Account
      </button>
      
      <div className="h-px bg-white/10 my-2" />
      
      <button
        className="w-full px-4 py-2.5 text-left text-sm rounded-lg hover:bg-destructive/20 transition-colors flex items-center gap-3 text-destructive"
        onClick={onLogout}
      >
        <LogOut size={16} />
        Sign Out
      </button>
    </div>
  );
};

export default ProfileMenu;
