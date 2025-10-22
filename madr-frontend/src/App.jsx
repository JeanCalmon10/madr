import { useState, useEffect } from "react";
import { fecthHealthCheck } from "./services/api";

function App() {
  useEffect(() => {
    fecthHealthCheck();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold text-blue-600">Hello MADR Frontend</h1>
    </div>
  );
}

export default App;
