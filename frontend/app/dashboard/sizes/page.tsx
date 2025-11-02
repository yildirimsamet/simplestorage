'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { showAlert } from '@/lib/alert';
import type { Size } from '@/lib/types';

export default function SizesPage() {
  const [sizes, setSizes] = useState<Size[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingSize, setEditingSize] = useState<Size | null>(null);
  const [formData, setFormData] = useState({ name: '' });
  const [editFormData, setEditFormData] = useState({
    name: '',
    display_order: 0,
  });

  useEffect(() => {
    loadSizes();
  }, []);

  const loadSizes = async () => {
    try {
      const response = await api.sizes.getAll();
      if (response.success && response.data) {
        const sizesData = Array.isArray(response.data) ? response.data : [response.data];
        const sortedSizes = sizesData.sort((a: Size, b: Size) => (a.display_order || 0) - (b.display_order || 0));
      
        setSizes(sortedSizes);
      }
    } catch (err) {
      console.error('Failed to load sizes', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      const response = await api.sizes.create(formData);

      if (response.success) {
        showAlert.success('Size created successfully');
        setShowModal(false);
        setFormData({ name: '' });
        loadSizes();
      } else {
        showAlert.error(response.message || 'Could not create size');
      }
    } catch (err) {
      console.error('Failed to create size', err);
      showAlert.error('Could not create size');
    }
  };

  const openCreateModal = () => {
    setFormData({ name: '' });
    setShowModal(true);
  };

  const openEditModal = (size: Size) => {
    setEditingSize(size);
    setEditFormData({
      name: size.name,
      display_order: size.display_order || 0,
    });
    setShowEditModal(true);
  };

  const handleEditSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!editingSize) return;

    try {
      const response = await api.sizes.update(editingSize.id, editFormData);

      if (response.success) {
        showAlert.success('Size updated successfully');
        setShowEditModal(false);
        setEditingSize(null);
        loadSizes();
      } else {
        showAlert.error(response.message || 'Could not update size');
      }
    } catch (err) {
      showAlert.error('Could not update size');
    }
  };

  const getSizeByDisplayOrder = (displayOrder: number) => {
    return sizes.find(size => size.display_order === displayOrder);
  };

  const handleDelete = async (size: Size) => {
    const confirmed = await showAlert.confirm(
      `Delete "${size.name}"?`
    );

    if (!confirmed) return;

    try {
      const response = await api.sizes.delete(size.id);
      console.log('res', response);

      if (response.success) {
        showAlert.success('Size deleted successfully');
        loadSizes();
      } else {
        showAlert.error(response.message || 'Could not delete size');
      }
    } catch (err) {
      showAlert.error('Could not delete size');
    }
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
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Display Order</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Name</th>
              <th className="px-6 py-3 text-right text-sm font-semibold text-gray-700">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {sizes.map((size) => (
              <tr key={size.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-sm text-gray-600">{size.display_order}</td>
                <td className="px-6 py-4 text-sm text-gray-900">{size.name}</td>
                <td className="px-6 py-4 text-sm text-right">
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={() => openEditModal(size)}
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
                      onClick={() => handleDelete(size)}
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

      {showEditModal && editingSize && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Edit Size</h2>

            <form onSubmit={handleEditSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Size Name
                </label>
                <input
                  type="text"
                  value={editFormData.name}
                  onChange={(e) => setEditFormData({ ...editFormData, name: e.target.value })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., Small, Medium, Large"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Display Order
                </label>
                <input
                  type="number"
                  min="1"
                  value={editFormData.display_order}
                  onChange={(e) => setEditFormData({ ...editFormData, display_order: Number(e.target.value) })}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter display order"
                />
                {editFormData.display_order !== editingSize.display_order &&
                 getSizeByDisplayOrder(editFormData.display_order) && (
                  <p className="mt-2 text-sm text-amber-600">
                    Will swap with "{getSizeByDisplayOrder(editFormData.display_order)?.name}"
                  </p>
                )}
              </div>

              <div className="flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={() => {
                    setShowEditModal(false);
                    setEditingSize(null);
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
