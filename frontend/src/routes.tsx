import { Route, Routes } from "react-router";
import StoreFront from "./pages/storefront";

const AppRoutes = () => (
  <Routes>
    <Route index element={<StoreFront />} />
  </Routes>
);

export default AppRoutes;
