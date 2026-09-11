"use client";

import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

export default function Home() {
  const [isOn, setIsOn] = useState(false);
  const [loading, setLoading] = useState(false);
  const [backendConnected, setBackendConnected] = useState(false);

  useEffect(() => {
    checkBackend();
  }, []);

  async function checkBackend() {
    try {
      const response = await fetch(`${API_URL}/health`);

      if (response.ok) {
        const data = await response.json();
        setBackendConnected(data.fastapi === "running");
      }
    } catch {
      setBackendConnected(false);
    }
  }

  async function toggleLight() {
    const newState = !isOn;

    setLoading(true);

    try {
      const endpoint = newState ? "/light/on" : "/light/off";

      const response = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("API request failed");
      }

      const data = await response.json();

      if (data.success) {
        setIsOn(newState);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Unable to connect to FastAPI");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      {" "}
      <div className="card">
        <h1>Nexora</h1>

        <p className="subtitle">
          <div className="status-api">
            <span className={backendConnected ? "dot connected" : "dot disconnected"} />
            Backend:
            {backendConnected ? " Connected" : " Disconnected"}
          </div>
        </p>

        <div className="power-container">
          <input
            id="checkbox"
            type="checkbox"
            checked={isOn}
            onChange={toggleLight}
            disabled={loading}
          />
          <label className="switch" htmlFor="checkbox">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 512 512"
              className="slider"
            >
              <path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V256c0 17.7 14.3 32 32 32s32-14.3 32-32V32zM143.5 120.6c13.6-11.3 15.4-31.5 4.1-45.1s-31.5-15.4-45.1-4.1C49.7 115.4 16 181.8 16 256c0 132.5 107.5 240 240 240s240-107.5 240-240c0-74.2-33.8-140.6-86.6-184.6c-13.6-11.3-33.8-9.4-45.1 4.1s-9.4 33.8 4.1 45.1c38.9 32.3 63.5 81 63.5 135.4c0 97.2-78.8 176-176 176s-176-78.8-176-176c0-54.4 24.7-103.1 63.5-135.4z"></path>
            </svg>
          </label>
        </div>

        <div className="backend publisher">
          <span>Developed By Kamal</span>
        </div>
        <div className="publisher"></div>
      </div>
    </main>
  );
}
