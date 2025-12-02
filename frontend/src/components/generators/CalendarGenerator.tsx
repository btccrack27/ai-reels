'use client';

import { useState } from 'react';
import { api } from '@/lib/api';

interface DayContent {
  day: number;
  hook: string;
  theme: string;
}

interface CalendarResult {
  id: string;
  days: DayContent[];
  niche: string;
  created_at: string;
}

export default function CalendarGenerator() {
  const [niche, setNiche] = useState('');
  const [context, setContext] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<CalendarResult | null>(null);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await api.generateCalendar(niche, context || undefined);
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
      a.download = `calendar_${result.id}.pdf`;
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
            <label htmlFor="niche" className="block text-sm font-medium text-gray-700">
              Nische / Themenbereich *
            </label>
            <input
              type="text"
              id="niche"
              required
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="z.B. Fitness, Kochen, Reisen, Personal Development"
              value={niche}
              onChange={(e) => setNiche(e.target.value)}
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
              placeholder="z.B. Zielgruppe: Anfänger, Stil: Educational, Frequenz: täglich"
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
            {loading ? 'Wird generiert...' : '30-Tage Content-Plan generieren'}
          </button>
        </form>
      </div>

      {/* Results */}
      {result && (
        <div className="bg-white shadow sm:rounded-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-gray-900">
              30-Tage Content Calendar
            </h3>
            <button
              onClick={handleExport}
              className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              PDF Download
            </button>
          </div>

          <div className="mb-4 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm font-medium text-blue-900">
              Nische: <span className="font-bold">{result.niche}</span>
            </p>
            <p className="text-xs text-blue-700 mt-1">
              Verwende diesen Plan als Grundlage für deine Content-Strategie. Passe die Themen an deine Zielgruppe an.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {result.days.map((day) => (
              <div
                key={day.day}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 text-white text-sm font-bold">
                    {day.day}
                  </span>
                  <span className="text-xs text-gray-500">Tag {day.day}</span>
                </div>

                <div className="space-y-2">
                  <div>
                    <p className="text-xs font-medium text-gray-500 uppercase">Thema:</p>
                    <p className="text-sm font-semibold text-gray-900">{day.theme}</p>
                  </div>

                  <div>
                    <p className="text-xs font-medium text-gray-500 uppercase">Hook:</p>
                    <p className="text-sm text-gray-700">{day.hook}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <p className="text-xs font-medium text-gray-500 mb-2">CONTENT-STRATEGIE TIPPS:</p>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>• Plane 1-2 Wochen im Voraus und bleibe flexibel</li>
              <li>• Kombiniere verschiedene Content-Formate (Tutorial, Behind-the-Scenes, Q&A)</li>
              <li>• Analysiere welche Themen am besten performen</li>
              <li>• Erstelle Batches von 3-5 Videos am Stück</li>
              <li>• Nutze Analytics um deinen Content-Plan zu optimieren</li>
            </ul>
          </div>

          <div className="mt-4 text-sm text-gray-500">
            <p>Nische: {result.niche}</p>
            <p>Generiert: {new Date(result.created_at).toLocaleString('de-DE')}</p>
          </div>
        </div>
      )}
    </div>
  );
}
