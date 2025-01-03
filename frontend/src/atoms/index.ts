import { client } from "@/client";
import { atomWithQuery } from "jotai-tanstack-query";
import { atomWithStorage } from "jotai/utils";

export * from "./products";

export const darkModeAtom = atomWithStorage("darkMode", false);

export const currentUserAtom = atomWithQuery(() => ({
  queryKey: ["currentUser"],
  queryFn: async () => {
    const { data } = await client.GET("/api/v1/users/me");
    return data ?? null;
  },
}));

export const accessTokenAtom = atomWithStorage<string | null>(
  "accessToken",
  null
);
