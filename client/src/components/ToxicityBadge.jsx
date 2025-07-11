// client/src/components/ToxicityBadge.jsx
import React from 'react';
import { AlertTriangle, Shield, Zap, Flame } from 'lucide-react';

const ToxicityBadge = ({ categories, severity = 'medio', compact = false }) => {
  const getSeverityIcon = (level) => {
    switch (level) {
      case 'bajo': return <Shield className="h-3 w-3" />;
      case 'medio': return <AlertTriangle className="h-3 w-3" />;
      case 'alto': return <Zap className="h-3 w-3" />;
      case 'crítico': return <Flame className="h-3 w-3" />;
      default: return <AlertTriangle className="h-3 w-3" />;
    }
  };

  const getSeverityColor = (level) => {
    switch (level) {
      case 'bajo': return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800';
      case 'medio': return 'bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-300 border-orange-200 dark:border-orange-800';
      case 'alto': return 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300 border-red-200 dark:border-red-800';
      case 'crítico': return 'bg-red-200 dark:bg-red-900/50 text-red-900 dark:text-red-200 border-red-300 dark:border-red-700';
      default: return 'bg-gray-100 dark:bg-gray-900/30 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-800';
    }
  };

  if (!categories || categories.length === 0) {
    return (
      <span className="px-2 py-1 rounded-full text-xs bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 border border-green-200 dark:border-green-800 flex items-center space-x-1">
        <Shield className="h-3 w-3" />
        <span>Contenido Seguro</span>
      </span>
    );
  }

  if (compact) {
    return (
      <span className={`px-2 py-1 rounded-full text-xs border flex items-center space-x-1 ${getSeverityColor(severity)}`}>
        {getSeverityIcon(severity)}
        <span>{categories.length} categoría(s)</span>
      </span>
    );
  }

  return (
    <div className="flex flex-wrap gap-1">
      {categories.slice(0, 3).map((category, index) => (
        <span 
          key={index}
          className={`px-2 py-1 rounded-full text-xs border flex items-center space-x-1 ${getSeverityColor(category.severity)}`}
          title={`Severidad: ${category.severity}`}
        >
          {getSeverityIcon(category.severity)}
          <span>{category.friendly}</span>
        </span>
      ))}
      {categories.length > 3 && (
        <span className="px-2 py-1 rounded-full text-xs bg-gray-100 dark:bg-gray-900/30 text-gray-600 dark:text-gray-400 border border-gray-200 dark:border-gray-800">
          +{categories.length - 3} más
        </span>
      )}
    </div>
  );
};

export default ToxicityBadge;