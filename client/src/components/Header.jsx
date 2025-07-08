import { Bell, Search, Sun, Moon } from "lucide-react";
import { useTheme } from "../contexts/ThemeContext";

const Header = () => {
  const { isDark, toggleTheme } = useTheme();

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-cream-200 dark:border-gray-700 px-6 py-4 transition-colors duration-300">
      <div className="flex items-center justify-between">
        <div className="flex items-center flex-1 max-w-lg">
          <div className="relative w-full">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-navy-400 dark:text-cream-500 h-4 w-4" />
            <input
              type="text"
              placeholder="Buscar análisis..."
              className="input-primary w-full pl-10 pr-4 py-2"
            />
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {/* Toggle de tema */}
          <button
            onClick={toggleTheme}
            className="p-2 text-navy-500 hover:text-navy-700 dark:text-cream-300 dark:hover:text-cream-100 
                       hover:bg-cream-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            {isDark ? (
              <Sun className="h-5 w-5" />
            ) : (
              <Moon className="h-5 w-5" />
            )}
          </button>

          <button className="relative p-2 text-navy-500 hover:text-navy-700 dark:text-cream-300 dark:hover:text-cream-100">
            <Bell className="h-5 w-5" />
            <span className="absolute top-0 right-0 h-2 w-2 bg-wine-500 rounded-full"></span>
          </button>

          <div className="flex items-center space-x-3">
            <div className="text-right">
              <p className="text-sm font-medium text-navy-800 dark:text-cream-100">
                Admin Godzilla
              </p>
              <p className="text-xs text-navy-500 dark:text-cream-400">
                Moderador
              </p>
            </div>
            <div className="h-12 w-12 rounded-full overflow-hidden border-2 border-accent-500 dark:border-accent-400 shadow-md hover:shadow-lg hover:border-accent-600 dark:hover:border-accent-300 transition-all duration-300 cursor-pointer">
              <img
                src="../public/img/iconGojira.png"
                alt="Admin Avatar"
                className="h-full w-full object-cover object-center hover:scale-110 transition-transform duration-300"
              />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
