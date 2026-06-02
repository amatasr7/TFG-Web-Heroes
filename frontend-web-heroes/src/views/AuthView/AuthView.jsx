import { useState } from "react";
import "./AuthView.css";
import logoImg from "./components/logo-web-heroes2.png"; 

const API_URL = "http://localhost:8000/api";

export default function AuthView({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const clearForm = () => {
    setName("");
    setEmail("");
    setPassword("");
    setError("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setError("");

    const endpoint = isRegister ? "/auth/register" : "/auth/login";
    const payload = isRegister
      ? { name, email, password }
      : { email, password };

    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorBody = await response.json();
        throw new Error(errorBody.detail || "Ocurrió un error en la autenticación.");
      }

      const user = await response.json();
      onLogin(user);
      clearForm();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-view">
      <img src={logoImg} alt="Web Heroes Logo" className="auth-logo" />

      <div className="auth-card">
        <h1>{isRegister ? "Regístrate" : "Inicia sesión"}</h1>
        <p>
          {isRegister
            ? "¡Crea tu cuenta y empieza a jugar a Web Heroes!"
            : "Accede con tu cuenta de Web Heroes"}
        </p>

        <form onSubmit={handleSubmit} className="auth-form">
          {isRegister && (
            <label>
              Nombre de usuario
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </label>
          )}

          <label>
            Correo electrónico
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>

          <label>
            Contraseña
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>

          {error && <div className="auth-error">{error}</div>}

          <button type="submit" className="auth-submit" disabled={isLoading}>
            {isLoading
              ? isRegister
                ? "Registrando..."
                : "Entrando..."
              : isRegister
              ? "Registrarme"
              : "Iniciar sesión"}
          </button>
        </form>

        <button
          type="button"
          className="auth-toggle"
          onClick={() => {
            setIsRegister(!isRegister);
            setError("");
          }}
        >
          {isRegister
            ? "¿Ya tienes cuenta? Inicia sesión"
            : "¿No tienes cuenta? Regístrate"}
        </button>
      </div>
    </div>
  );
}