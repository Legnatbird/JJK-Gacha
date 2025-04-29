def calculate_multis_banner(initial_points):
    """
    ¿Cuántas multis necesitas para conseguir un personaje en el banner?
    1 multis = 10 tiradas
    1 multis = 3000 cubos
    Probabilidad del personaje = 0.7% por multi
    """

    # Puntos iniciales usables (máximo 100 por banner)
    multis_needed = 24  # De 25 a 24 porque el juego regala 1 multi
    usable_points = min(initial_points, 100)

    # Multis que te ahorras por los puntos iniciales
    saved_multis = usable_points // 10

    # Multis necesarios para conseguir el personaje deseado
    pity_multis = multis_needed - saved_multis

    # Probabilidad de obtener el personaje en cada multi es 0.7%
    prob_per_multi = 0.007  # 0.7% por multi

    return pity_multis, usable_points, prob_per_multi


def main():
    cubes = int(input("¿Cuántos cubos tienes? "))
    initial_points = int(input("¿Cuántos puntos gacha tienes inicialmente? "))
    desired = int(input("¿Cuántos personajes quieres asegurar? "))

    possible_multis = cubes // 3000
    print(f"Puedes hacer {possible_multis} multis.")

    remaining_points = initial_points
    remaining_cubes = cubes

    # Para guardar información para el reporte
    report_data = {
        "cubos_iniciales": cubes,
        "puntos_iniciales": initial_points,
        "personajes_deseados": desired,
        "personajes_info": []
    }

    for i in range(desired):
        print(f"\n--- Personaje {i + 1} ---")
        
        # Diccionario para almacenar datos de este personaje
        personaje_info = {"numero": i+1}

        # Calcular multis necesarias y probabilidad
        multis_needed, used_points, prob_per_multi = calculate_multis_banner(
            remaining_points
        )
        
        personaje_info["multis_needed"] = multis_needed
        personaje_info["prob_per_multi"] = prob_per_multi
        personaje_info["used_points"] = used_points

        # Probabilidad de obtener el personaje antes o en el pity
        prob_before_pity = 1 - (1 - prob_per_multi) ** multis_needed
        personaje_info["prob_before_pity"] = prob_before_pity

        print(f"Multis necesarias para garantizar (pity): {multis_needed}")
        print(f"Probabilidad por multi: {prob_per_multi * 100:.2f}%")
        print(
            f"Probabilidad de obtener antes o en el pity: {prob_before_pity * 100:.2f}%"
        )

        # Verificar si tiene suficientes cubos
        if (multis_needed * 3000) > remaining_cubes:
            available_multis = remaining_cubes // 3000
            prob_with_available = 1 - (1 - prob_per_multi) ** available_multis
            
            personaje_info["can_guarantee"] = False
            personaje_info["available_multis"] = available_multis
            personaje_info["prob_with_available"] = prob_with_available
            personaje_info["missing_cubes"] = multis_needed * 3000 - remaining_cubes
            
            print("No puedes asegurar este personaje (pity) con los cubos actuales.")
            print(
                f"Con tus {available_multis} multis disponibles, tienes {prob_with_available * 100:.2f}% de probabilidad."
            )
            
            # Si no es el primer personaje, considerar escenarios optimistas del personaje anterior
            if i > 0:
                escenarios_previos = []
                print("\n--- Escenarios optimistas teniendo en cuenta que te salga con los escenarios anteriores ---")
                
                # Calcular ahorros potenciales del personaje anterior
                prev_multis_needed, _, _ = calculate_multis_banner(
                    initial_points if i == 1 else 0  # Para el primer personaje, usar puntos iniciales
                )
                
                # Definir escenarios de suerte para el personaje anterior
                half_prev = max(1, prev_multis_needed // 2)
                quarter_prev = max(1, prev_multis_needed // 4)
                first_5_prev = min(5, prev_multis_needed)
                
                # Calcular ahorros para cada escenario
                saving_half = (prev_multis_needed - half_prev) * 3000
                saving_quarter = (prev_multis_needed - quarter_prev) * 3000
                saving_first_5 = (prev_multis_needed - first_5_prev) * 3000
                
                # Calcular nuevos cubos disponibles en cada escenario
                new_cubes_half = remaining_cubes + saving_half
                new_cubes_quarter = remaining_cubes + saving_quarter
                new_cubes_first_5 = remaining_cubes + saving_first_5
                
                # Probabilidades de cada escenario para el personaje anterior
                prob_half_prev = 1 - (1 - prob_per_multi) ** half_prev
                prob_quarter_prev = 1 - (1 - prob_per_multi) ** quarter_prev
                prob_first_5_prev = 1 - (1 - prob_per_multi) ** first_5_prev
                
                # Verificar si algún escenario permite asegurar el personaje actual
                print("Si el personaje anterior saliera antes:")
                
                # Escenario 1: Mitad de multis
                can_guarantee_half = new_cubes_half >= multis_needed * 3000
                new_available_half = new_cubes_half // 3000
                new_prob_half = 1 - (1 - prob_per_multi) ** min(new_available_half, multis_needed)
                
                escenario1 = {
                    "tipo": "mitad",
                    "multis": half_prev,
                    "ahorro": saving_half,
                    "nuevos_cubos": new_cubes_half,
                    "probabilidad": prob_half_prev,
                    "puede_garantizar": can_guarantee_half,
                    "multis_disponibles": new_available_half,
                    "nueva_probabilidad": new_prob_half
                }
                escenarios_previos.append(escenario1)
                
                print(f"\nEscenario 1 (Probabilidad {prob_half_prev*100:.2f}%):")
                print(f"Si el personaje anterior sale en {half_prev} multis, ahorrarías {saving_half} cubos")
                if can_guarantee_half:
                    print(f"→ ¡Podrías garantizar este personaje con {new_cubes_half} cubos!")
                    print(f"  Te sobrarían {new_cubes_half - multis_needed * 3000} cubos")
                else:
                    print(f"→ Aún no podrías garantizarlo, pero tendrías {new_cubes_half} cubos")
                    print(f"  Con {new_available_half} multis, tendrías {new_prob_half*100:.2f}% de probabilidad")
                
                # Escenario 2: Cuarto de multis
                can_guarantee_quarter = new_cubes_quarter >= multis_needed * 3000
                new_available_quarter = new_cubes_quarter // 3000
                new_prob_quarter = 1 - (1 - prob_per_multi) ** min(new_available_quarter, multis_needed)
                
                escenario2 = {
                    "tipo": "cuarto",
                    "multis": quarter_prev,
                    "ahorro": saving_quarter,
                    "nuevos_cubos": new_cubes_quarter,
                    "probabilidad": prob_quarter_prev,
                    "puede_garantizar": can_guarantee_quarter,
                    "multis_disponibles": new_available_quarter,
                    "nueva_probabilidad": new_prob_quarter
                }
                escenarios_previos.append(escenario2)
                
                print(f"\nEscenario 2 (Probabilidad {prob_quarter_prev*100:.2f}%):")
                print(f"Si el personaje anterior sale en {quarter_prev} multis, ahorrarías {saving_quarter} cubos")
                if can_guarantee_quarter:
                    print(f"→ ¡Podrías garantizar este personaje con {new_cubes_quarter} cubos!")
                    print(f"  Te sobrarían {new_cubes_quarter - multis_needed * 3000} cubos")
                else:
                    print(f"→ Aún no podrías garantizarlo, pero tendrías {new_cubes_quarter} cubos")
                    print(f"  Con {new_available_quarter} multis, tendrías {new_prob_quarter*100:.2f}% de probabilidad")
                
                # Escenario 3: Primeras 5 multis
                can_guarantee_first_5 = new_cubes_first_5 >= multis_needed * 3000
                new_available_first_5 = new_cubes_first_5 // 3000
                new_prob_first_5 = 1 - (1 - prob_per_multi) ** min(new_available_first_5, multis_needed)
                
                escenario3 = {
                    "tipo": "primeras_5",
                    "multis": first_5_prev,
                    "ahorro": saving_first_5,
                    "nuevos_cubos": new_cubes_first_5,
                    "probabilidad": prob_first_5_prev,
                    "puede_garantizar": can_guarantee_first_5,
                    "multis_disponibles": new_available_first_5,
                    "nueva_probabilidad": new_prob_first_5
                }
                escenarios_previos.append(escenario3)
                
                personaje_info["escenarios_previos"] = escenarios_previos
                
                print(f"\nEscenario 3 (Probabilidad {prob_first_5_prev*100:.2f}%):")
                print(f"Si el personaje anterior sale en {first_5_prev} multis, ahorrarías {saving_first_5} cubos")
                if can_guarantee_first_5:
                    print(f"→ ¡Podrías garantizar este personaje con {new_cubes_first_5} cubos!")
                    print(f"  Te sobrarían {new_cubes_first_5 - multis_needed * 3000} cubos")
                else:
                    print(f"→ Aún no podrías garantizarlo, pero tendrías {new_cubes_first_5} cubos")
                    print(f"  Con {new_available_first_5} multis, tendrías {new_prob_first_5*100:.2f}% de probabilidad")
            
            print(f"\nNecesitarías {multis_needed * 3000 - remaining_cubes} cubos adicionales para garantizarlo.")
            
            report_data["personajes_info"].append(personaje_info)
            break

        # Sección optimista: probabilidades de obtener el personaje antes del pity
        print("\n--- Escenario Optimista ---")
        
        # Calcular probabilidades para diferentes escenarios de suerte
        half_multis = max(1, multis_needed // 2)
        quarter_multis = max(1, multis_needed // 4)
        first_5_multis = min(5, multis_needed)
        
        prob_half = 1 - (1 - prob_per_multi) ** half_multis
        prob_quarter = 1 - (1 - prob_per_multi) ** quarter_multis
        prob_first_5 = 1 - (1 - prob_per_multi) ** first_5_multis
        
        # Guardar escenarios optimistas
        escenarios_optimistas = [
            {
                "tipo": "mitad",
                "multis": half_multis,
                "probabilidad": prob_half,
                "ahorro": (multis_needed - half_multis) * 3000
            },
            {
                "tipo": "cuarto",
                "multis": quarter_multis,
                "probabilidad": prob_quarter,
                "ahorro": (multis_needed - quarter_multis) * 3000
            },
            {
                "tipo": "primeras_5",
                "multis": first_5_multis,
                "probabilidad": prob_first_5,
                "ahorro": (multis_needed - first_5_multis) * 3000
            }
        ]
        personaje_info["escenarios_optimistas"] = escenarios_optimistas
        personaje_info["can_guarantee"] = True
        personaje_info["remaining_cubes_after"] = remaining_cubes - multis_needed * 3000
        personaje_info["remaining_points_after"] = remaining_points - used_points
        
        print(f"Tienes {prob_half * 100:.2f}% de probabilidad de conseguirlo en solo {half_multis} multis ({half_multis * 3000} cubos)")
        print(f"Tienes {prob_quarter * 100:.2f}% de probabilidad de conseguirlo en solo {quarter_multis} multis ({quarter_multis * 3000} cubos)")
        print(f"Tienes {prob_first_5 * 100:.2f}% de probabilidad de conseguirlo en las primeras {first_5_multis} multis ({first_5_multis * 3000} cubos)")
        
        # Calcular el ahorro potencial en cada escenario
        saving_half = (multis_needed - half_multis) * 3000
        saving_quarter = (multis_needed - quarter_multis) * 3000
        saving_first_5 = (multis_needed - first_5_multis) * 3000
        
        print("\nPosibles ahorros:")
        print(f"Si sale en {half_multis} multis: ahorrarías {saving_half} cubos")
        print(f"Si sale en {quarter_multis} multis: ahorrarías {saving_quarter} cubos")
        print(f"Si sale en {first_5_multis} multis: ahorrarías {saving_first_5} cubos")

        # Actualizar recursos restantes
        remaining_cubes -= multis_needed * 3000
        remaining_points -= used_points

        print(f"\nTe quedan {remaining_cubes} cubos y {remaining_points} puntos gacha.")
        
        report_data["personajes_info"].append(personaje_info)

    # Generar reporte PDF con toda la información
    generate_pdf_report(report_data)
    print("\nSe ha generado un reporte PDF con todos los detalles.")


def generate_pdf_report(data):
    """Genera un reporte PDF con toda la información calculada"""
    try:
        # Importar bibliotecas necesarias para PDF
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        import os
        from datetime import datetime
        
        # Crear directorio de reportes si no existe
        report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reportes")
        os.makedirs(report_dir, exist_ok=True)
        
        # Nombre del archivo con fecha y hora
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(report_dir, f"reporte_gacha_{now}.pdf")
        
        # Crear documento
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72, leftMargin=72,
            topMargin=72, bottomMargin=18
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CenteredTitle',
            parent=styles['Heading1'],
            alignment=1,  # 0=left, 1=center, 2=right
            spaceAfter=20
        ))
        styles.add(ParagraphStyle(
            name='Subtitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=10
        ))
        
        # Contenido del documento
        content = []
        
        # Título
        content.append(Paragraph("Reporte de Análisis Gacha", styles['CenteredTitle']))
        content.append(Spacer(1, 0.25 * inch))
        
        # Información general
        content.append(Paragraph("Información General", styles['Subtitle']))
        general_info = [
            ["Cubos Iniciales:", f"{data['cubos_iniciales']}"],
            ["Puntos Gacha Iniciales:", f"{data['puntos_iniciales']}"],
            ["Personajes Deseados:", f"{data['personajes_deseados']}"],
            ["Multis Posibles:", f"{data['cubos_iniciales'] // 3000}"]
        ]
        
        general_table = Table(general_info, colWidths=[3*inch, 2*inch])
        general_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))
        content.append(general_table)
        content.append(Spacer(1, 0.25 * inch))
        
        # Información de cada personaje
        for personaje in data["personajes_info"]:
            num = personaje["numero"]
            content.append(Paragraph(f"Personaje {num}", styles['Subtitle']))
            
            # Información básica
            personaje_info = [
                ["Multis para Garantizar (Pity):", f"{personaje['multis_needed']}"],
                ["Probabilidad por Multi:", f"{personaje['prob_per_multi'] * 100:.2f}%"],
                ["Probabilidad hasta Pity:", f"{personaje['prob_before_pity'] * 100:.2f}%"],
            ]
            
            # Si puede garantizar el personaje
            if personaje.get("can_guarantee", False):
                personaje_info.append(["Cubos Restantes Después:", f"{personaje['remaining_cubes_after']}"])
                personaje_info.append(["Puntos Restantes Después:", f"{personaje['remaining_points_after']}"])
            else:
                personaje_info.append(["¿Puede Garantizar?:", "No"])
                personaje_info.append(["Multis Disponibles:", f"{personaje['available_multis']}"])
                personaje_info.append(["Probabilidad con Disponibles:", f"{personaje['prob_with_available'] * 100:.2f}%"])
                personaje_info.append(["Cubos Adicionales Necesarios:", f"{personaje['missing_cubes']}"])
            
            personaje_table = Table(personaje_info, colWidths=[3*inch, 2*inch])
            personaje_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('PADDING', (0, 0), (-1, -1), 6)
            ]))
            content.append(personaje_table)
            content.append(Spacer(1, 0.1 * inch))
            
            # Información de escenarios optimistas
            if "escenarios_optimistas" in personaje:
                content.append(Paragraph("Escenarios Optimistas", styles['Subtitle']))
                
                escenarios_data = [
                    ["Escenario", "Multis", "Probabilidad", "Ahorro de Cubos"]
                ]
                
                for esc in personaje["escenarios_optimistas"]:
                    tipo_nombre = ""
                    if esc["tipo"] == "mitad":
                        tipo_nombre = "Mitad de Multis"
                    elif esc["tipo"] == "cuarto":
                        tipo_nombre = "Cuarto de Multis"
                    else:
                        tipo_nombre = "Primeras 5 Multis"
                        
                    escenarios_data.append([
                        tipo_nombre,
                        f"{esc['multis']}",
                        f"{esc['probabilidad'] * 100:.2f}%",
                        f"{esc['ahorro']}"
                    ])
                
                escenarios_table = Table(escenarios_data, colWidths=[1.5*inch, 1*inch, 1.25*inch, 1.25*inch])
                escenarios_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                    ('PADDING', (0, 0), (-1, -1), 6)
                ]))
                content.append(escenarios_table)
            
            # Escenarios optimistas del personaje anterior
            if "escenarios_previos" in personaje:
                content.append(Spacer(1, 0.1 * inch))
                content.append(Paragraph("Si el Personaje Anterior Sale Antes", styles['Subtitle']))
                
                for esc in personaje["escenarios_previos"]:
                    tipo_nombre = ""
                    if esc["tipo"] == "mitad":
                        tipo_nombre = "Mitad de Multis"
                    elif esc["tipo"] == "cuarto":
                        tipo_nombre = "Cuarto de Multis"
                    else:
                        tipo_nombre = "Primeras 5 Multis"
                        
                    prev_esc_data = [
                        [f"Escenario: {tipo_nombre} (Probabilidad: {esc['probabilidad'] * 100:.2f}%)"]
                    ]
                    prev_esc_details = [
                        ["Multis Necesarias:", f"{esc['multis']}"],
                        ["Ahorro de Cubos:", f"{esc['ahorro']}"],
                        ["Nuevos Cubos Disponibles:", f"{esc['nuevos_cubos']}"],
                    ]
                    
                    if esc["puede_garantizar"]:
                        prev_esc_details.append(["¿Podría Garantizar?:", "Sí"])
                        prev_esc_details.append(["Cubos Sobrantes:", f"{esc['nuevos_cubos'] - personaje['multis_needed'] * 3000}"])
                    else:
                        prev_esc_details.append(["¿Podría Garantizar?:", "No"])
                        prev_esc_details.append(["Multis Disponibles:", f"{esc['multis_disponibles']}"])
                        prev_esc_details.append(["Nueva Probabilidad:", f"{esc['nueva_probabilidad'] * 100:.2f}%"])
                    
                    # Tabla de título del escenario
                    title_table = Table(prev_esc_data, colWidths=[5*inch])
                    title_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, 0), colors.lightblue),
                        ('GRID', (0, 0), (0, 0), 1, colors.black),
                        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                        ('PADDING', (0, 0), (0, 0), 6)
                    ]))
                    content.append(title_table)
                    
                    # Tabla de detalles del escenario
                    details_table = Table(prev_esc_details, colWidths=[3*inch, 2*inch])
                    details_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                        ('PADDING', (0, 0), (-1, -1), 6)
                    ]))
                    content.append(details_table)
                    content.append(Spacer(1, 0.1 * inch))
            
            content.append(Spacer(1, 0.25 * inch))
        
        # Construir el PDF
        doc.build(content)
        return filename
    
    except ImportError:
        print("\nError: No se pudo generar el PDF. Asegúrate de tener instalada la biblioteca 'reportlab'.")
        print("Puedes instalarla con: pip install reportlab")
        return None


if __name__ == "__main__":
    main()