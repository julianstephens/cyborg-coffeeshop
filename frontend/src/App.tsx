import "./App.css";
import reactLogo from "./assets/react.svg";
import { $api } from "./client";
import viteLogo from "/vite.svg";

function App() {
  const { data, error } = $api.useQuery("get", "/api/v1/utils/health-check/");

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <h3>API HEALTHY: {!error ? JSON.stringify(data) : <></>}</h3>
    </>
  );
}

export default App;
