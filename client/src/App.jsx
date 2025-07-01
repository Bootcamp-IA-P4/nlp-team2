import { useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import AnalyzeTab from './components/AnalyzeTab';
import HistoryTab from './components/HistoryTab';
import GuideTab from './components/GuideTab';

function App() {
  const [activeTab, setActiveTab] = useState('analyze');

  const renderContent = () => {
    switch (activeTab) {
      case 'analyze':
        return <AnalyzeTab />;
      case 'history':
        return <HistoryTab />;
      case 'guide':
        return <GuideTab />;
      default:
        return <AnalyzeTab />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}

export default App;