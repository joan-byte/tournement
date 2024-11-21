<!--
  Home.vue - Página principal de la aplicación
  Muestra una página de bienvenida con tarjetas de navegación a las principales funcionalidades
  del sistema de gestión de torneos de dominó.
-->

<template>
  <!-- Contenedor principal con padding y márgenes responsivos -->
  <div class="py-6">
    <!-- Contenedor con ancho máximo y padding adaptativo según breakpoints -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Título principal de la página -->
      <h1 class="text-3xl font-bold text-gray-900">
        Bienvenido al Torneo de Dominó
      </h1>

      <!-- Grid de tarjetas de navegación - Responsivo: 1 columna en móvil, 2 en tablet, 3 en desktop -->
      <div class="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <!-- Iteración sobre el array de tarjetas -->
        <div
          v-for="(card, index) in cards"
          :key="index"
          class="bg-white overflow-hidden shadow rounded-lg"
        >
          <!-- Contenido principal de la tarjeta -->
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg font-medium text-gray-900">
              {{ card.title }}
            </h3>
            <p class="mt-2 text-sm text-gray-500">
              {{ card.description }}
            </p>
          </div>
          <!-- Pie de la tarjeta con enlace de navegación -->
          <div class="bg-gray-50 px-4 py-4 sm:px-6">
            <router-link
              :to="card.link"
              class="text-sm font-medium text-primary-600 hover:text-primary-500"
            >
              Ver más <span aria-hidden="true">&rarr;</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * Definición de las tarjetas de navegación
 * Cada tarjeta contiene:
 * @property {string} title - Título de la sección
 * @property {string} description - Breve descripción de la funcionalidad
 * @property {string} link - Ruta de navegación
 */
const cards = [
  {
    title: 'Campeonatos',
    description: 'Gestiona los campeonatos activos y crea nuevos torneos.',
    link: '/campeonatos'
  },
  {
    title: 'Parejas',
    description: 'Administra las parejas participantes y sus inscripciones.',
    link: '/parejas'
  },
  {
    title: 'Resultados',
    description: 'Consulta los resultados y clasificaciones de los torneos.',
    link: '/resultados'
  }
]
</script> 