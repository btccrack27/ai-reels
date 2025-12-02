'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { useAuthStore } from '@/store/authStore';

interface SubscriptionData {
  plan: string;
  status: string;
  current_period_end: string;
  cancel_at_period_end: boolean;
}

interface UsageData {
  hooks: { used: number; limit: number };
  scripts: { used: number; limit: number };
  shotlists: { used: number; limit: number };
  voiceovers: { used: number; limit: number };
  captions: { used: number; limit: number };
  brolls: { used: number; limit: number };
  calendars: { used: number; limit: number };
  pdf_exports: { used: number; limit: number };
}

export default function SubscriptionPage() {
  const { user } = useAuthStore();
  const [subscription, setSubscription] = useState<SubscriptionData | null>(null);
  const [usage, setUsage] = useState<UsageData | null>(null);
  const [loading, setLoading] = useState(true);
  const [portalLoading, setPortalLoading] = useState(false);

  useEffect(() => {
    loadSubscriptionData();
  }, []);

  const loadSubscriptionData = async () => {
    try {
      setLoading(true);
      const [subData, usageData] = await Promise.all([
        api.getSubscriptionStatus(),
        api.getUsageStats(),
      ]);
      setSubscription(subData);
      setUsage(usageData);
    } catch (err) {
      console.error('Error loading subscription:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleBillingPortal = async () => {
    try {
      setPortalLoading(true);
      const { portal_url } = await api.createPortalSession();
      window.location.href = portal_url;
    } catch (err) {
      console.error('Portal error:', err);
      alert('Fehler beim Öffnen des Billing Portals');
    } finally {
      setPortalLoading(false);
    }
  };

  const handleUpgrade = async (priceId: string) => {
    try {
      const { checkout_url } = await api.createCheckoutSession(priceId);
      window.location.href = checkout_url;
    } catch (err) {
      console.error('Checkout error:', err);
      alert('Fehler beim Checkout');
    }
  };

  const getProgressColor = (used: number, limit: number) => {
    const percentage = (used / limit) * 100;
    if (percentage >= 90) return 'bg-red-600';
    if (percentage >= 70) return 'bg-yellow-600';
    return 'bg-blue-600';
  };

  const plans = [
    {
      name: 'Basic',
      price: '19',
      priceId: 'price_basic',
      features: ['50 Hooks', '30 Scripts', '5 Calendars', '20 PDFs'],
    },
    {
      name: 'Pro',
      price: '49',
      priceId: 'price_pro',
      features: ['500 Hooks', '300 Scripts', '20 Calendars', '200 PDFs'],
    },
    {
      name: 'Enterprise',
      price: '199',
      priceId: 'price_enterprise',
      features: ['Unlimited', 'Unlimited', 'Unlimited', 'Unlimited'],
    },
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

  const currentPlan = subscription?.plan?.toUpperCase() || 'FREE';

  return (
    <div className="px-4 sm:px-0">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Subscription & Usage</h1>
        <p className="mt-2 text-sm text-gray-600">
          Verwalte dein Abo und sieh deine Nutzungsstatistiken
        </p>
      </div>

      {/* Current Plan */}
      <div className="bg-white shadow sm:rounded-lg p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-medium text-gray-900">Aktueller Plan</h2>
            <p className="text-3xl font-bold text-blue-600 mt-2">{currentPlan}</p>
            {subscription?.current_period_end && (
              <p className="text-sm text-gray-500 mt-1">
                Erneuert am{' '}
                {new Date(subscription.current_period_end).toLocaleDateString('de-DE')}
              </p>
            )}
            {subscription?.cancel_at_period_end && (
              <p className="text-sm text-red-600 mt-1">
                Wird am Ende der Periode gekündigt
              </p>
            )}
          </div>

          {currentPlan !== 'FREE' && (
            <button
              onClick={handleBillingPortal}
              disabled={portalLoading}
              className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              {portalLoading ? 'Lädt...' : 'Billing Portal'}
            </button>
          )}
        </div>

        {subscription?.status && (
          <div className="mt-4">
            <span
              className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
                subscription.status === 'active'
                  ? 'bg-green-100 text-green-800'
                  : 'bg-yellow-100 text-yellow-800'
              }`}
            >
              Status: {subscription.status}
            </span>
          </div>
        )}
      </div>

      {/* Usage Statistics */}
      {usage && (
        <div className="bg-white shadow sm:rounded-lg p-6 mb-6">
          <h2 className="text-lg font-medium text-gray-900 mb-6">
            Nutzung diesen Monat
          </h2>

          <div className="space-y-6">
            {Object.entries(usage).map(([key, value]) => (
              <div key={key}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium text-gray-700 capitalize">
                    {key.replace('_', ' ')}
                  </span>
                  <span className="text-gray-500">
                    {value.used} / {value.limit === -1 ? '∞' : value.limit}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${getProgressColor(
                      value.used,
                      value.limit
                    )}`}
                    style={{
                      width:
                        value.limit === -1
                          ? '100%'
                          : `${Math.min((value.used / value.limit) * 100, 100)}%`,
                    }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Upgrade Options */}
      {currentPlan === 'FREE' && (
        <div className="bg-white shadow sm:rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-6">
            Upgrade für mehr Features
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {plans.map((plan) => (
              <div
                key={plan.name}
                className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
              >
                <h3 className="text-lg font-semibold text-gray-900">{plan.name}</h3>
                <p className="mt-4">
                  <span className="text-3xl font-bold text-gray-900">€{plan.price}</span>
                  <span className="text-gray-500">/Monat</span>
                </p>

                <ul className="mt-6 space-y-3">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-center text-sm text-gray-600">
                      <svg
                        className="h-5 w-5 text-green-500 mr-2"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                          clipRule="evenodd"
                        />
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>

                <button
                  onClick={() => handleUpgrade(plan.priceId)}
                  className="mt-6 w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Upgrade zu {plan.name}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
