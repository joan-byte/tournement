"""
Backup de funciones eliminadas del sistema
Fecha: [fecha actual]
"""

# Backup de ResultadoService
class ResultadoServiceBackup:
    def ajustar_pg(
        self,
        campeonato_id: int,
        pareja_id: int,
        nuevo_pg: int
    ) -> Dict[str, str]:
        # Obtener el último resultado de la pareja
        resultado = self.db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id,
            Resultado.id_pareja == pareja_id
        ).order_by(Resultado.P.desc()).first()

        if not resultado:
            raise HTTPException(
                status_code=404,
                detail="No se encontró el resultado para ajustar"
            )

        resultado.PG = nuevo_pg
        try:
            self.db.commit()
            return {"message": "PG actualizado correctamente"}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def verificar_ultima_partida(
        self,
        campeonato_id: int,
        pareja1_id: int,
        pareja2_id: int
    ) -> Dict[str, Any]:
        # Obtener últimos resultados de ambas parejas
        pareja1 = self.db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id,
            Resultado.id_pareja == pareja1_id
        ).order_by(Resultado.P.desc()).first()

        pareja2 = self.db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id,
            Resultado.id_pareja == pareja2_id
        ).order_by(Resultado.P.desc()).first()

        if not pareja1 or not pareja2:
            return {
                "debe_jugar": True,
                "razon": None
            }

        # Verificar diferencias de PG y PP
        diferencia_pg = pareja1.PG - pareja2.PG
        diferencia_pp = pareja1.PP - pareja2.PP

        debe_jugar = True
        razon = None

        if diferencia_pg > 1:
            debe_jugar = False
            razon = "Diferencia de PG mayor a 1"
        elif diferencia_pg == 1 and diferencia_pp > 300:
            debe_jugar = False
            razon = "Diferencia de PP mayor a 300 con PG=1"

        return {
            "debe_jugar": debe_jugar,
            "razon": razon,
            "diferencia_pg": diferencia_pg,
            "diferencia_pp": diferencia_pp
        }

# Backup de funciones de Parejas.vue
"""
const handleInscripcionButton = async () => {
  try {
    if (!campeonatoActual.value) return

    if (!inscripcionEstado.value) {
      const parejasActivas = parejas.value.filter(p => p.activa)
      if (parejasActivas.length < 4) {
        alert('Se necesitan al menos 4 parejas activas para iniciar el campeonato')
        return
      }

      await mesaStore.sortearMesas(campeonatoActual.value.id)
      inscripcionEstado.value = true
    } else {
      await mesaStore.eliminarMesas(campeonatoActual.value.id)
      inscripcionEstado.value = false
    }
    
    await loadParejas()
  } catch (error) {
    console.error('Error al manejar inscripción:', error)
    alert('Error al realizar el sorteo de mesas')
  }
}

const cerrarInscripcion = () => {
  inscripcionEstado.value = true
}
"""

# Backup de funciones de RegistroResultados.vue
"""
const finalizarCampeonato = async () => {
  try {
    if (!campeonatoActual.value) return
    router.push('/podium')
  } catch (error) {
    console.error('Error al finalizar campeonato:', error)
  }
}
""" 