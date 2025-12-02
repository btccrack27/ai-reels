'use client';

import { useState } from 'react';
import { api } from '@/lib/api';

interface Scene {
  scene_number: number;
  type: string;
  text: string;
  visual_description: string;
  duration_seconds: number;
}

interface ScriptResult {
  id: string;
  scenes: Scene[];
  cta: string;
  total_duration: number;
  prompt: string;
  created_at: string;
}

export default function ScriptGenerator() {
  const [prompt, setPrompt] = useState('');
  const [context, setContext] = useState('');
  const [duration, setDuration] = useState(15);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<ScriptResult | null>(null);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await api.generateScript(prompt, context || undefined, duration);
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
      a.download = `script_${result.id}.pdf`;
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
              placeholder="z.B. 5 Tipps für besseren Schlaf"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
          </div>

          <div>
            <label htmlFor="duration" className="block text-sm font-medium text-gray-700">
              Ziel-Dauer (Sekunden)
            </label>
            <select
              id="duration"
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value={10}>10 Sekunden</option>
              <option value={15}>15 Sekunden</option>
              <option value={20}>20 Sekunden</option>
            </select>
          </div>

          <div>
            <label htmlFor="context" className="block text-sm font-medium text-gray-700">
              Zusätzlicher Kontext (optional)
            </label>
            <textarea
              id="context"
              rows={2}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="z.B. Stil: Educational, Zielgruppe: Studenten"
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
            {loading ? 'Wird generiert...' : 'Script generieren'}
          </button>
        </form>
      </div>

      {/* Results */}
      {result && (
        <div className="bg-white shadow sm:rounded-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-gray-900">
              Generiertes Script ({result.total_duration}s)
            </h3>
            <button
              onClick={handleExport}
              className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              PDF Download
            </button>
          </div>

          <div className="space-y-4">
            {result.scenes.map((scene) => (
              <div key={scene.scene_number} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-sm font-medium text-gray-900">
                    Szene {scene.scene_number} ({scene.type})
                  </h4>
                  <span className="text-xs text-gray-500">{scene.duration_seconds}s</span>
                </div>
                <div className="space-y-2">
                  <div>
                    <p className="text-xs font-medium text-gray-500">Text:</p>
                    <p className="text-sm text-gray-900">{scene.text}</p>
                  </div>
                  <div>
                    <p className="text-xs font-medium text-gray-500">Visual:</p>
                    <p className="text-sm text-gray-700">{scene.visual_description}</p>
                  </div>
                </div>
              </div>
            ))}

            <div className="border border-blue-200 bg-blue-50 rounded-lg p-4">
              <p className="text-xs font-medium text-blue-900 mb-1">Call to Action:</p>
              <p className="text-sm text-blue-800">{result.cta}</p>
            </div>
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
