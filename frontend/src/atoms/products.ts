import { client } from "@/client";
import { atomWithQuery } from "jotai-tanstack-query";

export const productsAtom = atomWithQuery(() => ({
  queryKey: ["products"],
  queryFn: async () => {
    const res = await client.GET("/api/v1/products/");
    return res.data;
  },
}));
