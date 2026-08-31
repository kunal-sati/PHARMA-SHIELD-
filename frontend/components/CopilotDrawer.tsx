"use client";

import { useState } from "react";
import { Bot, Send, X, BookOpen, Sparkles, CheckCircle2 } from "lucide-react";

interface CopilotDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  shipmentId?: string;
}

export function CopilotDrawer({ isOpen, onClose, shipmentId = "PS-1026" }: CopilotDrawerProps) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Array<{ sender: string; text: string; citations?: string[] }>>([
    {
      sender: "copilot",
      text: "Hello! I am your PharmaShield Resilience Copilot. Ask me about thermal stability, cold-storage capacity, SOP handling policies, or What-If decision reasoning for shipment PS-1026.",
      citations: ["PharmaShield Enterprise Policy v2.0"]
    }
  ]);

  if (!isOpen) return null;

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    const userText = query;
    setQuery("");
    setMessages((prev) => [...prev, { sender: "user", text: userText }]);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/copilot/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userText, shipment_id: shipmentId }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          sender: "copilot",
          text: data.answer,
          citations: data.source_citations,
        },
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        { sender: "copilot", text: `Error processing query: ${err.message}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-y-0 right-0 w-96 bg-cardBg border-l border-cardBorder shadow-2xl z-50 flex flex-col">
      {/* Drawer Header */}
      <div className="p-4 border-b border-cardBorder flex items-center justify-between bg-darkBg/60">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-cyanAccent/20 text-cyanAccent">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-1.5">
              Resilience Copilot
              <Sparkles className="w-3.5 h-3.5 text-cyanAccent" />
            </h3>
            <p className="text-[10px] text-gray-400">Contextual Supply Chain Assistant</p>
          </div>
        </div>
        <button onClick={onClose} className="p-1 rounded text-gray-400 hover:text-white">
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4 text-xs">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`p-3.5 rounded-xl space-y-2 ${
              m.sender === "user"
                ? "bg-cyanAccent/10 border border-cyanAccent/30 text-white ml-6"
                : "bg-white/5 border border-cardBorder text-gray-200 mr-4"
            }`}
          >
            <p className="leading-relaxed">{m.text}</p>

            {m.citations && m.citations.length > 0 && (
              <div className="pt-2 border-t border-white/10 text-[10px] text-gray-400 space-y-1">
                <p className="font-semibold text-cyanAccent flex items-center gap-1">
                  <BookOpen className="w-3 h-3" /> Sources & SOP References:
                </p>
                <ul className="list-disc list-inside font-mono">
                  {m.citations.map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="p-3 text-xs text-gray-400 animate-pulse flex items-center gap-2">
            <Bot className="w-4 h-4 text-cyanAccent" /> Processing context & RAG sources...
          </div>
        )}
      </div>

      {/* Disclaimer */}
      <div className="px-4 py-2 bg-darkBg/80 border-t border-cardBorder text-[10px] text-gray-400 text-center">
        Provides decision support. High-impact rerouting requires SAP governance & Manager approval.
      </div>

      {/* Input Form */}
      <form onSubmit={handleSend} className="p-3 border-t border-cardBorder bg-cardBg flex items-center gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask why CS-04 was chosen, or what if we wait..."
          className="flex-1 bg-darkBg border border-cardBorder rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyanAccent"
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="p-2 rounded-lg bg-cyanAccent text-darkBg font-bold hover:opacity-90 disabled:opacity-50"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
