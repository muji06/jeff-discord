from math import floor
from typing import Optional
from discord import app_commands
from discord.ext import commands
import discord
import json
from requests import get
import time
from database import Session, Listeners
from discord.ui import View, Button
from discord.ui import Modal, TextInput, Button, Select


class ListenerListView(View):
    def __init__(self, listeners, remove_listener_callback):
        super().__init__(timeout=180)
        self.listeners = listeners
        self.remove_listener_callback = remove_listener_callback
        self.current_page = 0
        self.build()

    async def build(self):
        self.clear_items()
        for i, listener in enumerate(self.listeners[self.current_page * 5:(self.current_page + 1) * 5]):
            button = Button(label=f"{listener['event']} - {listener['channel']}", style=discord.ButtonStyle.red)
            button.custom_id = f"remove_listener_{i}"  # Unique ID for each button
            button.callback = self.remove_listener_button
            self.add_item(button)

        # Add pagination buttons (if applicable)
        if len(self.listeners) > 5:
            if self.current_page > 0:
                prev_button = Button(label="Previous", style=discord.ButtonStyle.gray)
                prev_button.callback = self.prev_page_button
                self.add_item(prev_button)
            if self.current_page < (len(self.listeners) // 5):
                next_button = Button(label="Next", style=discord.ButtonStyle.gray)
                next_button.callback = self.next_page_button
                self.add_item(next_button)

    async def remove_listener_button(self, interaction: discord.Interaction, button: Button):
        listener_index = int(button.custom_id.split("_")[-1])
        removed_listener = self.listeners.pop(listener_index + self.current_page * 5)
        await self.remove_listener_callback(interaction.guild, removed_listener) 
        await self.build() 

    async def prev_page_button(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.build()

    async def next_page_button(self, interaction: discord.Interaction, button: Button):
        if self.current_page < (len(self.listeners) // 5):
            self.current_page += 1
            await self.build()


async def remove_listener(guild: discord.Guild, listener_data):
    server_id = str(guild.id)
    current_listeners = Session.get(Listeners, server_id)
    if not current_listeners:
        return  

    listeners_list = current_listeners.listeners
    found = False
    for i, listener in enumerate(listeners_list):
        if (
            listener["event"] == listener_data["event"]
            and listener["channel"] == listener_data["channel"]
            and listener["ping"] == listener_data["ping"]
        ):
            del listeners_list[i]
            found = True
            break

    if found:
        current_listeners.listeners = listeners_list
        Session.commit()
    else:
        pass


class listen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="listen", description="Manage listeners in your server")
    @app_commands.choices(
        subcommand=[
            discord.app_commands.Choice(name="**Add**   :Add a new listener on this server", value="add"),
            discord.app_commands.Choice(name="**List**  :Shows current active listeners", value="list"),
        ],
        type=[
            discord.app_commands.Choice(name="**Alerts**         : Missions that periodically show up with a time limit", value="alert"),
            discord.app_commands.Choice(name="**Global Boosters**: The usual weekend boosters", value="booster"),
        ]
    )
    @commands.has_permissions(administrator= True)
    async def listen(self, interaction: discord.Interaction, subcommand: discord.app_commands.Choice[str], type: Optional[discord.app_commands.Choice[str]] = None, channel: Optional[discord.TextChannel] = None, role_to_ping: Optional[discord.Role] = None):
        # await interaction.response.defer()
        
        server_id = str(interaction.guild.id)
        current_listeners = Session.get(Listeners, server_id)

        if subcommand.value == "add":

            listeners_list = current_listeners.listeners if current_listeners else []

            # Add the new listener
            new_listener = {
                "event": type.value,
                "server": server_id,
                "channel": str(channel.id),
                "ping": str(role_to_ping.id),
            }
            listeners_list.append(new_listener)

            # Update the database with the new listener list
            if not current_listeners:
                new_listener_entry = Listeners(server_id=server_id, listeners=listeners_list)
                Session.add(new_listener_entry)
            else:
                current_listeners.listeners = listeners_list
            Session.commit()

            await interaction.response.send_message(f"Successfully added listener(s) for {type.value} events!")

        elif subcommand.value == "list":

            if not current_listeners:
                await interaction.response.send_message("No listeners found for this server.")
                return
            listener_view = ListenerListView(current_listeners.listeners, remove_listener)
            await interaction.response.send_message(view=listener_view)

        else:
            await interaction.message.send("Invalid subcommand.")

async def setup(bot):
    await bot.add_cog(listen(bot))