"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch("https://searchprojectdemo.com/api/accounts/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (res.ok) {
        const data = await res.json();

        // ✅ Token'ları kaydet
        localStorage.setItem("accessToken", data.access);
        localStorage.setItem("refreshToken", data.refresh);

        // ✅ Kullanıcı adını kaydet
        localStorage.setItem("username", username);

        // ✅ Cookie (middleware için)
        document.cookie = `accessToken=${data.access}; path=/; SameSite=Lax`;
        document.cookie = `refreshToken=${data.refresh}; path=/; SameSite=Lax`;

        router.push("/dashboard");
      } else {
        const errorData = await res.json();
        alert(errorData.detail || "❌ Kullanıcı adı veya şifre hatalı!");
      }
    } catch (err) {
      console.error("Login hatası:", err);
      alert("Bir hata oluştu.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      className="flex justify-center items-center min-h-screen"
      style={{ backgroundColor: "#ebbecb" }}
    >
      <form
        onSubmit={handleLogin}
        className="bg-white/30 backdrop-blur-lg p-8 rounded-2xl shadow-xl w-full max-w-sm border border-white/40"
      >
        <h1 className="text-2xl font-bold mb-6 text-center text-gray-900 drop-shadow">
          Sina Pırlanta CXP Giriş
        </h1>

        <input
          type="text"
          placeholder="Kullanıcı Adı"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="border border-white/40 bg-white/20 p-3 mb-4 w-full rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400 text-gray-900 placeholder-gray-700"
          required
        />

        <input
          type="password"
          placeholder="Şifre"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border border-white/40 bg-white/20 p-3 mb-6 w-full rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400 text-gray-900 placeholder-gray-700"
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="bg-pink-600 text-white py-2 px-4 w-full rounded-lg hover:bg-pink-700 transition font-semibold shadow-lg"
        >
          {loading ? "Giriş yapılıyor..." : "Giriş Yap"}
        </button>
      </form>
    </div>
  );
}
