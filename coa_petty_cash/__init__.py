from . import models


def post_init_hook(env):
    """Add admin and root users to the petty cash manager group on install."""
    manager_group = env.ref('petty_cash.group_petty_cash_manager', raise_if_not_found=False)
    if not manager_group:
        return
    for xml_id in ('base.user_admin', 'base.user_root'):
        user = env.ref(xml_id, raise_if_not_found=False)
        if user and manager_group not in user.group_ids:
            env.cr.execute(
                "INSERT INTO res_groups_users_rel (gid, uid) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (manager_group.id, user.id)
            )
