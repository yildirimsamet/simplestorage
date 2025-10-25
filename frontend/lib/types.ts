export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
}

export interface Category {
  id: number;
  name: string;
}

export interface Size {
  id: number;
  name: string;
  display_order?: number;
}

export interface ProductSize {
  size_id: number;
  size_name: string;
  price: number;
  stock: number;
}

export interface Product {
  id: number;
  name: string;
  image?: string;
  description?: string;
  category_id: number;
  sizes?: ProductSize[];
}

export interface User {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}
