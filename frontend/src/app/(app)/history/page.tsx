'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { useAuthStore } from '@/store/authStore';

type ContentType = 'hook' | 'script' | 'shotlist' | 'voiceover' | 'caption' | 'broll' | 'calendar' | 'all';

interface ContentItem {
  id: string;
  type: string;
  prompt: string;
  created_at: string;
  data: any;
}

export default function HistoryPage() {
  const { user } = useAuthStore();
  const [contents, setContents] = useState<ContentItem[]>([]);
  const [filteredContents, setFilteredContents] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<ContentType>('all');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadHistory();
  }, []);

  useEffect(() => {
    filterContents();
  }, [filter, searchQuery, contents]);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await api.getContentHistory();
      setContents(data);
    } catch (err) {
      console.error('Error loading history:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterContents = () => {
    let filtered = contents;

    // Filter by type
    if (filter !== 'all') {
      filtered = filtered.filter((item) => item.type === filter);
    }

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter((item) =>
        item.prompt.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredContents(filtered);
  };

  const handleExport = async (id: string) => {
    try {
      const pdfBlob = await api.exportPDF(id);
      const url = window.URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `content_${id}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Export error:', err);
      alert('PDF Export fehlgeschlagen');
    }
  };

  const getTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      hook: 'Hooks',
      script: 'Script',
      shotlist: 'Shotlist',
      voiceover: 'Voiceover',
      caption: 'Caption',
      broll: 'B-Roll',
      calendar: 'Calendar',
    };
    return labels[type] || type;
  };

  const getTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      hook: 'bg-blue-100 text-blue-800',
      script: 'bg-green-100 text-green-800',
      shotlist: 'bg-purple-100 text-purple-800',
      voiceover: 'bg-yellow-100 text-yellow-800',
      caption: 'bg-pink-100 text-pink-800',
      broll: 'bg-indigo-100 text-indigo-800',
      calendar: 'bg-red-100 text-red-800',
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Wird geladen...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="px-4 sm:px-0">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Content History</h1>
        <p className="mt-2 text-sm text-gray-600">
          Alle deine generierten Inhalte an einem Ort
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white shadow sm:rounded-lg p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
              Suche
            </label>
            <input
              type="text"
              id="search"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Nach Thema suchen..."
              className="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label htmlFor="filter" className="block text-sm font-medium text-gray-700 mb-2">
              Filter nach Typ
            </label>
            <select
              id="filter"
              value={filter}
              onChange={(e) => setFilter(e.target.value as ContentType)}
              className="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">Alle Typen</option>
              <option value="hook">Hooks</option>
              <option value="script">Scripts</option>
              <option value="shotlist">Shotlists</option>
              <option value="voiceover">Voiceovers</option>
              <option value="caption">Captions</option>
              <option value="broll">B-Roll</option>
              <option value="calendar">Calendars</option>
            </select>
          </div>
        </div>

        <div className="mt-4 text-sm text-gray-500">
          {filteredContents.length} {filteredContents.length === 1 ? 'Ergebnis' : 'Ergebnisse'}
        </div>
      </div>

      {/* Content List */}
      {filteredContents.length === 0 ? (
        <div className="bg-white shadow sm:rounded-lg p-12 text-center">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">Keine Inhalte gefunden</h3>
          <p className="mt-1 text-sm text-gray-500">
            {searchQuery || filter !== 'all'
              ? 'Versuche andere Suchkriterien'
              : 'Starte mit der Generierung von Content'}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredContents.map((item) => (
            <div
              key={item.id}
              className="bg-white shadow sm:rounded-lg p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span
                      className={`inline-flex items-center px-3 py-0.5 rounded-full text-xs font-medium ${getTypeColor(
                        item.type
                      )}`}
                    >
                      {getTypeLabel(item.type)}
                    </span>
                    <span className="text-sm text-gray-500">
                      {new Date(item.created_at).toLocaleString('de-DE')}
                    </span>
                  </div>

                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    {item.prompt}
                  </h3>

                  <div className="text-sm text-gray-500">
                    {item.type === 'hook' && `${item.data.hooks?.length || 0} Hooks`}
                    {item.type === 'script' && `${item.data.scenes?.length || 0} Scenes`}
                    {item.type === 'shotlist' && `${item.data.shots?.length || 0} Shots`}
                    {item.type === 'voiceover' && `${item.data.word_count || 0} Wörter`}
                    {item.type === 'caption' && `${item.data.hashtags?.length || 0} Hashtags`}
                    {item.type === 'broll' && `${item.data.broll_ideas?.length || 0} Ideas`}
                    {item.type === 'calendar' && `${item.data.days?.length || 0} Tage`}
                  </div>
                </div>

                <button
                  onClick={() => handleExport(item.id)}
                  className="ml-4 inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  PDF
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
