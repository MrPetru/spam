
${c.asset_description(value=asset, id = 'description', extra_data = dict(user_id=c.user.id)).display() | n}

<div class="tasks">
    ${c.o_tasks(value=old_tasks, id = 'oldtasks').display() | n}
</div>

<script type="text/javascript">
    spam.toggles_activate_oldtasks()
</script>
