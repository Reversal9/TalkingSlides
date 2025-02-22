import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import HomePage from "./pages/HomePage";
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  const [firstPageVisited, setFirstPageVisited] = useState(
    localStorage.getItem("firstPageVisited") === "true"
  );

  // Ensure that firstPageVisited is stored correctly
  useEffect(() => {
    const visited = localStorage.getItem("firstPageVisited");
    if (visited === "true") {
      setFirstPageVisited(true);
    }
  }, []);

  return (
    <Router>
      <Routes>
        {/* First page - Accessible by everyone */}
        <Route
          path="/"
          element={<HomePage setFirstPageVisited={setFirstPageVisited} />}
        />

        {/* Protected routes - Only accessible after visiting the first page */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute isAllowed={firstPageVisited}>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        {/* Redirect any unknown routes to home */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
