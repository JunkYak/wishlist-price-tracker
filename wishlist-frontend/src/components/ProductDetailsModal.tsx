import { X, ExternalLink, Target, TrendingDown, Minus } from 'lucide-react';
import { Product } from '@/api/api';

interface ProductDetailsModalProps {
  product: Product;
  onClose: () => void;
}

const ProductDetailsModal = ({ product, onClose }: ProductDetailsModalProps) => {
  const getStatusConfig = () => {
    switch (product.status) {
      case 'target-hit':
        return {
          icon: <Target size={18} />,
          text: 'Target Hit',
          bgColor: 'bg-green-100 dark:bg-green-900/30',
          textColor: 'text-green-700 dark:text-green-300',
        };
      case 'price-drop':
        return {
          icon: <TrendingDown size={18} />,
          text: 'Price Drop',
          bgColor: 'bg-blue-100 dark:bg-blue-900/30',
          textColor: 'text-blue-700 dark:text-blue-300',
        };
      default:
        return {
          icon: <Minus size={18} />,
          text: 'No Change',
          bgColor: 'bg-gray-100 dark:bg-gray-800/30',
          textColor: 'text-gray-600 dark:text-gray-400',
        };
    }
  };

  const statusConfig = getStatusConfig();

  return (
    <div className="glass-overlay p-4" onClick={onClose}>
      <div
        className="backdrop-blur-md bg-[#1a1a22]/80 border border-white/10 rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.6)] p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between mb-6">
          <div className="flex-1 pr-4">
            <h2 className="text-2xl font-semibold text-gray-100 mb-2">
              {product.name}
            </h2>
            <a
              href={product.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-[#c58cff] hover:text-[#c58cff]/80 transition-colors text-sm"
            >
              View on store
              <ExternalLink size={14} />
            </a>
          </div>
          
          <div className="flex items-start gap-3">
            <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium whitespace-nowrap ${statusConfig.bgColor} ${statusConfig.textColor}`}>
              {statusConfig.icon}
              {statusConfig.text}
            </div>
            
            <button
              onClick={onClose}
              className="p-2 hover:bg-white/15 rounded-lg transition-colors flex-shrink-0 text-gray-100"
            >
              <X size={20} />
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4 mb-6">
          <div className="backdrop-blur-md bg-[#1a1a22]/80 border border-white/10 rounded-xl p-4">
            <p className="text-sm text-gray-400 mb-2">Current Price</p>
            <p className="text-3xl font-semibold text-gray-100">
              ${product.currentPrice.toFixed(2)}
            </p>
          </div>

          {product.targetPrice && (
            <div className="backdrop-blur-md bg-[#1a1a22]/80 border border-white/10 rounded-xl p-4">
              <p className="text-sm text-gray-400 mb-2">Target Price</p>
              <p className="text-3xl font-semibold text-[#c58cff]">
                ${product.targetPrice.toFixed(2)}
              </p>
            </div>
          )}
        </div>

        <div className="backdrop-blur-md bg-[#1a1a22]/80 border border-white/10 rounded-xl p-8 text-center">
          <div className="inline-block p-3 rounded-full bg-white/10 mb-3">
            <TrendingDown size={28} className="text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-100">
            Price history chart coming soon
          </h3>
        </div>

        <div className="mt-4 text-xs text-gray-400 text-center">
          Last checked: {product.lastChecked.toLocaleString()}
        </div>
      </div>
    </div>
  );
};

export default ProductDetailsModal;
