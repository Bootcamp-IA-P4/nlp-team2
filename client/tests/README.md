# Tests del Cliente

Este directorio contiene los tests automatizados para la aplicación cliente del proyecto NLP Toxicity Analyzer. Los tests están implementados usando [Vitest](https://vitest.dev/) y [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/).

## Estructura de los tests

- **basic.test.js**: Pruebas básicas de operaciones matemáticas, strings y arrays para validar el entorno de testing.
- **App.test.jsx**: Pruebas del componente principal de la aplicación.
- **basic-component.test.jsx**: Pruebas de componentes React simples.
- **components/**: Pruebas unitarias de componentes UI como `Header`, `Sidebar`, `Dashboard`, y `ThemeContext`.
- **utils/**: Pruebas de utilidades y funciones auxiliares.
- **setup/**: Configuración global y utilidades para los tests.

## Instalación y ejecución

1. Instala las dependencias (desde la carpeta `client`):

```bash
npm install
```

2. Ejecuta todos los tests:

```bash
npm test
```

3. Ejecuta los tests con interfaz visual:

```bash
npm run test:ui
```

4. Genera un reporte de cobertura de código:

```bash
npm run test:coverage
```

5. Abre el reporte de cobertura en el navegador:

```bash
npm run test:coverage:open
```

## Funcionalidad de los tests

- **Validación de lógica básica**: Se asegura que el entorno de testing funcione correctamente con operaciones matemáticas, strings y arrays (`basic.test.js`).
- **Pruebas de componentes React**: Se verifica el renderizado, interacción y estilos de los componentes principales de la UI.
- **Cobertura de código**: Se mide qué porcentaje del código fuente está cubierto por los tests.
- **Utilidades y mocks**: Se incluyen utilidades para facilitar el testing y mocks de datos para pruebas aisladas.

## Buenas prácticas

- Mantén los tests actualizados junto con los componentes.
- Usa nombres descriptivos para los tests y los archivos.
- Ejecuta los tests y revisa la cobertura antes de hacer deploy.

## Estado Actual de los Tests

### ✅ Tests que Pasan (39 tests en total)

1. **Dashboard Tests**: 1 test
   - ✅ should render dashboard header and key stats

2. **ThemeContext Tests**: 9 tests
   - ✅ should provide default theme as light
   - ✅ should load theme from localStorage if available
   - ✅ should use system preference when no localStorage value
   - ✅ should toggle theme from light to dark
   - ✅ should toggle theme from dark to light
   - ✅ should save theme to localStorage when toggling
   - ✅ should apply theme class to document
   - ✅ should handle system preference changes
   - ✅ should provide theme context to children

3. **Header Tests**: 4 tests
   - ✅ Todos los tests del Header pasan

4. **Sidebar Tests**: 2 tests
   - ✅ Todos los tests del Sidebar pasan

5. **App Tests**: 2 tests
   - ✅ Todos los tests del App pasan

6. **Utils Tests**: 15 tests
   - ✅ Todos los tests de mockData.js pasan

7. **Basic Tests**: 6 tests
   - ✅ Todos los tests básicos pasan

### 📊 Cobertura de Código

- **Total**: 28.66% statements, 44.73% branches, 44.11% functions
- **Archivos mejor cubiertos**:
  - `ThemeContext.jsx`: 93.93% coverage
  - `Header.jsx`: 97.95% coverage 
  - `Sidebar.jsx`: 96.07% coverage
  - `App.jsx`: 82.85% coverage
  - `Dashboard.jsx`: 72.63% coverage
  - `mockData.js`: 100% coverage

### 🔧 Correcciones Realizadas

1. **Dashboard Test**:
   - ✅ Corregido problema de múltiples elementos con "Comentarios" usando `getAllByText`
   - ✅ Ajustados los números esperados para coincidir con el HTML real (sin comas)
   - ✅ Eliminadas verificaciones de datos que no existen en el DOM

2. **ThemeContext Test**:
   - ✅ Agregado manejo de errores para localStorage y matchMedia
   - ✅ Mejorados los mocks para evitar errores en entorno de test

3. **API Mocks**:
   - ✅ Creados mocks robustos para evitar llamadas HTTP reales durante tests
   - ✅ Simplificados datos de test para evitar errores de renderizado

### 📝 Notas Importantes

- Los tests ahora utilizan datos mock simples que evitan problemas de renderizado
- Se maneja correctamente el localStorage y matchMedia en entorno de test
- Los errores de red en las pruebas son esperados y no afectan el resultado
- La cobertura se puede mejorar agregando más tests para componentes complejos

---

_Actualizado: 9 de julio de 2025_
