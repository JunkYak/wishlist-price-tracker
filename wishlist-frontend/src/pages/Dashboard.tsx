import { useState, useEffect } from 'react';
import { Plus } from 'lucide-react';
import PriceCard from '@/components/PriceCard';
import AddProductModal from '@/components/AddProductModal';
import ProductDetailsModal from '@/components/ProductDetailsModal';
import { getProducts, Product } from '@/api/api';

const Dashboard = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadProducts = async () => {
    setIsLoading(true);
    try {
      const data = await getProducts();
      setProducts(data);
    } catch (error) {
      console.error('Failed to load products:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const handleProductAdded = () => {
    loadProducts();
  };

  return (
    <div className="min-h-screen pb-20">
      <div className="max-w-7xl mx-auto px-4 py-10">
        <div className="mb-10">
          <h1 className="text-4xl font-semibold text-gray-100 mb-3">
            Price Tracker
          </h1>
          <p className="text-gray-400 text-lg">
            Monitor products and get notified when prices drop ✦
          </p>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3].map((i) => (
              <div key={i} className="glass-card p-6 animate-pulse">
                <div className="h-6 bg-white/10 rounded mb-4" />
                <div className="h-8 bg-white/10 rounded mb-2" />
                <div className="h-6 bg-white/10 rounded" />
              </div>
            ))}
          </div>
        ) : products.length === 0 ? (
          <div className="flex items-center justify-center min-h-[50vh]">
            <div className="glass-card p-10 text-center max-w-md">
              <div className="text-5xl mb-4">✦</div>
              <h3 className="text-xl font-medium text-gray-100 mb-2">
                Nothing tracked yet
              </h3>
              <p className="text-gray-400 mb-6">
                Click the + button to start tracking your first product
              </p>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {products.map((product) => (
              <PriceCard 
                key={product.id} 
                product={product} 
                onClick={setSelectedProduct}
              />
            ))}
          </div>
        )}
      </div>

      <button
        onClick={() => setIsModalOpen(true)}
        className="fixed bottom-8 right-8 w-14 h-14 bg-[#c58cff] hover:bg-[#c58cff]/90 text-[#0e0e11] rounded-full shadow-[0_8px_32px_rgba(197,140,255,0.4)] hover:shadow-[0_8px_40px_rgba(197,140,255,0.6)] transition-all hover:scale-105 flex items-center justify-center z-40 font-semibold"
      >
        <Plus size={24} />
      </button>

      {isModalOpen && (
        <AddProductModal
          onClose={() => setIsModalOpen(false)}
          onProductAdded={handleProductAdded}
        />
      )}

      {selectedProduct && (
        <ProductDetailsModal
          product={selectedProduct}
          onClose={() => setSelectedProduct(null)}
        />
      )}
    </div>
  );
};

export default Dashboard;
