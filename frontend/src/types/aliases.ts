import type { components } from "./openapi";

export type Product = components["schemas"]["ProductPublic"];
export type Products = components["schemas"]["ProductsPublic"];
export type User = components["schemas"]["UserPublic"];
export type Review = components["schemas"]["ReviewPublic"];
export type LoginRequest =
  components["schemas"]["Body_login-login_access_token"];
export type RegisterRequest = components["schemas"]["UserRegister"];
export type APIError = components["schemas"]["HTTPValidationError"];
export type ValidationError = components["schemas"]["ValidationError"];
