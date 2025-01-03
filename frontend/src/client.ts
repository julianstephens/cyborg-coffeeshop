import type { paths } from "@/types";
import createFetchClient, { Middleware } from "openapi-fetch";
import createClient from "openapi-react-query";

const authMiddleware: Middleware = {
  onRequest: async ({ request }) => {
    const accessToken = localStorage.getItem("accessToken");
    if (accessToken) {
      request.headers.append(
        "Authorization",
        `Bearer ${accessToken.substring(1, accessToken.length - 1)}`
      );
    }
    return request;
  },
};

export const client = createFetchClient<paths>({
  baseUrl: import.meta.env.VITE_API_URL,
});
client.use(authMiddleware);

export const $api = createClient(client);
