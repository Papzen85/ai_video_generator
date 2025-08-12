// frontend/src/App.jsx
import React, { useState, useEffect, createContext, useContext } from "react";
import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import VideoGenerator from "./pages/VideoGenerator";
import VideoEditor from "./pages/VideoEditor";
import ImageGenerator from "./pages/ImageGenerator";
import AuthPage from "./pages/AuthPage";
import Profile from "./pages/Profile";
import "./styles.css";

/* ----------------------
   Simple Auth Context (dev)
   Stores JWT token in localStorage
   ---------------------- */
const AuthContext = createContext(null);
export function useAuth() { return useContext(AuthContext); }

function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("vidcraft_token"));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      localStorage.setItem("vidcraft_token", token);
      (async () => {
        try {
          const r = await fetch("/api/auth/me", { headers: { Authorization: `Bearer ${token}` } });
          if (r.ok) setUser(await r.json());
          else setUser(null);
        } catch { setUser(null); }
      })();
    } else {
      localStorage.removeItem("vidcraft_token");
      setUser(null);
    }
  }, [token]);

  const login = (newToken) => setToken(newToken);
  const logout = () => setToken(null);

  return <AuthContext.Provider value={{ token, user, login, logout }}>{children}</AuthContext.Provider>;
}

/* ----------------------
   Layout and Nav
   ---------------------- */
function Layout({ children }) {
  const { user, logout } = useAuth();
  const [dark, setDark] = useState(localStorage.getItem("vidcraft_theme") === "dark");

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
    localStorage.setItem("vidcraft_theme", dark ? "dark" : "light");
  }, [dark]);

  return (
    <div className="app">
      <nav className="nav">
        <div className="nav-left">
          <Link to="/">VidCraft</Link>
        </div>
        <div className="nav-right">
          <Link to="/generate">Generate</Link>
          <Link to="/editor">Editor</Link>
          <Link to="/image">Image</Link>
          {user ? <Link to="/profile">{user.username || "Profile"}</Link> : <Link to="/auth">Login</Link>}
          {user && <button className="btn-link" onClick={logout}>Logout</button>}
          <button className="btn-toggle" onClick={() => setDark(d => !d)}>{dark ? "Light" : "Dark"}</button>
        </div>
      </nav>
      <main className="container">{children}</main>
    </div>
  );
}

/* ----------------------
   Protected route helper
   ---------------------- */
function ProtectedRoute({ children }) {
  const { token } = useAuth();
  if (!token) return <Navigate to="/auth" replace />;
  return children;
}

/* ----------------------
   App Router
   ---------------------- */
export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/generate" element={<VideoGenerator />} />
            <Route path="/editor" element={<VideoEditor />} />
            <Route path="/image" element={<ImageGenerator />} />
            <Route path="/auth" element={<AuthPage />} />
            <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </AuthProvider>
  );
}

function Home() {
  return (
    <div>
      <h1>Welcome to VidCraft</h1>
      <p>Create AI-generated realistic videos, edit them, and produce thumbnails — all in one place.</p>
    </div>
  );
}
