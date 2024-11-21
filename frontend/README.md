# Sistema de Gestión de Torneos de Dominó

## Descripción
Aplicación web para la gestión integral de torneos de dominó desarrollada con Vue 3, TypeScript y Vite. Permite administrar campeonatos, parejas participantes, resultados y clasificaciones.

## Tecnologías Principales
- Vue 3 con Composition API
- TypeScript
- Vite
- Tailwind CSS
- Vue Router
- Pinia (State Management)

## Características Principales
- Gestión de campeonatos
- Registro y administración de parejas
- Sorteo automático de mesas
- Registro de resultados por partida
- Clasificación en tiempo real
- Sistema de puntuación configurable
- Soporte para grupos A/B

## Requisitos Previos
- Node.js (v14 o superior)
- npm o yarn
- Git

## Instalación

```bash
# Clonar el repositorio
git clone [url-del-repositorio]

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build
```

## Estructura del Proyecto
```
frontend/
├── src/
│   ├── components/     # Componentes reutilizables
│   ├── views/          # Vistas principales
│   ├── stores/         # Stores de Pinia
│   ├── router/         # Configuración de rutas
│   ├── types/          # Definiciones de TypeScript
│   └── assets/         # Recursos estáticos
```

## Convenciones de Código
- Componentes Vue usando Composition API con `<script setup>`
- TypeScript para tipo seguro
- Nombres de componentes en PascalCase
- Props y eventos documentados con JSDoc
- Estilos con Tailwind CSS

## Scripts Disponibles
- `npm run dev`: Inicia servidor de desarrollo
- `npm run build`: Compila para producción
- `npm run preview`: Vista previa de producción
- `npm run lint`: Ejecuta el linter
- `npm run type-check`: Verifica tipos TypeScript

## Documentación Adicional
- [Documentación de Vue 3](https://v3.vuejs.org/)
- [Guía TypeScript de Vue](https://vuejs.org/guide/typescript/overview.html)
- [Documentación de Vite](https://vitejs.dev/)

## Contribución
1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit cambios (`git commit -m 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Crear Pull Request

## Licencia
[MIT](LICENSE)
