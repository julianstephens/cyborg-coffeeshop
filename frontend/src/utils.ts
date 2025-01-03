import type { APIError } from "@/types";

export const isAPIError = (err: unknown): err is APIError => {
  return err != null && typeof err == "object" && "detail" in err;
};
