'use client';

import { useState, useEffect } from 'react';
import React from 'react';
import { api } from '@/lib/api';
import { showAlert } from '@/lib/alert';
import type { Product, Category, Size } from '@/lib/types';

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [sizes, setSizes] = useState<Size[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [modal, setModal] = useState<'create' | 'addSize' | 'editSize' | null>(null);
  const [selectedProductId, setSelectedProductId] = useState<number | null>(null);
  const [expandedProductId, setExpandedProductId] = useState<number | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [editingSizeData, setEditingSizeData] = useState<{
    productId: number;
    sizeId: number;
    sizeName: string;
    price: number;
    stock: number;
  } | null>(null);
  const [formData, setFormData] = useState<Omit<Product, 'id' | 'created_at' | 'updated_at'>>({
    name: '',
    description: '',
    category_id: 0,
  });
  const [sizeFormData, setSizeFormData] = useState({
    size_id: 0,
    price: 0,
    stock: 0,
  });
  const [editSizeFormData, setEditSizeFormData] = useState({
    price: 0,
    stock: 0,
  });
  const [imageFile, setImageFile] = useState<File | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    if (searchQuery.trim() === '') {
      loadData();
      return;
    }

    const timeout = setTimeout(async () => {
      try {
        const response = await api.products.search(searchQuery);
        if (response.success && response.data) {
          setProducts(Array.isArray(response.data) ? response.data : [response.data]);
        }
      } catch (err) {
        console.error('Search failed', err);
      }
    }, 300);

    return () => {
      console.log('Clearing timeout');
      clearTimeout(timeout);
    }
  }, [searchQuery]);

  const loadData = async () => {
    try {
      const [productsRes, categoriesRes, sizesRes] = await Promise.all([
        api.products.getAll(),
        api.categories.getAll(),
        api.sizes.getAll(),
      ]);

      if (productsRes.success && productsRes.data) {
        setProducts(Array.isArray(productsRes.data) ? productsRes.data : [productsRes.data]);
      }

      if (categoriesRes.success && categoriesRes.data) {
        setCategories(Array.isArray(categoriesRes.data) ? categoriesRes.data : [categoriesRes.data]);
      }

      if (sizesRes.success && sizesRes.data) {
        setSizes(Array.isArray(sizesRes.data) ? sizesRes.data : [sizesRes.data]);
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
        setModal(null);
        setFormData({ name: '', description: '', category_id: 0 });
        setImageFile(null);
        loadData();
      } else {
        showAlert.error(response.message || 'Product creation failed');
      }
    } catch (err) {
      showAlert.error('Product creation failed');
    }
  };

  const openCreateModal = () => {
    setFormData({ name: '', description: '', category_id: categories[0]?.id || 0 });
    setImageFile(null);
    setModal('create');
  };

  const getCategoryName = (categoryId: number) => {
    return categories.find(c => c.id === categoryId)?.name || 'Unknown';
  };

  const toggleAccordion = (productId: number) => {
    setExpandedProductId(expandedProductId === productId ? null : productId);
  };

  const openAddSizeModal = (productId: number) => {
    setSelectedProductId(productId);
    setSizeFormData({
      size_id: sizes[0]?.id || 0,
      price: 0,
      stock: 0,
    });
    setModal('addSize');
  };

  const handleSizeSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!selectedProductId) return;

    try {
      const response = await api.products.addSize(selectedProductId, sizeFormData);

      if (response.success) {
        showAlert.success('Size added successfully');
        setModal(null);
        setSizeFormData({ size_id: 0, price: 0, stock: 0 });
        setSelectedProductId(null);
        loadData();
      } else {
        showAlert.error(response.message || 'Could not add size');
      }
    } catch (err) {
      showAlert.error('Could not add size');
    }
  };

  const getAvailableSizes = (productId: number) => {
    const product = products.find(product => product.id === productId);
    if (!product) return sizes;

    const usedSizeIds = product.sizes?.map(size => size.size_id) || [];
    return sizes.filter(size => !usedSizeIds.includes(size.id));
  };

  const handleDeleteSize = async (productId: number, sizeId: number) => {
    const result = await showAlert.confirm('Are you sure you want to remove this size?');

    if (!result.isConfirmed) return;

    try {
      const response = await api.products.deleteSize(productId, sizeId);

      if (response.success) {
        showAlert.success('Size removed successfully');
        loadData();
      } else {
        showAlert.error(response.message || 'Could not remove size');
      }
    } catch (err) {
      showAlert.error('Could not remove size');
    }
  };

  const openEditSizeModal = (productId: number, sizeId: number, sizeName: string, price: number, stock: number) => {
    setEditingSizeData({ productId, sizeId, sizeName, price, stock });
    setEditSizeFormData({ price, stock });
    setModal('editSize');
  };

  const handleEditSizeSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!editingSizeData) return;

    try {
      const response = await api.products.updateSize(
        editingSizeData.productId,
        editingSizeData.sizeId,
        editSizeFormData
      );

      if (response.success) {
        showAlert.success('Size updated successfully');
        setModal(null);
        setEditingSizeData(null);
        loadData();
      } else {
        showAlert.error(response.message || 'Could not update size');
      }
    } catch (err) {
      showAlert.error('Could not update size');
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Products</h1>
        <div className="flex gap-3 items-center">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search products..."
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent w-64"
          />
          <button
            onClick={openCreateModal}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Add Product
          </button>
        </div>
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
                        <div className="flex justify-between items-center mb-3">
                          <h3 className="text-sm font-semibold text-gray-700">Size Information</h3>
                          {getAvailableSizes(product.id).length > 0 && (
                            <button
                              onClick={(event) => {
                                event.stopPropagation();
                                openAddSizeModal(product.id);
                              }}
                              className="px-3 py-1 bg-green-600 text-white text-xs rounded hover:bg-green-700 transition-colors"
                            >
                              Add Size
                            </button>
                          )}
                        </div>

                        {product.sizes && product.sizes.length > 0 ? (
                          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
                            <table className="w-full">
                              <thead className="bg-gray-100 border-b border-gray-200">
                                <tr>
                                  <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Size</th>
                                  <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Price</th>
                                  <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Stock</th>
                                  <th className="px-4 py-2 text-right text-xs font-semibold text-gray-600">Action</th>
                                </tr>
                              </thead>
                              <tbody className="divide-y divide-gray-200">
                                {[...product.sizes].sort((a, b) => {
                                  const sizeA = sizes.find(s => s.id === a.size_id);
                                  const sizeB = sizes.find(s => s.id === b.size_id);

                                  return (sizeA?.display_order || 0) - (sizeB?.display_order || 0);
                                }).map((size, index) => (
                                  <tr key={index} className="hover:bg-gray-50">
                                    <td className="px-4 py-2 text-sm text-gray-900">{size.size_name}</td>
                                    <td className="px-4 py-2 text-sm text-gray-900">${size.price.toFixed(2)}</td>
                                    <td className="px-4 py-2 text-sm text-gray-900">{size.stock}</td>
                                    <td className="px-4 py-2 text-sm text-right">
                                      <div className="flex gap-2 justify-end">
                                        <button
                                          onClick={(e) => {
                                            e.stopPropagation();
                                            openEditSizeModal(product.id, size.size_id, size.size_name, size.price, size.stock);
                                          }}
                                          className="text-blue-600 hover:text-blue-800 transition-colors"
                                        >
                                          <svg
                                            className="w-4 h-4"
                                            fill="none"
                                            stroke="currentColor"
                                            viewBox="0 0 24 24"
                                          >
                                            <path
                                              strokeLinecap="round"
                                              strokeLinejoin="round"
                                              strokeWidth={2}
                                              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                                            />
                                          </svg>
                                        </button>
                                        <button
                                          onClick={(e) => {
                                            e.stopPropagation();
                                            handleDeleteSize(product.id, size.size_id);
                                          }}
                                          className="text-red-600 hover:text-red-800 transition-colors"
                                        >
                                          <svg
                                            className="w-4 h-4"
                                            fill="none"
                                            stroke="currentColor"
                                            viewBox="0 0 24 24"
                                          >
                                            <path
                                              strokeLinecap="round"
                                              strokeLinejoin="round"
                                              strokeWidth={2}
                                              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                                            />
                                          </svg>
                                        </button>
                                      </div>
                                    </td>
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

      {modal === 'create' && (
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
                  onClick={() => setModal(null)}
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

      {modal === 'addSize' && selectedProductId && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Add Size to Product</h2>

            <form onSubmit={handleSizeSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Size
                </label>
                <select
                  value={sizeFormData.size_id}
                  onChange={(e) => setSizeFormData({ ...sizeFormData, size_id: Number(e.target.value) })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                >
                  <option value={0}>Select a size</option>
                  {getAvailableSizes(selectedProductId).map((size) => (
                    <option key={size.id} value={size.id}>
                      {size.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Price
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={sizeFormData.price}
                  onChange={(e) => setSizeFormData({ ...sizeFormData, price: Number(e.target.value) })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="Enter price"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Stock
                </label>
                <input
                  type="number"
                  min="0"
                  value={sizeFormData.stock}
                  onChange={(e) => setSizeFormData({ ...sizeFormData, stock: Number(e.target.value) })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="Enter stock quantity"
                />
              </div>

              <div className="flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={() => {
                    setModal(null);
                    setSelectedProductId(null);
                  }}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  Add Size
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {modal === 'editSize' && editingSizeData && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              Edit Size: {editingSizeData.sizeName}
            </h2>

            <form onSubmit={handleEditSizeSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Price
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={editSizeFormData.price}
                  onChange={(e) => setEditSizeFormData({ ...editSizeFormData, price: Number(e.target.value) })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter price"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Stock
                </label>
                <input
                  type="number"
                  min="0"
                  value={editSizeFormData.stock}
                  onChange={(e) => setEditSizeFormData({ ...editSizeFormData, stock: Number(e.target.value) })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter stock quantity"
                />
              </div>

              <div className="flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={() => {
                    setModal(null);
                    setEditingSizeData(null);
                  }}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Update
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
