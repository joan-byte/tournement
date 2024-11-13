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
    def __init__(self, db: Session):
        self.db = db

    def exportar_ranking_excel(self, campeonato_id: int) -> Tuple[BinaryIO, str]:
        try:
            # Obtener datos del ranking
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

            # Crear DataFrame
            df = pd.DataFrame(ranking)
            
            # Crear archivo Excel en memoria
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Ranking')
            
            output.seek(0)
            return output, f"ranking_{campeonato_id}.xlsx"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def exportar_ranking_pdf(self, campeonato_id: int) -> Tuple[BinaryIO, str]:
        try:
            # Obtener datos del ranking
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

            # Crear buffer para PDF
            buffer = BytesIO()
            
            # Crear documento PDF
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            # Convertir datos a formato de tabla
            data = [['Pareja', 'Club', 'PG', 'PP', 'Grupo']]
            for r in ranking:
                data.append([
                    r.nombre_pareja,
                    r.club or '',
                    str(r.PG),
                    str(r.PP),
                    r.GB
                ])

            # Crear tabla
            t = Table(data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
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
        try:
            # Obtener todos los resultados
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

            # Crear DataFrame
            df = pd.DataFrame(resultados)
            
            # Crear archivo Excel en memoria
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Resultados')
            
            output.seek(0)
            return output, f"resultados_{campeonato_id}.xlsx"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def exportar_resultados_pdf(self, campeonato_id: int) -> Tuple[BinaryIO, str]:
        try:
            # Obtener todos los resultados
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

            # Crear buffer para PDF
            buffer = BytesIO()
            
            # Crear documento PDF
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            # Convertir datos a formato de tabla
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

            # Crear tabla
            t = Table(data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
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