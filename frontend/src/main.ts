/**
 * @file main.ts
 * @description Punto de entrada principal de la aplicación Vue
 * @responsibilities
 * - Inicialización de la aplicación Vue
 * - Configuración de plugins (Pinia, Router)
 * - Montaje de la aplicación en el DOM
 */

// Importación de la función createApp de Vue
import { createApp } from 'vue'

// Importación del store manager Pinia
import { createPinia } from 'pinia'

// Importación del componente raíz
import App from './App.vue'

// Importación del router configurado
import router from '@/router'

// Importación de estilos globales
import './assets/main.css'

// Creación de la instancia de la aplicación Vue
const app = createApp(App)

// Instalación de Pinia para la gestión del estado global
app.use(createPinia())

// Instalación del router para la navegación
app.use(router)

// Montaje de la aplicación en el elemento con id 'app'
app.mount('#app')
