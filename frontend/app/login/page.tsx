"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ShieldAlert, Lock, Mail, ArrowRight } from "lucide-react";
import { api } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("manager@pharmashield.io");
  const [password, setPassword] = useState("Password123!");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch("http://localhost:8000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        throw new Error("Invalid credentials");
      }

      const data = await res.json();
      localStorage.setItem("pharmashield_token", data.access_token);
      localStorage.setItem("pharmashield_role", data.user.role);
      localStorage.setItem("pharmashield_user", JSON.stringify(data.user));

      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-darkBg flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-cardBg border border-cardBorder rounded-2xl p-8 space-y-6 shadow-2xl">
        {/* Brand */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-cyanAccent to-blueAccent flex items-center justify-center mx-auto shadow-lg shadow-cyanAccent/20">
            <ShieldAlert className="w-7 h-7 text-darkBg stroke-[2.5]" />
          </div>
          <h1 className="text-2xl font-bold text-white tracking-wide">
            Pharma<span className="text-cyanAccent">Shield</span>
          </h1>
          <p className="text-xs text-gray-400">Agentic Cold Chain Resilience Platform</p>
        </div>

        {error && (
          <div className="p-3 rounded-lg bg-roseCritical/10 border border-roseCritical/30 text-roseCritical text-xs font-semibold text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs text-gray-300 font-semibold">User Email</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-darkBg border border-cardBorder rounded-lg pl-9 pr-3 py-2 text-xs text-white focus:outline-none focus:border-cyanAccent"
                required
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs text-gray-300 font-semibold">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-darkBg border border-cardBorder rounded-lg pl-9 pr-3 py-2 text-xs text-white focus:outline-none focus:border-cyanAccent"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-lg bg-gradient-to-r from-cyanAccent to-blueAccent text-darkBg font-bold text-xs shadow-lg shadow-cyanAccent/20 hover:opacity-95 transition flex items-center justify-center gap-2"
          >
            {loading ? "Authenticating..." : "Sign In to Control Tower"} <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        <div className="pt-4 border-t border-cardBorder text-center text-xs text-gray-400 space-y-1">
          <p className="font-semibold text-gray-300">Demo Logins:</p>
          <p>Manager: <code className="text-cyanAccent">manager@pharmashield.io</code></p>
          <p>Operator: <code className="text-cyanAccent">operator@pharmashield.io</code></p>
          <p>Password: <code className="text-gray-300">Password123!</code></p>
        </div>
      </div>
    </div>
  );
}
