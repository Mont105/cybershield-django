from django.db import migrations

# datos de categorías
CATEGORIES = [
    ('Ofensivo', 'ofensivo', 'Evaluaciones que simulan a un atacante real.'),
    ('Defensivo', 'defensivo', 'Monitoreo, detección y respuesta continua.'),
    ('Infraestructura', 'infraestructura', 'Bastionado y endurecimiento de sistemas.'),
    ('Forense', 'forense', 'Investigación y respuesta ante incidentes.'),
    ('Normativa', 'normativa', 'Cumplimiento de estándares y regulaciones.'),
]

# datos de etiquetas
TAGS = [
    ('OWASP', 'owasp'), ('Pentesting', 'pentesting'), ('Redes', 'redes'),
    ('SIEM', 'siem'), ('SOC', 'soc'), ('Linux', 'linux'),
    ('Windows Server', 'windows-server'), ('CIS Benchmarks', 'cis-benchmarks'),
    ('DFIR', 'dfir'), ('ISO 27001', 'iso-27001'), ('CVSS', 'cvss'),
    ('Cloud', 'cloud'),
]

# datos de productos
PRODUCTS = [
    ('Test de Intrusión (Pentesting)',
     'Evaluación técnica bajo marco OWASP y PTES sobre aplicaciones web y perímetro de red. Incluye informe ejecutivo y técnico con plan de remediación.',
     1200000, 'catalog/background-letras-en-picada.jpg', 'ofensivo', ['owasp', 'pentesting', 'redes']),
    ('Monitoreo SOC y SIEM',
     'Correlación de logs en tiempo real, detección de vectores de persistencia y respuesta a incidentes con analistas 24/7.',
     850000, 'catalog/data-center_-768x534.jpg', 'defensivo', ['siem', 'soc', 'redes']),
    ('Hardening de Servidores',
     'Bastionado conforme a directrices CIS Benchmarks en entornos Linux y Windows Server, con validación posterior.',
     450000, 'catalog/servidores.jpg', 'infraestructura', ['linux', 'windows-server', 'cis-benchmarks']),
    ('Respuesta a Incidentes (DFIR)',
     'Análisis de memoria volátil, preservación de evidencia digital, cadena de custodia y erradicación tras una brecha.',
     1500000, 'catalog/background-letras-en-picada.jpg', 'forense', ['dfir', 'windows-server', 'linux']),
    ('Auditoría ISO 27001',
     'Diagnóstico de brechas (Gap Analysis), evaluación de controles SGSI y diseño de políticas para cumplimiento regulatorio.',
     2000000, 'catalog/laptop-image.jpg', 'normativa', ['iso-27001']),
    ('Gestión de Vulnerabilidades',
     'Escaneo periódico de infraestructura perimetral, priorización según CVSS y reportes técnicos de remediación.',
     600000, 'catalog/data-center_-768x534.jpg', 'defensivo', ['cvss', 'redes', 'cloud']),
    ('Pentesting de Aplicaciones Móviles',
     'Pruebas de seguridad sobre apps Android e iOS siguiendo OWASP MASVS: almacenamiento, comunicaciones y lógica.',
     1100000, 'catalog/laptop-image.jpg', 'ofensivo', ['owasp', 'pentesting']),
    ('Hardening de Entornos Cloud',
     'Revisión de configuraciones IAM, redes virtuales y almacenamiento en AWS/Azure según CIS Benchmarks.',
     900000, 'catalog/servidores.jpg', 'infraestructura', ['cloud', 'cis-benchmarks']),
    ('Análisis Forense de Equipos',
     'Adquisición forense de discos y dispositivos, línea de tiempo de eventos e informe pericial.',
     700000, 'catalog/laptop-image.jpg', 'forense', ['dfir', 'windows-server']),
    ('Red Team Corporativo',
     'Campaña adversarial completa: ingeniería social, intrusión física y movimiento lateral en la red interna.',
     3500000, 'catalog/background-letras-en-picada.jpg', 'ofensivo', ['pentesting', 'redes', 'windows-server']),
]


# carga de datos iniciales
def poblar(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    Tag = apps.get_model('catalog', 'Tag')
    Product = apps.get_model('catalog', 'Product')

    cats = {}
    for name, slug, desc in CATEGORIES:
        cats[slug], _ = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
    tags = {}
    for name, slug in TAGS:
        tags[slug], _ = Tag.objects.get_or_create(slug=slug, defaults={'name': name})

    for title, desc, price, image, cat, tag_slugs in PRODUCTS:
        product = Product.objects.filter(title=title).first()
        if product is None:
            product = Product(title=title, description=desc, price=price, image=image)
        else:
            product.description = desc
            product.price = price
        product.category = cats[cat]
        product.save()
        product.tags.set([tags[t] for t in tag_slugs])

    # productos antiguos sin categoría
    Product.objects.filter(category__isnull=True).update(category=cats['ofensivo'])


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_categorias_etiquetas'),
    ]

    operations = [
        migrations.RunPython(poblar, migrations.RunPython.noop),
    ]
