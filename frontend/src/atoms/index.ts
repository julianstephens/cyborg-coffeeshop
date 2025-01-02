import type { User } from "@/types";
import { atomWithStorage } from "jotai/utils";

export * from "./products";

export const darkModeAtom = atomWithStorage("darkMode", false);

export const currentUserAtom = atomWithStorage<User | null>(
  "currentUser",
  null
);
