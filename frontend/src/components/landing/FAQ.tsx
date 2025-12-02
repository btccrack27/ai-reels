'use client';

import { useState } from 'react';

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const faqs = [
    {
      question: 'Was ist der AI Reels Generator?',
      answer:
        'Der AI Reels Generator ist eine Plattform die dir hilft virale Inhalte für Instagram Reels, TikTok und YouTube Shorts zu erstellen. Mit 7 verschiedenen Tools kannst du Hooks, Scripts, Shotlists, Voiceovers, Captions, B-Roll Ideas und Content Calendars generieren - alles powered by Claude AI.',
    },
    {
      question: 'Wie funktioniert die Generierung?',
      answer:
        'Du gibst einfach dein Thema oder eine kurze Beschreibung ein. Unsere KI (Claude 3.5 Sonnet) analysiert deine Eingabe und erstellt professionelle, auf deine Nische zugeschnittene Inhalte in Sekunden. Du kannst die generierten Inhalte direkt nutzen oder als Inspiration verwenden.',
    },
    {
      question: 'Kann ich die generierten Inhalte kommerziell nutzen?',
      answer:
        'Ja, alle generierten Inhalte gehören dir und können kommerziell genutzt werden. Du kannst sie für deine eigenen Social Media Accounts, für Kunden oder in deiner Agentur einsetzen.',
    },
    {
      question: 'Was passiert wenn ich mein Limit erreiche?',
      answer:
        'Wenn du dein monatliches Limit erreichst, kannst du entweder bis zum nächsten Monat warten (bei Free) oder jederzeit auf einen höheren Plan upgraden. Deine bisherigen Inhalte bleiben natürlich verfügbar.',
    },
    {
      question: 'Kann ich meinen Plan jederzeit ändern?',
      answer:
        'Ja, du kannst jederzeit upgraden oder downgraden. Beim Upgrade hast du sofort Zugriff auf die höheren Limits. Beim Downgrade gelten die neuen Limits ab dem nächsten Abrechnungszyklus.',
    },
    {
      question: 'Werden meine Daten sicher gespeichert?',
      answer:
        'Ja, wir nehmen Datenschutz sehr ernst. Alle Daten werden verschlüsselt in einer sicheren Vercel Postgres Datenbank gespeichert. Deine generierten Inhalte sind nur für dich sichtbar.',
    },
    {
      question: 'Gibt es eine Geld-zurück-Garantie?',
      answer:
        'Ja, wir bieten eine 14-Tage Geld-zurück-Garantie für alle bezahlten Pläne. Wenn du nicht zufrieden bist, kontaktiere einfach unseren Support.',
    },
    {
      question: 'Welche Zahlungsmethoden werden akzeptiert?',
      answer:
        'Wir akzeptieren alle gängigen Kreditkarten (Visa, Mastercard, American Express) und weitere Zahlungsmethoden über Stripe. Die Abrechnung erfolgt monatlich.',
    },
  ];

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="bg-white py-12" id="faq">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">
            FAQ
          </h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Häufig gestellte Fragen
          </p>
        </div>

        <div className="mt-12">
          <dl className="space-y-4">
            {faqs.map((faq, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg overflow-hidden"
              >
                <dt>
                  <button
                    onClick={() => toggleFAQ(index)}
                    className="w-full text-left px-6 py-4 flex justify-between items-center hover:bg-gray-50 transition-colors"
                  >
                    <span className="text-lg font-medium text-gray-900">
                      {faq.question}
                    </span>
                    <svg
                      className={`h-6 w-6 text-gray-500 transform transition-transform ${
                        openIndex === index ? 'rotate-180' : ''
                      }`}
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </button>
                </dt>
                {openIndex === index && (
                  <dd className="px-6 pb-4">
                    <p className="text-base text-gray-500">{faq.answer}</p>
                  </dd>
                )}
              </div>
            ))}
          </dl>
        </div>
      </div>
    </div>
  );
}
