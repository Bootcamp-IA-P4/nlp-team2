import { describe, it, expect } from 'vitest';
import { mockToxicityData } from '../../src/utils/mockData.js';

describe('mockData', () => {
  describe('mockToxicityData', () => {
    it('should have all required top-level properties', () => {
      expect(mockToxicityData).toHaveProperty('overall');
      expect(mockToxicityData).toHaveProperty('toxicityTypes');
      expect(mockToxicityData).toHaveProperty('timelineData');
      expect(mockToxicityData).toHaveProperty('recentAnalysis');
    });

    describe('overall data', () => {
      it('should have correct structure', () => {
        const { overall } = mockToxicityData;
        
        expect(overall).toHaveProperty('totalComments');
        expect(overall).toHaveProperty('toxicComments');
        expect(overall).toHaveProperty('toxicityRate');
        expect(overall).toHaveProperty('videoTitle');
        expect(overall).toHaveProperty('videoId');
      });

      it('should have valid numeric values', () => {
        const { overall } = mockToxicityData;
        
        expect(typeof overall.totalComments).toBe('number');
        expect(typeof overall.toxicComments).toBe('number');
        expect(typeof overall.toxicityRate).toBe('number');
        expect(overall.totalComments).toBeGreaterThan(0);
        expect(overall.toxicComments).toBeGreaterThanOrEqual(0);
        expect(overall.toxicityRate).toBeGreaterThanOrEqual(0);
        expect(overall.toxicityRate).toBeLessThanOrEqual(100);
      });

      it('should have consistent data', () => {
        const { overall } = mockToxicityData;
        
        // La tasa de toxicidad debería coincidir con el cálculo
        const calculatedRate = (overall.toxicComments / overall.totalComments) * 100;
        expect(Math.abs(overall.toxicityRate - calculatedRate)).toBeLessThan(1); // Permitir pequeña diferencia por redondeo
      });
    });

    describe('toxicityTypes data', () => {
      it('should be an array with items', () => {
        const { toxicityTypes } = mockToxicityData;
        
        expect(Array.isArray(toxicityTypes)).toBe(true);
        expect(toxicityTypes.length).toBeGreaterThan(0);
      });

      it('should have correct structure for each item', () => {
        const { toxicityTypes } = mockToxicityData;
        
        toxicityTypes.forEach(type => {
          expect(type).toHaveProperty('name');
          expect(type).toHaveProperty('count');
          expect(type).toHaveProperty('percentage');
          expect(type).toHaveProperty('color');
          
          expect(typeof type.name).toBe('string');
          expect(typeof type.count).toBe('number');
          expect(typeof type.percentage).toBe('number');
          expect(typeof type.color).toBe('string');
          expect(type.color).toMatch(/^#[0-9a-f]{6}$/i); // Verificar formato hexadecimal
        });
      });

      it('should have valid ranges for numeric values', () => {
        const { toxicityTypes } = mockToxicityData;
        
        toxicityTypes.forEach(type => {
          expect(type.count).toBeGreaterThanOrEqual(0);
          expect(type.percentage).toBeGreaterThanOrEqual(0);
          expect(type.percentage).toBeLessThanOrEqual(100);
        });
      });
    });

    describe('timelineData', () => {
      it('should be an array with items', () => {
        const { timelineData } = mockToxicityData;
        
        expect(Array.isArray(timelineData)).toBe(true);
        expect(timelineData.length).toBeGreaterThan(0);
      });

      it('should have correct structure for each item', () => {
        const { timelineData } = mockToxicityData;
        
        timelineData.forEach(item => {
          expect(item).toHaveProperty('time');
          expect(item).toHaveProperty('toxic');
          expect(item).toHaveProperty('clean');
          
          expect(typeof item.time).toBe('string');
          expect(typeof item.toxic).toBe('number');
          expect(typeof item.clean).toBe('number');
        });
      });

      it('should have valid numeric values', () => {
        const { timelineData } = mockToxicityData;
        
        timelineData.forEach(item => {
          expect(item.toxic).toBeGreaterThanOrEqual(0);
          expect(item.clean).toBeGreaterThanOrEqual(0);
        });
      });
    });

    describe('recentAnalysis', () => {
      it('should be an array with items', () => {
        const { recentAnalysis } = mockToxicityData;
        
        expect(Array.isArray(recentAnalysis)).toBe(true);
        expect(recentAnalysis.length).toBeGreaterThan(0);
      });

      it('should have correct structure for each item', () => {
        const { recentAnalysis } = mockToxicityData;
        
        recentAnalysis.forEach(analysis => {
          expect(analysis).toHaveProperty('id');
          expect(analysis).toHaveProperty('videoTitle');
          expect(analysis).toHaveProperty('date');
          expect(analysis).toHaveProperty('toxicityRate');
          
          expect(typeof analysis.id).toBe('number');
          expect(typeof analysis.videoTitle).toBe('string');
          expect(typeof analysis.date).toBe('string');
          expect(typeof analysis.toxicityRate).toBe('number');
        });
      });

      it('should have valid date format', () => {
        const { recentAnalysis } = mockToxicityData;
        
        recentAnalysis.forEach(analysis => {
          // Verificar formato de fecha YYYY-MM-DD
          expect(analysis.date).toMatch(/^\d{4}-\d{2}-\d{2}$/);
          
          // Verificar que es una fecha válida
          const date = new Date(analysis.date);
          expect(date.toString()).not.toBe('Invalid Date');
        });
      });

      it('should have unique IDs', () => {
        const { recentAnalysis } = mockToxicityData;
        
        const ids = recentAnalysis.map(analysis => analysis.id);
        const uniqueIds = [...new Set(ids)];
        
        expect(ids.length).toBe(uniqueIds.length);
      });

      it('should have valid toxicity rates', () => {
        const { recentAnalysis } = mockToxicityData;
        
        recentAnalysis.forEach(analysis => {
          expect(analysis.toxicityRate).toBeGreaterThanOrEqual(0);
          expect(analysis.toxicityRate).toBeLessThanOrEqual(100);
        });
      });
    });
  });
});
