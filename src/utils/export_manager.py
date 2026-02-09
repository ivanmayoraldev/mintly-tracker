import csv
from datetime import datetime
from typing import List
from src.models.transaction import Transaction

class ExportManager:
    # Feature [proxima]: Que el usuario pueda meter archivos csv o xlsx contables para que el sistema meta los datos automaticamente
    # Feature [proxima]: Que el usuario mediante los tickets/recibos pueda meter los gatos directamente con un lector de recibos
    @staticmethod
    def export_to_csv(
            transactions: List[Transaction],
            filename: str,
            goals: list = None
    ) -> bool:
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)

                writer.writerow(['FECHA', 'TIPO', 'CATEGORIA', 'MONTO', 'DESCRIPCION'])

                for trans in transactions:
                    if trans.is_income():
                        tipo = 'Ingreso'
                    elif trans.is_savings():
                        tipo = 'Ahorro'
                    else:
                        tipo = 'Gasto'

                    writer.writerow([
                        trans.date,
                        tipo,
                        trans.category,
                        f"{trans.amount:.2f}",
                        trans.description
                    ])

                if goals:
                    writer.writerow([])
                    writer.writerow(['--- METAS DE AHORRO ---'])
                    writer.writerow(['NOMBRE', 'OBJETIVO', 'AHORRADO', 'PROGRESO', 'FECHA LIMITE'])

                    for g in goals:
                        prog = (g.current_amount / g.target_amount * 100) if g.target_amount > 0 else 0
                        writer.writerow([
                            g.name,
                            f"{g.target_amount:.2f}",
                            f"{g.current_amount:.2f}",
                            f"{prog:.1f}%",
                            g.deadline
                        ])

            return True

        except Exception as e:
            print(f"Error exportando CSV: {e}")
            return False

    @staticmethod
    def export_to_pdf(
            transactions: List[Transaction],
            balance: dict,
            filename: str,
            goals: list = None
    ) -> bool:
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.platypus import (
                SimpleDocTemplate, Table, TableStyle,
                Paragraph, Spacer
            )
            from reportlab.lib.styles import getSampleStyleSheet

            doc = SimpleDocTemplate(filename, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()

            title_text = f"Reporte Financiero - {datetime.now().strftime('%d/%m/%Y')}"
            elements.append(Paragraph(title_text, styles['Title']))
            elements.append(Spacer(1, 12))

            data_balance = [
                ['Concepto', 'Monto'],
                ['Ingresos Totales', f"€ {balance['total_income']:,.2f}"],
                ['Gastos Totales', f"€ {balance['total_expense']:,.2f}"],
                ['Ahorro Total', f"€ {balance['total_savings']:,.2f}"],
                ['Balance Neto', f"€ {balance['balance']:,.2f}"]
            ]

            table_balance = Table(data_balance, colWidths=[200, 100])
            table_balance.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))

            elements.append(table_balance)
            elements.append(Spacer(1, 20))

            if goals:
                elements.append(Paragraph("Metas de Ahorro", styles['Heading2']))
                elements.append(Spacer(1, 10))

                data_goals = [['Meta', 'Objetivo', 'Ahorrado', 'Progreso']]
                for g in goals:
                    prog = (g.current_amount / g.target_amount * 100) if g.target_amount > 0 else 0
                    data_goals.append([
                        g.name,
                        f"€{g.target_amount:,.0f}",
                        f"€{g.current_amount:,.0f}",
                        f"{prog:.1f}%"
                    ])

                table_goals = Table(data_goals, colWidths=[150, 100, 100, 50])
                table_goals.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B5CF6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                ]))

                elements.append(table_goals)
                elements.append(Spacer(1, 20))

            if transactions:
                elements.append(Paragraph("Transacciones Recientes", styles['Heading2']))
                elements.append(Spacer(1, 10))

                data_trans = [['Fecha', 'Tipo', 'Categoría', 'Monto']]
                for trans in transactions[:20]:
                    if trans.is_income():
                        tipo = 'Ingreso'
                    elif trans.is_savings():
                        tipo = 'Ahorro'
                    else:
                        tipo = 'Gasto'

                    data_trans.append([
                        trans.date,
                        tipo,
                        trans.category,
                        f"€ {trans.amount:.2f}"
                    ])

                table_trans = Table(data_trans, colWidths=[80, 80, 150, 80])
                table_trans.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#334155')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1),
                     [colors.white, colors.HexColor('#F8FAFC')])
                ]))

                elements.append(table_trans)

            doc.build(elements)
            return True

        except ImportError:
            print("ReportLab no instalado. Instala con: pip install reportlab")
            return False
        except Exception as e:
            print(f"Error exportando PDF: {e}")
            import traceback
            traceback.print_exc()
            return False