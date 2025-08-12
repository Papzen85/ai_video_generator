// frontend/src/pages/Profile.jsx
import React, { useEffect, useState } from "react";

export default function Profile() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    (async () => {
      const token = localStorage.getItem("vidcraft_token");
      if (!token) return;
      const r = await fetch("/api/auth/me", { headers: { Authorization: `Bearer ${token}` } });
      if (r.ok) setUser(await r.json());
      else setUser(null);
    })();
  }, []);

  const logout = () => {
    localStorage.removeItem("vidcraft_token");
    window.location.href = "/";
  };

  return (
    <div>
      <h2>Profile</h2>
      {user ? (
        <div>
          <pre>{JSON.stringify(user, null, 2)}</pre>
          <button onClick={logout}>Logout</button>
        </div>
      ) : (
        <p>Please login.</p>
      )}
    </div>
  );
}
