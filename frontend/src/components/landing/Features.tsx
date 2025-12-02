export default function Features() {
  const features = [
    {
      name: 'Hooks',
      description: '10 virale Hooks in Sekunden. Fessle deine Zuschauer in den ersten 3 Sekunden.',
      icon: '🎣',
    },
    {
      name: 'Scripts',
      description: 'Komplette 2-4 Szenen Scripts mit CTA. Perfekt strukturiert für 10-20 Sekunden Reels.',
      icon: '📝',
    },
    {
      name: 'Shotlist',
      description: '3-4 professionelle Shot-Beschreibungen mit Kamerawinkeln und Timing.',
      icon: '🎬',
    },
    {
      name: 'Voiceover',
      description: '10-20 Sekunden Voiceover-Text. Sofort einsetzbar für deine Videos.',
      icon: '🎙️',
    },
    {
      name: 'Captions',
      description: 'Perfekte Caption + 15 relevante Hashtags. Maximiere deine Reichweite.',
      icon: '💬',
    },
    {
      name: 'B-Roll Ideas',
      description: '10 kreative B-Roll Ideen um deine Videos professioneller zu machen.',
      icon: '🎥',
    },
    {
      name: '30-Tage Calendar',
      description: 'Kompletter Content-Plan für einen Monat. Nie wieder ohne Ideen.',
      icon: '📅',
    },
  ];

  return (
    <div className="py-12 bg-white" id="features">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="lg:text-center">
          <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Features
          </h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            7 Tools für viralen Content
          </p>
          <p className="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Alles was du brauchst um konstant hochwertige Reels zu produzieren.
            Powered by Claude AI.
          </p>
        </div>

        <div className="mt-10">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <div key={feature.name} className="relative">
                <div className="flow-root bg-gray-50 rounded-lg px-6 pb-8 pt-6 hover:shadow-lg transition-shadow">
                  <div className="-mt-6">
                    <div>
                      <span className="inline-flex items-center justify-center p-3 bg-blue-600 rounded-md shadow-lg text-3xl">
                        {feature.icon}
                      </span>
                    </div>
                    <h3 className="mt-8 text-lg font-medium text-gray-900 tracking-tight">
                      {feature.name}
                    </h3>
                    <p className="mt-5 text-base text-gray-500">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-16 bg-blue-50 rounded-lg p-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold text-gray-900">
              Wie funktioniert es?
            </h3>
            <div className="mt-8 grid grid-cols-1 gap-8 sm:grid-cols-3">
              <div>
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white text-xl font-bold mx-auto">
                  1
                </div>
                <h4 className="mt-4 text-lg font-medium">Thema eingeben</h4>
                <p className="mt-2 text-gray-600">
                  Beschreibe dein Video-Thema in wenigen Worten
                </p>
              </div>
              <div>
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white text-xl font-bold mx-auto">
                  2
                </div>
                <h4 className="mt-4 text-lg font-medium">KI generiert Content</h4>
                <p className="mt-2 text-gray-600">
                  Claude AI erstellt professionelle Inhalte in Sekunden
                </p>
              </div>
              <div>
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white text-xl font-bold mx-auto">
                  3
                </div>
                <h4 className="mt-4 text-lg font-medium">Reel produzieren</h4>
                <p className="mt-2 text-gray-600">
                  Nutze die Inhalte für deine Videos und gehe viral
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
