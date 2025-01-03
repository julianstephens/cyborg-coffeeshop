import { Layout } from "@/components/layout";
import { Provider } from "@/components/ui/provider";
import { Toaster } from "@/components/ui/toaster";
import AppRoutes from "@/routes";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";

const client = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <QueryClientProvider client={client}>
        <Provider>
          <Toaster />
          <Layout>
            <AppRoutes />
          </Layout>
        </Provider>
      </QueryClientProvider>
    </BrowserRouter>
  </StrictMode>
);
