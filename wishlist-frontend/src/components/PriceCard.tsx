import { TrendingDown, Target, Minus } from 'lucide-react';
import { Product } from '@/api/api';

interface PriceCardProps {
  product: Product;
  onClick: (product: Product) => void;
}

const PriceCard = ({ product, onClick }: PriceCardProps) => {

  const getStatusConfig = () => {
    switch (product.status) {
      case 'target-hit':
        return {
          icon: <Target size={16} />,
          text: 'Target Hit',
          bgColor: 'bg-green-100 dark:bg-green-900/30',
          textColor: 'text-green-700 dark:text-green-300',
        };
      case 'price-drop':
        return {
          icon: <TrendingDown size={16} />,
          text: 'Price Drop',
          bgColor: 'bg-blue-100 dark:bg-blue-900/30',
          textColor: 'text-blue-700 dark:text-blue-300',
        };
      default:
        return {
          icon: <Minus size={16} />,
          text: 'No Change',
          bgColor: 'bg-gray-100 dark:bg-gray-800/30',
          textColor: 'text-gray-600 dark:text-gray-400',
        };
    }
  };

  const statusConfig = getStatusConfig();

  return (
    <div
      onClick={() => onClick(product)}
      className="glass-card glass-hover p-6 cursor-pointer group"
    >
      <div className="flex items-start justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-100 line-clamp-2 group-hover:text-[#c58cff] transition-colors">
          {product.name}
        </h3>
        <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium whitespace-nowrap ${statusConfig.bgColor} ${statusConfig.textColor}`}>
          {statusConfig.icon}
          {statusConfig.text}
        </div>
      </div>

      <div className="space-y-3">
        <div>
          <p className="text-xs text-gray-400 mb-1">Current Price</p>
          <p className="text-2xl font-semibold text-gray-100">
            ${product.currentPrice.toFixed(2)}
          </p>
        </div>

        {product.targetPrice && (
          <div>
            <p className="text-xs text-gray-400 mb-1">Target Price</p>
            <p className="text-lg font-medium text-[#c58cff]">
              ${product.targetPrice.toFixed(2)}
            </p>
          </div>
        )}
      </div>

      <div className="mt-4 pt-4 border-t border-white/10">
        <span className="text-xs text-gray-400">
          Last checked: {product.lastChecked.toLocaleString()}
        </span>
      </div>
    </div>
  );
};

export default PriceCard;
