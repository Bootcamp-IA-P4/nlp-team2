import { BarChart3, History, BookOpen, Shield } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'analyze', label: 'Analizar', icon: BarChart3 },
    { id: 'history', label: 'Historial', icon: History },
    { id: 'guide', label: 'Guía', icon: BookOpen }
  ];

  return (
    <div className="w-64 bg-white shadow-lg border-r border-gray-200">
      {/* Logo */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center">
          <Shield className="h-8 w-8 text-blue-600" />
          <h1 className="ml-3 text-xl font-bold text-gray-800">Modzilla</h1>
        </div>
        <p className="text-sm text-gray-500 mt-1">Monitor de Toxicidad</p>
      </div>

      {/* Navigation */}
      <nav className="mt-6">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <div
              key={item.id}
              className={`sidebar-item ${activeTab === item.id ? 'active' : ''}`}
              onClick={() => setActiveTab(item.id)}
            >
              <Icon className="h-5 w-5 mr-3" />
              <span className="font-medium">{item.label}</span>
            </div>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="absolute bottom-0 w-64 p-4 border-t border-gray-200">
        <div className="text-xs text-gray-500">
          <p>© 2024 Modzilla</p>
          <p>NLP Team 2</p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;