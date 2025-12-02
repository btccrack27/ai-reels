'use client';

import { useState } from 'react';
import { useAuthStore } from '@/store/authStore';
import { api } from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function Pricing() {
  const { isAuthenticated } = useAuthStore();
  const router = useRouter();
  const [loading, setLoading] = useState<string | null>(null);

  const plans = [
    {
      name: 'Free',
      price: '0',
      priceId: null,
      description: 'Perfekt zum Testen',
      features: [
        '5 Hooks pro Monat',
        '3 Scripts pro Monat',
        '1 Calendar pro Monat',
        '2 PDF Exports pro Monat',
        'Basis-Support',
      ],
      cta: 'Kostenlos starten',
      highlighted: false,
    },
    {
      name: 'Basic',
      price: '19',
      priceId: 'price_basic', // Replace with actual Stripe price ID
      description: 'Für Content Creator',
      features: [
        '50 Hooks pro Monat',
        '30 Scripts pro Monat',
        '5 Calendars pro Monat',
        '20 PDF Exports pro Monat',
        'Alle 7 Tools inklusive',
        'E-Mail Support',
      ],
      cta: 'Jetzt starten',
      highlighted: true,
    },
    {
      name: 'Pro',
      price: '49',
      priceId: 'price_pro', // Replace with actual Stripe price ID
      description: 'Für Profis & Agenturen',
      features: [
        '500 Hooks pro Monat',
        '300 Scripts pro Monat',
        '20 Calendars pro Monat',
        '200 PDF Exports pro Monat',
        'Alle 7 Tools inklusive',
        'Priority Support',
        'API Zugang (coming soon)',
      ],
      cta: 'Jetzt upgraden',
      highlighted: false,
    },
    {
      name: 'Enterprise',
      price: '199',
      priceId: 'price_enterprise', // Replace with actual Stripe price ID
      description: 'Unbegrenzt für Teams',
      features: [
        'Unbegrenzte Generierungen',
        'Unbegrenzte PDF Exports',
        'Alle 7 Tools inklusive',
        'Dedizierter Support',
        'API Zugang',
        'Custom Integrationen',
        'Team-Management',
      ],
      cta: 'Kontakt aufnehmen',
      highlighted: false,
    },
  ];

  const handleCheckout = async (priceId: string | null, planName: string) => {
    if (!priceId) {
      // Free plan - redirect to register
      router.push('/register');
      return;
    }

    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    setLoading(planName);

    try {
      const { checkout_url } = await api.createCheckoutSession(priceId);
      window.location.href = checkout_url;
    } catch (err: any) {
      console.error('Checkout error:', err);
      alert('Checkout fehlgeschlagen. Bitte versuche es erneut.');
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="bg-gray-50 py-12" id="pricing">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Pricing
          </h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Der richtige Plan für jeden
          </p>
          <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
            Starte kostenlos oder wähle einen Plan der zu deinen Bedürfnissen passt.
            Jederzeit kündbar.
          </p>
        </div>

        <div className="mt-12 space-y-4 sm:mt-16 sm:space-y-0 sm:grid sm:grid-cols-2 sm:gap-6 lg:max-w-4xl lg:mx-auto xl:max-w-none xl:grid-cols-4">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`rounded-lg shadow-lg divide-y divide-gray-200 ${
                plan.highlighted
                  ? 'border-2 border-blue-600 relative'
                  : 'border border-gray-200'
              }`}
            >
              {plan.highlighted && (
                <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                  <span className="inline-flex rounded-full bg-blue-600 px-4 py-1 text-xs font-semibold tracking-wide uppercase text-white">
                    Beliebt
                  </span>
                </div>
              )}

              <div className="p-6 bg-white rounded-t-lg">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                  {plan.name}
                </h3>
                <p className="mt-4 text-sm text-gray-500">{plan.description}</p>
                <p className="mt-8">
                  <span className="text-4xl font-extrabold text-gray-900">
                    €{plan.price}
                  </span>
                  <span className="text-base font-medium text-gray-500">/Monat</span>
                </p>
                <button
                  onClick={() => handleCheckout(plan.priceId, plan.name)}
                  disabled={loading === plan.name}
                  className={`mt-8 block w-full rounded-md py-2 text-sm font-semibold text-center ${
                    plan.highlighted
                      ? 'bg-blue-600 text-white hover:bg-blue-700'
                      : 'bg-blue-50 text-blue-700 hover:bg-blue-100'
                  } ${loading === plan.name ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  {loading === plan.name ? 'Lädt...' : plan.cta}
                </button>
              </div>

              <div className="pt-6 pb-8 px-6 bg-gray-50 rounded-b-lg">
                <h4 className="text-sm font-medium text-gray-900 tracking-wide uppercase">
                  Enthalten:
                </h4>
                <ul className="mt-6 space-y-4">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex space-x-3">
                      <svg
                        className="flex-shrink-0 h-5 w-5 text-green-500"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                          clipRule="evenodd"
                        />
                      </svg>
                      <span className="text-sm text-gray-500">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 text-center">
          <p className="text-sm text-gray-500">
            Alle Preise in Euro. Keine versteckten Kosten. Jederzeit kündbar.
          </p>
        </div>
      </div>
    </div>
  );
}
