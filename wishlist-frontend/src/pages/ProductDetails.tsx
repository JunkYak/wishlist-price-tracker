import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, ExternalLink, TrendingDown, Target, Minus } from 'lucide-react';
import { getProduct, Product } from '@/api/api';

const ProductDetails = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [product, setProduct] = useState<Product | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadProduct = async () => {
      if (!id) return;
      
      setIsLoading(true);
      try {
        const data = await getProduct(id);
        setProduct(data);
      } catch (error) {
        console.error('Failed to load product:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadProduct();
  }, [id]);

  const getStatusConfig = () => {
    if (!product) return null;
    
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

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="glass-card p-8">
          <p className="text-muted-foreground">Loading product...</p>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <p className="text-foreground text-lg mb-4">Product not found</p>
          <button
            onClick={() => navigate('/')}
            className="px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-all"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const statusConfig = getStatusConfig();

  return (
    <div className="min-h-screen pb-20">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors mb-8"
        >
          <ArrowLeft size={20} />
          Back to Dashboard
        </button>

        <div className="glass-card p-8 mb-6">
          <div className="flex items-start justify-between mb-6">
            <h1 className="text-3xl font-bold text-foreground flex-1">
              {product.name}
            </h1>
            {statusConfig && (
              <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium ${statusConfig.bgColor} ${statusConfig.textColor}`}>
                {statusConfig.icon}
                {statusConfig.text}
              </div>
            )}
          </div>

          <a
            href={product.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-primary hover:text-primary/80 transition-colors mb-8"
          >
            View on store
            <ExternalLink size={16} />
          </a>

          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <div className="glass-card p-6">
              <p className="text-sm text-muted-foreground mb-2">Current Price</p>
              <p className="text-4xl font-bold text-foreground">
                ${product.currentPrice.toFixed(2)}
              </p>
            </div>

            {product.targetPrice && (
              <div className="glass-card p-6">
                <p className="text-sm text-muted-foreground mb-2">Target Price</p>
                <p className="text-4xl font-bold text-accent">
                  ${product.targetPrice.toFixed(2)}
                </p>
              </div>
            )}
          </div>

          <div className="text-sm text-muted-foreground">
            Last checked: {product.lastChecked.toLocaleString()}
          </div>
        </div>

        <div className="glass-card p-8 text-center">
          <div className="inline-block p-4 rounded-full bg-white/40 mb-4">
            <TrendingDown size={32} className="text-muted-foreground" />
          </div>
          <h2 className="text-xl font-semibold text-foreground mb-2">
            Price History Chart
          </h2>
          <p className="text-muted-foreground">
            Price history tracking coming soon
          </p>
        </div>
      </div>
    </div>
  );
};

export default ProductDetails;
