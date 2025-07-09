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

---

_Actualizado: 9 de julio de 2025_
