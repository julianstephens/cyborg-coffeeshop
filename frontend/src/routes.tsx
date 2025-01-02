import Login from "@/pages/login";
import StoreFront from "@/pages/storefront";
import { Route, Routes } from "react-router";

const AppRoutes = () => (
  <Routes>
    <Route index element={<StoreFront />} />
    <Route path="/login" element={<Login />} />
  </Routes>
);

export default AppRoutes;
