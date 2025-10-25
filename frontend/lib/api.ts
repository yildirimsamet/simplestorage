import { config } from "./config";
import type {
  ApiResponse,
  Category,
  Product,
  Size,
  LoginRequest,
  TokenResponse,
} from "./types";

const getToken = () => {
  if (typeof window !== "undefined") {
    // TODO: change to cookie later
    // TODO: use axios, set cookie from server and use axios with_credentials
    return localStorage.getItem("token");
  }
  return null;
};

const getHeaders = (includeAuth = true) => {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (includeAuth) {
    const token = getToken();

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }

  return headers;
};

export const api = {
  auth: {
    login: async (credentials: LoginRequest): Promise<TokenResponse> => {
      const response = await fetch(`${config.apiUrl}/auth/login`, {
        method: "POST",
        headers: getHeaders(false),
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      return response.json();
    },
  },

  categories: {
    getAll: async (): Promise<ApiResponse<Category[]>> => {
      const response = await fetch(`${config.apiUrl}/categories`, {
        headers: getHeaders(false),
      });

      if (!response.ok) {
        throw new Error("Categories not found");
      }

      return response.json();
    },

    create: async (data: Omit<Category, 'id'>): Promise<ApiResponse<Category>> => {
      const response = await fetch(`${config.apiUrl}/categories`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Category creation failed");
      }

      return response.json();
    },

    update: async (
      id: number,
      data: Omit<Category, 'id'>
    ): Promise<ApiResponse<Category>> => {
      const response = await fetch(`${config.apiUrl}/categories/${id}`, {
        method: "PUT",
        headers: getHeaders(),
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Category update failed");
      }

      return response.json();
    },

    delete: async (id: number): Promise<ApiResponse<Category>> => {
      const response = await fetch(`${config.apiUrl}/categories/${id}`, {
        method: "DELETE",
        headers: getHeaders(),
      });

      if (!response.ok) {
        throw new Error("Category deletion failed");
      }

      return response.json();
    },
  },

  products: {
    getAll: async (): Promise<ApiResponse<Product[]>> => {
      const response = await fetch(`${config.apiUrl}/products`, {
        headers: getHeaders(false),
      });

      if (!response.ok) {
        throw new Error("Products not found");
      }

      return response.json();
    },

    create: async (data: FormData): Promise<ApiResponse<Product>> => {
      const token = getToken();
      const headers: HeadersInit = {};

      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch(`${config.apiUrl}/products`, {
        method: "POST",
        headers,
        body: data,
      });

      return response.json();
    },
  },

  sizes: {
    getAll: async (): Promise<ApiResponse<Size[]>> => {
      const response = await fetch(`${config.apiUrl}/sizes`, {
        headers: getHeaders(false),
      });

      if (!response.ok) {
        throw new Error("Sizes not found");
      }

      return response.json();
    },

    create: async (data: Omit<Size, 'id'>): Promise<ApiResponse<Size>> => {
      const response = await fetch(`${config.apiUrl}/sizes`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Size creation failed");
      }

      return response.json();
    },
  },
};
