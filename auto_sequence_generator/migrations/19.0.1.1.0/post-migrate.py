def migrate(cr, version):
    # Strip PRD- from ir.sequence prefixes created by this module
    cr.execute("""
        UPDATE ir_sequence
           SET prefix = SUBSTRING(prefix FROM 5)
         WHERE code LIKE 'product.categ.%'
           AND prefix LIKE 'PRD-%'
    """)

    # Strip PRD- from existing product internal references
    cr.execute("""
        UPDATE product_template
           SET default_code = SUBSTRING(default_code FROM 5)
         WHERE default_code LIKE 'PRD-%'
    """)
    cr.execute("""
        UPDATE product_product
           SET default_code = SUBSTRING(default_code FROM 5)
         WHERE default_code LIKE 'PRD-%'
    """)
