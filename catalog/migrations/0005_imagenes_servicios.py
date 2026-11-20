from django.db import migrations

# imagen asignada a cada servicio
IMAGES = {
    'Test de Intrusión (Pentesting)': 'catalog/pentesting-web.jpg',
    'Monitoreo SOC y SIEM': 'catalog/soc-siem.jpg',
    'Hardening de Servidores': 'catalog/hardening-servidores.jpg',
    'Respuesta a Incidentes (DFIR)': 'catalog/dfir.jpg',
    'Auditoría ISO 27001': 'catalog/iso-27001.jpg',
    'Gestión de Vulnerabilidades': 'catalog/gestion-vulnerabilidades.jpg',
    'Pentesting de Aplicaciones Móviles': 'catalog/pentesting-movil.jpg',
    'Hardening de Entornos Cloud': 'catalog/hardening-cloud.jpg',
    'Análisis Forense de Equipos': 'catalog/forense-equipos.jpg',
    'Red Team Corporativo': 'catalog/red-team.jpg',
}


# actualización de imágenes de los servicios
def asignar_imagenes(apps, schema_editor):
    Product = apps.get_model('catalog', 'Product')
    for title, image in IMAGES.items():
        Product.objects.filter(title=title).update(image=image)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_categoria_obligatoria'),
    ]

    operations = [
        migrations.RunPython(asignar_imagenes, migrations.RunPython.noop),
    ]
