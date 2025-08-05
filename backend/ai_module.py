# Módulo de análisis AI para empleos SIMO
# Aquí puedes integrar modelos de clasificación, recomendación, etc.
def clasificar_empleos(empleos, perfil_usuario=None):
    # Ejemplo: priorizar empleos por salario
    return sorted(empleos, key=lambda e: int(''.join(filter(str.isdigit, e.get('asignacion_salarial','0')))), reverse=True)
