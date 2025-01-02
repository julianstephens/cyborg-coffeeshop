import { Provider } from "@/components/ui/provider";
import "@/index.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";
import AppRoutes from "./routes";

const client = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <QueryClientProvider client={client}>
        <Provider>
          <AppRoutes />
        </Provider>
      </QueryClientProvider>
    </BrowserRouter>
  </StrictMode>
);
