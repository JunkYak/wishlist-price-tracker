// API stub for future backend integration
export interface Product {
  id: string;
  name: string;
  url: string;
  currentPrice: number;
  targetPrice?: number;
  status: 'target-hit' | 'price-drop' | 'no-change';
  lastChecked: Date;
}

export interface User {
  id: string;
  email: string;
}

// Mock authentication
export const login = async (email: string, password: string): Promise<User> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  if (email && password) {
    return { id: '1', email };
  }
  throw new Error('Invalid credentials');
};

export const register = async (email: string, password: string, confirmPassword: string): Promise<User> => {
  await new Promise(resolve => setTimeout(resolve, 500));
  
  if (password !== confirmPassword) {
    throw new Error('Passwords do not match');
  }
  
  if (email && password) {
    return { id: '1', email };
  }
  throw new Error('Registration failed');
};

// Mock products data
export const getProducts = async (): Promise<Product[]> => {
  await new Promise(resolve => setTimeout(resolve, 300));
  
  return [
    {
      id: '1',
      name: 'Sony WH-1000XM5 Headphones',
      url: 'https://example.com/product1',
      currentPrice: 349.99,
      targetPrice: 299.99,
      status: 'no-change',
      lastChecked: new Date(),
    },
    {
      id: '2',
      name: 'MacBook Pro 14" M3',
      url: 'https://example.com/product2',
      currentPrice: 1599.99,
      targetPrice: 1699.99,
      status: 'target-hit',
      lastChecked: new Date(),
    },
    {
      id: '3',
      name: 'iPhone 15 Pro Max',
      url: 'https://example.com/product3',
      currentPrice: 1099.99,
      targetPrice: 1199.99,
      status: 'price-drop',
      lastChecked: new Date(),
    },
  ];
};

export const getProduct = async (id: string): Promise<Product | null> => {
  await new Promise(resolve => setTimeout(resolve, 300));
  
  const products = await getProducts();
  return products.find(p => p.id === id) || null;
};

export const addProduct = async (url: string, name?: string, targetPrice?: number): Promise<Product> => {
  await new Promise(resolve => setTimeout(resolve, 500));
  
  return {
    id: Date.now().toString(),
    name: name || 'New Product',
    url,
    currentPrice: 0,
    targetPrice,
    status: 'no-change',
    lastChecked: new Date(),
  };
};
