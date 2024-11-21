from sqlalchemy.orm import Session
from fastapi import HTTPException
import pandas as pd
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from app.models.resultado import Resultado
from app.models.pareja import Pareja
from typing import Tuple, BinaryIO

class ExportacionService:
    """
    Servicio que maneja la exportación de datos del campeonato a diferentes formatos.
    Proporciona funcionalidades para exportar rankings y resultados a Excel y PDF.
    """

    def __init__(self, db: Session):
        """
        Constructor del servicio de exportación.
        
        Args:
            db: Sesión de SQLAlchemy para interactuar con la base de datos
        """
        self.db = db

    def exportar_ranking_excel(self, campeonato_id: int) -> Tuple[BinaryIO, str]:
        """
        Exporta el ranking del campeonato a un archivo Excel.
        
        Args:
            campeonato_id: ID del campeonato a exportar
        
        Returns:
            Tuple[BinaryIO, str]: Buffer con el archivo Excel y nombre sugerido
            
        Raises:
            HTTPException: Si hay error en la exportación
            
        Note:
            El archivo Excel incluye: ID pareja, nombre, club, PG, PP y GB
        """
        try:
            # Consulta SQL para obtener los datos del ranking
            ranking = self.db.query(
                Resultado.id_pareja,
                Pareja.nombre.label('nombre_pareja'),
                Pareja.club,
                Resultado.PG.label('PG'),
                Resultado.PP.label('PP'),
                Resultado.GB.label('GB')
            ).join(
                Pareja,
                Resultado.id_pareja == Pareja.id
            ).filter(
                Resultado.campeonato_id == campeonato_id
            ).all()

            # Crear DataFrame de pandas con los resultados
            df = pd.DataFrame(ranking)
            
            # Generar archivo Excel en memoria
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Ranking')
            
            output.seek(0)
            return output, f"ranking_{campeonato_id}.xlsx"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def exportar_ranking_pdf(self, campeonato_id: int) -> Tuple[BinaryIO, str]:
        """
        Exporta el ranking del campeonato a un archivo PDF.
        
        Args:
            campeonato_id: ID del campeonato a exportar
        
        Returns:
            Tuple[BinaryIO, str]: Buffer con el archivo PDF y nombre sugerido
            
        Raises:
            HTTPException: Si hay error en la exportación
            
        Note:
            El PDF incluye una tabla formateada con estilos profesionales
        """
        try:
            # Consulta SQL para obtener los datos del ranking
            ranking = self.db.query(
                Resultado.id_pareja,
                Pareja.nombre.label('nombre_pareja'),
                Pareja.club,
                Resultado.PG.label('PG'),
                Resultado.PP.label('PP'),
                Resultado.GB.label('GB')
            ).join(
                Pareja,
                Resultado.id_pareja == Pareja.id
            ).filter(
                Resultado.campeonato_id == campeonato_id
            ).all()

            # Crear buffer para el PDF en memoria
            buffer = BytesIO()
            
            # Configurar documento PDF
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            # Preparar datos para la tabla
            data = [['Pareja', 'Club', 'PG', 'PP', 'Grupo']]  # Encabezados
            for r in ranking:
                data.append([
                    r.nombre_pareja,
                    r.club or '',
                    str(r.PG),
                    str(r.PP),
                    r.GB
                ])

            # Crear y estilizar la tabla
            t = Table(data)
            t.setStyle(TableStyle([
                # Estilo del encabezado
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                # Estilo del contenido
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(t)
            doc.build(elements)
            
            buffer.seek(0)
            return buffer, f"ranking_{campeonato_id}.pdf"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def exportar_resultados_excel(self, campeonato_id: int) -> Tuple[BinaryIO, str]:
        """
        Exporta los resultados detallados del campeonato a Excel.
        
        Args:
            campeonato_id: ID del campeonato a exportar
        
        Returns:
            Tuple[BinaryIO, str]: Buffer con el archivo Excel y nombre sugerido
            
        Raises:
            HTTPException: Si hay error en la exportación
            
        Note:
            Incluye: Partida, Mesa, Pareja, RP, PG, PP y GB
        """
        try:
            # Consulta SQL para obtener todos los resultados
            resultados = self.db.query(
                Resultado.P.label('Partida'),
                Resultado.M.label('Mesa'),
                Pareja.nombre.label('Pareja'),
                Resultado.RP.label('RP'),
                Resultado.PG.label('PG'),
                Resultado.PP.label('PP'),
                Resultado.GB.label('GB')
            ).join(
                Pareja,
                Resultado.id_pareja == Pareja.id
            ).filter(
                Resultado.campeonato_id == campeonato_id
            ).order_by(
                Resultado.P,
                Resultado.M
            ).all()

            # Crear DataFrame y exportar a Excel
            df = pd.DataFrame(resultados)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Resultados')
            
            output.seek(0)
            return output, f"resultados_{campeonato_id}.xlsx"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def exportar_resultados_pdf(self, campeonato_id: int) -> Tuple[BinaryIO, str]:
        """
        Exporta los resultados detallados del campeonato a PDF.
        
        Args:
            campeonato_id: ID del campeonato a exportar
        
        Returns:
            Tuple[BinaryIO, str]: Buffer con el archivo PDF y nombre sugerido
            
        Raises:
            HTTPException: Si hay error en la exportación
            
        Note:
            Genera un PDF con tabla formateada de todos los resultados
        """
        try:
            # Consulta SQL para obtener todos los resultados
            resultados = self.db.query(
                Resultado.P.label('Partida'),
                Resultado.M.label('Mesa'),
                Pareja.nombre.label('Pareja'),
                Resultado.RP.label('RP'),
                Resultado.PG.label('PG'),
                Resultado.PP.label('PP'),
                Resultado.GB.label('GB')
            ).join(
                Pareja,
                Resultado.id_pareja == Pareja.id
            ).filter(
                Resultado.campeonato_id == campeonato_id
            ).order_by(
                Resultado.P,
                Resultado.M
            ).all()

            # Crear buffer y documento PDF
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            # Preparar datos para la tabla
            data = [['Partida', 'Mesa', 'Pareja', 'RP', 'PG', 'PP', 'Grupo']]
            for r in resultados:
                data.append([
                    str(r.Partida),
                    str(r.Mesa),
                    r.Pareja,
                    str(r.RP),
                    str(r.PG),
                    str(r.PP),
                    r.GB
                ])

            # Crear y estilizar la tabla
            t = Table(data)
            t.setStyle(TableStyle([
                # Estilo del encabezado
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                # Estilo del contenido
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(t)
            doc.build(elements)
            
            buffer.seek(0)
            return buffer, f"resultados_{campeonato_id}.pdf"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 