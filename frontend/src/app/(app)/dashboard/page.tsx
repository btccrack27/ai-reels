'use client';

import { useState, useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';
import { api } from '@/lib/api';
import Link from 'next/link';

interface Stats {
  total_contents: number;
  this_month: number;
  hooks: number;
  scripts: number;
  calendars: number;
}

interface RecentContent {
  id: string;
  type: string;
  prompt: string;
  created_at: string;
}

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<Stats | null>(null);
  const [recentContent, setRecentContent] = useState<RecentContent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      // For now, we'll use mock data since the API endpoints might not be fully implemented yet
      // In production, you would call actual API endpoints here

      // Mock stats
      setStats({
        total_contents: 42,
        this_month: 15,
        hooks: 25,
        scripts: 12,
        calendars: 5,
      });

      // Load recent content from history API
      try {
        const history = await api.getContentHistory();
        setRecentContent(history.slice(0, 5));
      } catch (err) {
        console.error('Error loading recent content:', err);
        setRecentContent([]);
      }
    } catch (err) {
      console.error('Error loading dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    { name: 'Hooks generieren', href: '/generate?tab=hook', icon: '🎣', color: 'bg-blue-500' },
    { name: 'Script erstellen', href: '/generate?tab=script', icon: '📝', color: 'bg-green-500' },
    { name: 'Calendar planen', href: '/generate?tab=calendar', icon: '📅', color: 'bg-purple-500' },
    { name: 'History ansehen', href: '/history', icon: '📚', color: 'bg-yellow-500' },
  ];

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
      {/* Welcome */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Willkommen zurück, {user?.name}!
        </h1>
        <p className="mt-2 text-sm text-gray-600">
          Hier ist eine Übersicht deiner Content-Generierung
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="text-3xl">📊</div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Gesamt generiert
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats?.total_contents || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="text-3xl">🗓️</div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Diesen Monat
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats?.this_month || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="text-3xl">🎣</div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Hooks</dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats?.hooks || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="text-3xl">📝</div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Scripts</dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats?.scripts || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Quick Actions */}
        <div className="bg-white shadow sm:rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Schnellaktionen</h2>
          <div className="grid grid-cols-2 gap-4">
            {quickActions.map((action) => (
              <Link
                key={action.name}
                href={action.href}
                className="flex flex-col items-center p-4 bg-gray-50 rounded-lg hover:shadow-md transition-shadow"
              >
                <div
                  className={`w-12 h-12 ${action.color} rounded-full flex items-center justify-center text-2xl mb-2`}
                >
                  {action.icon}
                </div>
                <span className="text-sm font-medium text-gray-900 text-center">
                  {action.name}
                </span>
              </Link>
            ))}
          </div>
        </div>

        {/* Recent Content */}
        <div className="bg-white shadow sm:rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-medium text-gray-900">Zuletzt generiert</h2>
            <Link
              href="/history"
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              Alle ansehen →
            </Link>
          </div>

          {recentContent.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>Noch keine Inhalte generiert</p>
              <Link
                href="/generate"
                className="mt-2 inline-block text-blue-600 hover:text-blue-700 font-medium"
              >
                Jetzt starten
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {recentContent.map((item) => (
                <div
                  key={item.id}
                  className="flex items-start justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {item.prompt}
                    </p>
                    <div className="flex items-center mt-1 space-x-2">
                      <span className="text-xs text-gray-500 capitalize">{item.type}</span>
                      <span className="text-xs text-gray-400">•</span>
                      <span className="text-xs text-gray-500">
                        {new Date(item.created_at).toLocaleDateString('de-DE')}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Current Plan */}
      <div className="mt-8 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg shadow-lg p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold">Aktueller Plan: {user?.role?.toUpperCase() || 'FREE'}</h3>
            <p className="mt-1 text-blue-100 text-sm">
              {user?.role === 'free' || !user?.role
                ? 'Upgrade für unbegrenzten Zugriff auf alle Features'
                : 'Du hast vollen Zugriff auf alle Features'}
            </p>
          </div>
          {(user?.role === 'free' || !user?.role) && (
            <Link
              href="/subscription"
              className="bg-white text-blue-600 px-6 py-2 rounded-md font-medium hover:bg-blue-50 transition-colors"
            >
              Jetzt upgraden
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
