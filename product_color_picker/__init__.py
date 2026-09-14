from . import models


def pre_init_hook(env):
    """Clean up orphaned ir.model.fields record for product_color if the column is missing."""
    env.cr.execute("""
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'product_template' AND column_name = 'product_color'
    """)
    if not env.cr.fetchone():
        env.cr.execute("""
            DELETE FROM ir_model_fields
            WHERE model = 'product.template' AND name = 'product_color'
        """)
