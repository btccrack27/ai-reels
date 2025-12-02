'use client';

import { useState } from 'react';
import HookGenerator from '@/components/generators/HookGenerator';
import ScriptGenerator from '@/components/generators/ScriptGenerator';
import ShotlistGenerator from '@/components/generators/ShotlistGenerator';
import VoiceoverGenerator from '@/components/generators/VoiceoverGenerator';
import CaptionGenerator from '@/components/generators/CaptionGenerator';
import BRollGenerator from '@/components/generators/BRollGenerator';
import CalendarGenerator from '@/components/generators/CalendarGenerator';

type ContentType = 'hook' | 'script' | 'shotlist' | 'voiceover' | 'caption' | 'broll' | 'calendar';

const tabs = [
  { id: 'hook' as ContentType, name: 'Hooks', description: '10 virale Hooks' },
  { id: 'script' as ContentType, name: 'Script', description: '2-4 Szenen Script' },
  { id: 'shotlist' as ContentType, name: 'Shotlist', description: '3-4 Shots' },
  { id: 'voiceover' as ContentType, name: 'Voiceover', description: '10-20 Sek' },
  { id: 'caption' as ContentType, name: 'Caption', description: 'Caption + 15 Hashtags' },
  { id: 'broll' as ContentType, name: 'B-Roll', description: '10 B-Roll Ideas' },
  { id: 'calendar' as ContentType, name: 'Calendar', description: '30-Tage Plan' },
];

export default function GeneratePage() {
  const [activeTab, setActiveTab] = useState<ContentType>('hook');

  return (
    <div className="px-4 sm:px-0">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Content Generator</h1>
        <p className="mt-2 text-sm text-gray-600">
          Wähle einen Content-Typ und generiere virale Reels-Inhalte mit AI
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8 overflow-x-auto" aria-label="Tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm
                ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }
              `}
            >
              <div className="flex flex-col items-start">
                <span>{tab.name}</span>
                <span className="text-xs text-gray-400">{tab.description}</span>
              </div>
            </button>
          ))}
        </nav>
      </div>

      {/* Generator Content */}
      <div className="mt-8">
        {activeTab === 'hook' && <HookGenerator />}
        {activeTab === 'script' && <ScriptGenerator />}
        {activeTab === 'shotlist' && <ShotlistGenerator />}
        {activeTab === 'voiceover' && <VoiceoverGenerator />}
        {activeTab === 'caption' && <CaptionGenerator />}
        {activeTab === 'broll' && <BRollGenerator />}
        {activeTab === 'calendar' && <CalendarGenerator />}
      </div>
    </div>
  );
}
