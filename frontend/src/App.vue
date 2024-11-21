/**
 * @component App.vue
 * @description Componente raíz de la aplicación
 * @responsibilities
 * - Layout principal de la aplicación
 * - Estructura base con navbar y contenido principal
 * - Gestión de rutas a través de router-view
 */
<script setup lang="ts">
// Importación del componente de navegación
import NavBar from '@/components/NavBar.vue'
</script>

<template>
  <!-- Contenedor principal que ocupa toda la altura de la pantalla -->
  <div class="min-h-screen bg-gray-100">
    <!-- Barra de navegación global -->
    <nav-bar />
    
    <!-- Contenido principal de la aplicación -->
    <main class="py-10">
      <!-- Contenedor con ancho máximo y padding responsive -->
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <!-- Router view para renderizar las diferentes vistas -->
        <router-view />
      </div>
    </main>
  </div>
</template>

<style scoped>
/**
 * Estilos para el logo de la aplicación
 * Incluye animaciones y efectos hover
 */
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

/* Efecto hover para el logo general */
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

/* Efecto hover específico para el logo de Vue */
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
