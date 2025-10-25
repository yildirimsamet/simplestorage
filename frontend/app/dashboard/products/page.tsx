'use client';

import { useState, useEffect } from 'react';
import React from 'react';
import { api } from '@/lib/api';
import { showAlert } from '@/lib/alert';
import type { Product, Category } from '@/lib/types';

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [expandedProductId, setExpandedProductId] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category_id: 0,
  });
  const [imageFile, setImageFile] = useState<File | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [productsRes, categoriesRes] = await Promise.all([
        api.products.getAll(),
        api.categories.getAll(),
      ]);

      if (productsRes.success && productsRes.data) {
        setProducts(Array.isArray(productsRes.data) ? productsRes.data : [productsRes.data]);
      }

      if (categoriesRes.success && categoriesRes.data) {
        setCategories(Array.isArray(categoriesRes.data) ? categoriesRes.data : [categoriesRes.data]);
      }
    } catch (err) {
      console.error('Failed to load data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('name', formData.name);
      formDataToSend.append('category_id', formData.category_id.toString());

      if (formData.description) {
        formDataToSend.append('description', formData.description);
      }

      if (imageFile) {
        formDataToSend.append('image', imageFile);
      }

      const response = await api.products.create(formDataToSend);

      if (response.success) {
        showAlert.success('Product created successfully');
        setShowModal(false);
        setFormData({ name: '', description: '', category_id: 0 });
        setImageFile(null);
        loadData();
      } else {
        showAlert.error(response.message || 'Failed to create product');
      }
    } catch (err) {
      showAlert.error('Failed to create product');
    }
  };

  const openCreateModal = () => {
    setFormData({ name: '', description: '', category_id: categories[0]?.id || 0 });
    setImageFile(null);
    setShowModal(true);
  };

  const getCategoryName = (categoryId: number) => {
    return categories.find(c => c.id === categoryId)?.name || 'Unknown';
  };

  const toggleAccordion = (productId: number) => {
    setExpandedProductId(expandedProductId === productId ? null : productId);
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Products</h1>
        <button
          onClick={openCreateModal}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Add Product
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700 w-12"></th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Image</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">ID</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Name</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Category</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Description</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {products.map((product) => (
              <React.Fragment key={product.id}>
                <tr
                  onClick={() => toggleAccordion(product.id)}
                  className="hover:bg-gray-50 cursor-pointer transition-colors"
                >
                  <td className="px-6 py-4 text-sm text-gray-900">
                    <svg
                      className={`w-5 h-5 transition-transform ${
                        expandedProductId === product.id ? 'rotate-90' : ''
                      }`}
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {product.image ? (
                      <img
                        src={`http://localhost:8000/uploads/products/${product.image}`}
                        alt={product.name}
                        className="w-16 h-16 object-cover rounded"
                      />
                    ) : (
                      <div className="w-16 h-16 bg-gray-200 rounded flex items-center justify-center">
                        <span className="text-gray-400 text-xs">No image</span>
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">{product.id}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">{product.name}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">{getCategoryName(product.category_id)}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {product.description || '-'}
                  </td>
                </tr>

                {expandedProductId === product.id && (
                  <tr key={`${product.id}-details`}>
                    <td colSpan={6} className="px-6 py-4 bg-gray-50">
                      <div className="ml-8">
                        <h3 className="text-sm font-semibold text-gray-700 mb-3">Size Information</h3>

                        {product.sizes && product.sizes.length > 0 ? (
                          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
                            <table className="w-full">
                              <thead className="bg-gray-100 border-b border-gray-200">
                                <tr>
                                  <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Size</th>
                                  <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Price</th>
                                  <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Stock</th>
                                </tr>
                              </thead>
                              <tbody className="divide-y divide-gray-200">
                                {product.sizes.map((size, index) => (
                                  <tr key={index} className="hover:bg-gray-50">
                                    <td className="px-4 py-2 text-sm text-gray-900">{size.size_name}</td>
                                    <td className="px-4 py-2 text-sm text-gray-900">${size.price.toFixed(2)}</td>
                                    <td className="px-4 py-2 text-sm text-gray-900">{size.stock}</td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        ) : (
                          <p className="text-sm text-gray-500 italic">No size information available</p>
                        )}
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>

        {products.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No products found. Create your first product!
          </div>
        )}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Add Product</h2>

            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Product Name
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter product name"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Category
                </label>
                <select
                  value={formData.category_id}
                  onChange={(e) => setFormData({ ...formData, category_id: Number(e.target.value) })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value={0}>Select a category</option>
                  {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter product description"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Product Image
                </label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setImageFile(e.target.files?.[0] || null)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                {imageFile && (
                  <p className="mt-2 text-sm text-gray-600">Selected: {imageFile.name}</p>
                )}
              </div>

              <div className="flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
