'use client';

import { useEffect } from 'react';
import { useMiraiStore } from '@/store/useMiraiStore';
import { wsService } from '@/services/websocketService';

import SplashScreen from '@/components/screens/SplashScreen';
import NameEntryScreen from '@/components/screens/NameEntryScreen';
import HomeScreen from '@/components/screens/HomeScreen';
import HeroSelectScreen from '@/components/screens/HeroSelectScreen';
import StrategyScreen from '@/components/screens/StrategyScreen';
import AnalysisScreen from '@/components/screens/AnalysisScreen';
import BattleScreen from '@/components/screens/BattleScreen';
import BrainViewScreen from '@/components/screens/BrainViewScreen';
import ReplayScreen from '@/components/screens/ReplayScreen';
import LearningScreen from '@/components/screens/LearningScreen';
import BrainOverlay from '@/components/overlays/BrainOverlay';

export default function MainPage() {
  const currentScreen = useMiraiStore((state) => state.currentScreen);

  useEffect(() => {
    // Initiate WebSocket live telemetry connection
    wsService.connect();
  }, []);

  const renderScreen = () => {
    switch (currentScreen) {
      case 'splash':
        return <SplashScreen />;
      case 'name_entry':
        return <NameEntryScreen />;
      case 'home':
        return <HomeScreen />;
      case 'hero_select':
        return <HeroSelectScreen />;
      case 'strategy':
        return <StrategyScreen />;
      case 'analysis':
        return <AnalysisScreen />;
      case 'battle':
        return <BattleScreen />;
      case 'brain_view':
        return <BrainViewScreen />;
      case 'replay':
        return <ReplayScreen />;
      case 'learning':
        return <LearningScreen />;
      default:
        return <SplashScreen />;
    }
  };

  return (
    <>
      {renderScreen()}
      <BrainOverlay />
    </>
  );
}
