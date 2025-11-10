import { useState } from 'react';
import { X } from 'lucide-react';
import { addProduct } from '@/api/api';
import { toast } from '@/hooks/use-toast';

interface AddProductModalProps {
  onClose: () => void;
  onProductAdded: () => void;
}

const AddProductModal = ({ onClose, onProductAdded }: AddProductModalProps) => {
  const [url, setUrl] = useState('');
  const [name, setName] = useState('');
  const [targetPrice, setTargetPrice] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!url.trim()) {
      toast({
        title: 'URL Required',
        description: 'Please enter a product URL',
        variant: 'destructive',
      });
      return;
    }

    setIsLoading(true);
    
    try {
      await addProduct(
        url,
        name || undefined,
        targetPrice ? parseFloat(targetPrice) : undefined
      );
      
      toast({
        title: 'Product Added',
        description: 'The product has been added to your tracking list',
      });
      
      onProductAdded();
      onClose();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to add product. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="glass-overlay z-50" onClick={onClose}>
      <div
        className="backdrop-blur-md bg-[#1a1a22]/80 border border-white/10 rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.6)] p-8 w-full max-w-md mx-4"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-semibold text-gray-100">Track New Product</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/15 rounded-lg transition-colors text-gray-100"
          >
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="url" className="block text-sm font-medium text-gray-100 mb-2">
              Product URL *
            </label>
            <input
              id="url"
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://www.amazon.com/product/..."
              className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/10 text-gray-100 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-[#c58cff] transition-all"
              required
            />
          </div>

          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-100 mb-2">
              Product Name (Optional)
            </label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Leave blank to auto-fetch"
              className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/10 text-gray-100 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-[#c58cff] transition-all"
            />
          </div>

          <div>
            <label htmlFor="targetPrice" className="block text-sm font-medium text-gray-100 mb-2">
              Target Price (Optional)
            </label>
            <input
              id="targetPrice"
              type="number"
              step="0.01"
              value={targetPrice}
              onChange={(e) => setTargetPrice(e.target.value)}
              placeholder="e.g., 99.99"
              className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/10 text-gray-100 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-[#c58cff] transition-all"
            />
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-6 py-3 rounded-full bg-white/10 text-gray-100 hover:bg-white/15 transition-all font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 px-6 py-3 rounded-full bg-gradient-to-r from-[#c58cff] to-[#8b5cf6] text-white hover:shadow-[0_0_18px_3px_rgba(197,140,255,0.35)] transition-all disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {isLoading ? 'Adding...' : 'Add Product'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddProductModal;
