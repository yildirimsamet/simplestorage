import axios from "axios";
import { config } from "./config";
import type {
  ApiResponse,
  Category,
  Product,
  ProductSizeAdd,
  Size,
  LoginRequest,
  TokenResponse,
} from "./types";

const axiosInstance = axios.create({
  baseURL: config.apiUrl,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export const api = {
  auth: {
    login: async (credentials: LoginRequest): Promise<TokenResponse> => {
      const response = await axiosInstance.post("/auth/login", credentials, {
        headers: { "Content-Type": "application/json" },
        transformRequest: [(data) => JSON.stringify(data)],
      });

      console.log('res::', response.data);

      return response.data;
    },

    logout: async (): Promise<{ success: boolean; message: string }> => {
      const response = await axiosInstance.post("/auth/logout");

      console.log('res:', response.data);

      return response.data;
    },
  },

  categories: {
    getAll: async (): Promise<ApiResponse<Category[]>> => {
      const response = await axiosInstance.get("/categories");
      return response.data;
    },

    create: async (data: Omit<Category, "id">): Promise<ApiResponse<Category>> => {
      const response = await axiosInstance.post("/categories", data);
    
      return response.data;
    },

    update: async (
      id: number,
      data: Omit<Category, "id">
    ): Promise<ApiResponse<Category>> => {
      const response = await axiosInstance.put(`/categories/${id}`, data);
  
      return response.data;
    },

    delete: async (id: number): Promise<ApiResponse<Category>> => {
      const response = await axiosInstance.delete(`/categories/${id}`);
      return response.data;
    },
  },

  products: {
    getAll: async (): Promise<ApiResponse<Product[]>> => {
      const response = await axiosInstance.get("/products");
      return response.data;
    },

    search: async (searchQuery: string): Promise<ApiResponse<Product[]>> => {
      const response = await axiosInstance.get("/products/search", {
        params: { search_query: searchQuery },
      });

      console.log('data',response.data);

      return response.data;
    },

    create: async (data: FormData): Promise<ApiResponse<Product>> => {
      const response = await axiosInstance.post("/products", data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      return response.data;
    },

    addSize: async (
      productId: number,
      data: ProductSizeAdd
    ): Promise<ApiResponse<Product>> => {
      const response = await axiosInstance.post(
        `/products/${productId}/sizes`, data );
    
      return response.data;
    },

    deleteSize: async (
      productId: number,
      sizeId: number
    ): Promise<ApiResponse<Product>> => {
      const response = await axiosInstance.delete(
        `/products/${productId}/sizes/${sizeId}`);

    
      return response.data;
    },

    updateSize: async (
      productId: number,
      sizeId: number,
      data: { price?: number; stock?: number }
    ): Promise<ApiResponse<Product>> => {
      const response = await axiosInstance.put(
        `/products/${productId}/sizes/${sizeId}`, data
      );

      return response.data;
    },
  },

  sizes: {
    getAll: async (): Promise<ApiResponse<Size[]>> => {
      const response = await axiosInstance.get("/sizes");
  
      return response.data;
    },

    create: async (data: Omit<Size, "id">): Promise<ApiResponse<Size>> => {
      const response = await axiosInstance.post("/sizes", data);
      return response.data;
    },

    update: async (
      id: number,
      data: Partial<Omit<Size, "id">>
    ): Promise<ApiResponse<Size>> => {
      const response = await axiosInstance.put(`/sizes/${id}`, data);
      return response.data;
    },

    delete: async (id: number): Promise<ApiResponse<Size>> => {
      const response = await axiosInstance.delete(`/sizes/${id}`);
      return response.data;
    },
  },
};
