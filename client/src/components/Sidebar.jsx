import { BarChart3, History, BookOpen, Shield, PieChart } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: PieChart },
    { id: 'analyze', label: 'Analizar', icon: BarChart3 },
    { id: 'history', label: 'Historial', icon: History },
    { id: 'guide', label: 'Guía', icon: BookOpen }
  ];

  const handleLogoClick = () => {
    setActiveTab('dashboard');
  };

  return (
    <div className="w-64 bg-primary-500 dark:bg-gray-900 shadow-lg border-r border-primary-600 dark:border-gray-700 transition-colors duration-300">
      {/* Logo */}
      <div className="p-6 border-b border-primary-600 dark:border-gray-700">
        <div 
          className="flex items-center cursor-pointer hover:opacity-80 transition-opacity"
          onClick={handleLogoClick}
        >
          <img 
            src="/img/logoFull.png" 
            alt="Modzilla Logo" 
            className="h-28 w-auto object-contain center mx-auto"
          />
        </div>
      </div>

      {/* Navigation */}
      <nav className="mt-6">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          
          return (
            <div
              key={item.id}
              className={`
                flex items-center px-4 py-3 cursor-pointer transition-colors duration-200
                ${isActive 
                  ? 'bg-accent-500 dark:bg-accent-600 text-white border-r-4 border-accent-300 dark:border-accent-400' 
                  : 'text-primary-100 dark:text-gray-300 hover:bg-primary-400 dark:hover:bg-gray-700 hover:text-white'
                }
              `}
              onClick={() => setActiveTab(item.id)}
            >
              <Icon className="h-5 w-5 mr-3" />
              <span className="font-medium">{item.label}</span>
            </div>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="absolute bottom-0 w-64 p-4 border-t border-primary-600 dark:border-gray-700">
        <div className="text-xs text-primary-200 dark:text-gray-400">
          <p>© 2025 Modzilla</p>
          <p>Proyecto con carácter educativo</p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;