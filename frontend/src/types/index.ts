import { Review } from "./aliases";

export * from "./aliases";
export * from "./openapi";
export * from "./props";

export interface ProductReviews {
  [product: string]: Review[];
}
