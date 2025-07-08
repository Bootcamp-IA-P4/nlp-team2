import { useState } from 'react';
import AppMetadata from './components/AppMetadata';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import AnalyzeTab from './components/AnalyzeTab';
import HistoryTab from './components/HistoryTab';
import GuideTab from './components/GuideTab';
import Dashboard from './components/Dashboard';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  // 🎯 FUNCIÓN PARA OBTENER TÍTULO POR TAB
  const getPageTitle = () => {
    switch (activeTab) {
      case 'dashboard':
        return 'Dashboard General';
      case 'analyze':
        return 'Análisis de Toxicidad';
      case 'history':
        return 'Historial de Análisis';
      case 'guide':
        return 'Guía de Toxicidad';
      default:
        return 'Dashboard General';
    }
  };

  // 🎯 FUNCIÓN PARA OBTENER DESCRIPCIÓN POR TAB
  const getPageDescription = () => {
    switch (activeTab) {
      case 'dashboard':
        return 'Resumen completo del estado de toxicidad y estadísticas generales de análisis';
      case 'analyze':
        return 'Analiza comentarios individuales o videos completos de YouTube usando inteligencia artificial';
      case 'history':
        return 'Revisa el historial completo de análisis previos de videos y comentarios';
      case 'guide':
        return 'Aprende sobre los diferentes tipos de contenido tóxico y cómo identificarlos';
      default:
        return 'Aplicación para análisis de toxicidad en comentarios de YouTube usando IA';
    }
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'analyze':
        return <AnalyzeTab />;
      case 'history':
        return <HistoryTab />;
      case 'guide':
        return <GuideTab />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <>
      {/* 🎯 METADATA GLOBAL QUE SE ACTUALIZA SEGÚN EL TAB ACTIVO */}
      <AppMetadata 
        pageTitle={getPageTitle()}
        pageDescription={getPageDescription()}
      />
      
      <div className="flex h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        <div className="flex-1 flex flex-col overflow-hidden">
          <Header />
          <main className="flex-1 overflow-y-auto p-6">
            {renderContent()}
          </main>
        </div>
      </div>
    </>
  );
}

export default App;