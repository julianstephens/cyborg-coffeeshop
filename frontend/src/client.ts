import type { paths } from "@/types";
import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";

export const client = createFetchClient<paths>({
  baseUrl: import.meta.env.VITE_API_URL,
});

export const $api = createClient(client);
