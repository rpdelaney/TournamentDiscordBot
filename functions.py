import discord


async def setup_category(interaction: discord.Interaction,
                         new_category: str) -> dict:
    try:
        for category in interaction.guild.categories:
            if category.name == new_category:
                return {'success': True,
                        'message': f'Category "**{new_category}**" exists.'}

        await interaction.guild.create_category(new_category)
        return {'success': True,
                'message': f'Category "**{new_category}**" created.'}

    except Exception as Error:
        return {'success': False,
                'message': f'Failed to create "**{new_category}**": {Error}'}


def count_match_channels(interaction: discord.Interaction) -> int:
    channel_count = 0
    for channel in interaction.guild.channels:
        if channel.name.startswith('match-'):
            channel_count += 1

    return channel_count


async def create_staff_role(interaction: discord.Interaction) -> dict:
    staff_role = discord.utils.get(interaction.guild.roles,
                                   name="Tournament Staff")
    if staff_role:
        return {'success': True,
                'message': 'Role "**Tournament Staff**" already exists.'}

    permissions = discord.Permissions(
        read_messages=True,
        send_messages=True,
        read_message_history=True,
        view_channel=True,
        manage_channels=True,
        manage_roles=True,
        create_instant_invite=True,
        embed_links=True
    )

    try:
        await interaction.guild.create_role(name="Tournament Staff",
                                            permissions=permissions)
        return {'success': True,
                'message':
                    'Role "**Tournament Staff**" created successfully.'}

    except discord.Forbidden:
        return {'success': False,
                'message':
                    'Error: Missing perms to create "**Staff**" role.'}
    except Exception as Error:
        return {'success': False,
                'message':
                    f'Error creating "**Tournament Staff**" role: {Error}'}
