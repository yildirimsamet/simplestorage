'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { showAlert } from '@/lib/alert';
import type { Size } from '@/lib/types';

export default function SizesPage() {
  const [sizes, setSizes] = useState<Size[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({ name: '' });

  useEffect(() => {
    loadSizes();
  }, []);

  const loadSizes = async () => {
    try {
      const response = await api.sizes.getAll();
      if (response.success && response.data) {
        setSizes(Array.isArray(response.data) ? response.data : [response.data]);
      }
    } catch (err) {
      console.error('Failed to load sizes', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await api.sizes.create(formData);

      if (response.success) {
        showAlert.success('Size created successfully');
        setShowModal(false);
        setFormData({ name: '' });
        loadSizes();
      } else {
        showAlert.error(response.message || 'Failed to create size');
      }
    } catch (err) {
      showAlert.error('Failed to create size');
    }
  };

  const openCreateModal = () => {
    setFormData({ name: '' });
    setShowModal(true);
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Sizes</h1>
        <button
          onClick={openCreateModal}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Add Size
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">ID</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Name</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Display Order</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {sizes.map((size) => (
              <tr key={size.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-sm text-gray-900">{size.id}</td>
                <td className="px-6 py-4 text-sm text-gray-900">{size.name}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{size.display_order}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {sizes.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No sizes found. Create your first size!
          </div>
        )}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Add Size</h2>

            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Size Name
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ name: e.target.value })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., Small, Medium, Large"
                />
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
