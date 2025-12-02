'use client';

import { useState } from 'react';
import { api } from '@/lib/api';

interface BRollResult {
  id: string;
  broll_ideas: string[];
  prompt: string;
  created_at: string;
}

export default function BRollGenerator() {
  const [prompt, setPrompt] = useState('');
  const [context, setContext] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<BRollResult | null>(null);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await api.generateBRoll(prompt, context || undefined);
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Generierung fehlgeschlagen');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    if (!result) return;

    try {
      const pdfBlob = await api.exportPDF(result.id);
      const url = window.URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `broll_${result.id}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      setError('PDF Export fehlgeschlagen');
    }
  };

  return (
    <div className="space-y-6">
      {/* Form */}
      <div className="bg-white shadow sm:rounded-lg p-6">
        <form onSubmit={handleGenerate} className="space-y-4">
          <div>
            <label htmlFor="prompt" className="block text-sm font-medium text-gray-700">
              Thema / Prompt *
            </label>
            <textarea
              id="prompt"
              rows={3}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="z.B. Travel Vlog Bali, Cooking Tutorial, Fitness Workout"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
          </div>

          <div>
            <label htmlFor="context" className="block text-sm font-medium text-gray-700">
              Zusätzlicher Kontext (optional)
            </label>
            <textarea
              id="context"
              rows={2}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="z.B. Stil: Cinematic, Location: Indoor/Outdoor, Mood: Energetic"
              value={context}
              onChange={(e) => setContext(e.target.value)}
            />
          </div>

          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {loading ? 'Wird generiert...' : '10 B-Roll Ideas generieren'}
          </button>
        </form>
      </div>

      {/* Results */}
      {result && (
        <div className="bg-white shadow sm:rounded-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-gray-900">
              B-Roll Ideas ({result.broll_ideas.length})
            </h3>
            <button
              onClick={handleExport}
              className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              PDF Download
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {result.broll_ideas.map((idea, index) => (
              <div
                key={index}
                className="flex items-center p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-100 hover:shadow-md transition-shadow"
              >
                <div className="flex-shrink-0 w-10 h-10 flex items-center justify-center bg-blue-600 text-white rounded-lg text-sm font-bold">
                  {index + 1}
                </div>
                <p className="ml-4 text-gray-900 font-medium">{idea}</p>
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <p className="text-xs font-medium text-gray-500 mb-2">VERWENDUNGSTIPPS:</p>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>• Verwende B-Roll um deine Hauptaufnahmen aufzuwerten</li>
              <li>• Plane 2-3 Sekunden pro B-Roll Shot ein</li>
              <li>• Kombiniere verschiedene Kamerawinkel für mehr Dynamik</li>
              <li>• Nutze B-Roll um Übergänge zu glätten</li>
            </ul>
          </div>

          <div className="mt-4 text-sm text-gray-500">
            <p>Thema: {result.prompt}</p>
            <p>Generiert: {new Date(result.created_at).toLocaleString('de-DE')}</p>
          </div>
        </div>
      )}
    </div>
  );
}
