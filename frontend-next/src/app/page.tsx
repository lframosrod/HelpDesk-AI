"use client";

import { useState } from "react";
import { searchRAG, uploadDocument } from "@/lib/api";

export default function HelpDeskDashboard() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState<{
    query: string;
    ai_answer: string;
    sources: any[];
  } | null>(null);
  const [isSearching, setIsSearching] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsSearching(true);
    try {
      const result = await searchRAG(query);
      setAnswer(result);
    } catch (error) {
      console.error(error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    try {
      await uploadDocument(file);
      alert("Documento en procesamiento. Los artículos se generarán en breve.");
    } catch (error) {
      alert("Error al procesar el documento.");
    } finally {
      setIsUploading(false);
      e.target.value = ""; // Limpiar input
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 text-gray-900 p-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header & Upload */}
        <div className="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div>
            <h1 className="text-2xl font-bold text-blue-900">HelpDesk AI</h1>
            <p className="text-sm text-gray-500">
              Base de conocimiento impulsada por RAG
            </p>
          </div>
          <div>
            <label className="bg-blue-600 text-white px-4 py-2 rounded-lg cursor-pointer hover:bg-blue-700 transition">
              {isUploading ? "Procesando..." : "+ Subir Manual (PDF)"}
              <input
                type="file"
                accept=".pdf"
                className="hidden"
                onChange={handleFileUpload}
                disabled={isUploading}
              />
            </label>
          </div>
        </div>

        {/* Search Section */}
        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100">
          <form onSubmit={handleSearch} className="flex gap-4">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ej: ¿Qué hago si el equipo no enciende?"
              className="flex-1 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
            <button
              type="submit"
              disabled={isSearching}
              className="bg-gray-900 text-white px-8 rounded-lg font-medium hover:bg-gray-800 disabled:opacity-50"
            >
              {isSearching ? "Buscando..." : "Consultar AI"}
            </button>
          </form>

          {/* AI Response Area */}
          {answer && (
            <div className="mt-8 p-6 bg-blue-50 rounded-lg border border-blue-100">
              <h3 className="font-semibold text-blue-900 mb-2">
                Respuesta Generada
              </h3>
              <p className="text-gray-800 whitespace-pre-wrap">
                {answer.ai_answer}
              </p>

              <div className="mt-6">
                <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
                  Fuentes Consultadas
                </h4>
                <div className="grid gap-3">
                  {answer.sources.map((source, idx) => (
                    <div
                      key={idx}
                      className="bg-white p-3 rounded border border-gray-200 text-sm text-gray-600"
                    >
                      <span className="font-medium text-gray-900">
                        Documento ID: {source.document_id}
                      </span>
                      <p className="mt-1 line-clamp-2">{source.content}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
