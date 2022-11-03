import asyncio
import logging

import discord
import camera.camera as cam
from sys import platform
from discord import app_commands
from discord_bot import upload_to_drive

# TODO: Image correction
# TODO: Capture image from hdmi

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
discord_object_id = "YOUR DISCORD SERVER ID HERE"

windows = False
if platform == "win32":
    windows = True
    camera_id = 1
else:
    camera_id = 0

height = 1280
width = 720
camera = cam.Camera(camera_id, windows, height, width)


@client.event
async def on_ready():
    logging.info(f'Successfully logged in as {client.user}')


role1 = "Verified TINF21AI1"


async def has_role(ctx, ctx_msg=True):
    if ctx_msg:
        for role in ctx.user.roles:
            if role1 == role.name:
                return True
        return False
    else:
        for role in ctx.author.roles:
            if role1 == role.name:
                return True
        return False


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$sync'):
        if await has_role(message, False):
            await sync_commands()
            await message.channel.send('Synced commands')
        else:
            await message.channel.send("You don't have the permissions to use this command")


@tree.command(name="tafel", description="Sends a picture of the current board",
              guild=discord.Object(id=discord_object_id))
async def get_image_from_board(ctx, colour: bool = False):
    if await has_role(ctx):
        print("Image sent")
        channel = ctx.channel
        img_path = camera.get_current_board(channel, colour)
        img = discord.File(img_path)
        await ctx.response.defer()
        await asyncio.sleep(0)
        await ctx.followup.send(file=img)
    else:
        await ctx.response.send_message("You don't have the permissions to use this command")


@tree.command(name="exposure", description="Changes exposure. Range between-100000 and 100000",
              guild=discord.Object(id=discord_object_id))
async def change_exposure(ctx, arg1: int):
    if await has_role(ctx):
        print("Exposure changed")
        camera.change_exposure(int(arg1), False)
        await ctx.response.send_message(f"The exposure is now set to {int(arg1)}")
    else:
        await ctx.response.send_message("You don't have the permissions to use this command")


@tree.command(name="auto-exposure", description="Changes exposure to auto", guild=discord.Object(id=discord_object_id))
async def change_to_auto_exposure(ctx):
    if await has_role(ctx):
        print("Test Command")
        camera.change_exposure(0, True)
        await ctx.response.send_message(f"The Exposure is now set to auto")
    else:
        await ctx.response.send_message("You don't have the permissions to use this command")


@tree.command(name="upload", description="Uploads all images to the cloud and deletes the local images",
              guild=discord.Object(id=discord_object_id))
async def upload_images(ctx):
    if await has_role(ctx):
        print("Up")
        res = upload_to_drive.upload_and_delete()
        if res:
            await ctx.response.send_message("Images were uploaded successfully")
        else:
            await ctx.response.send_message("Images could not be uploaded")
    else:
        await ctx.response.send_message("You don't have the permissions to use this command")


async def sync_commands():
    await tree.sync(guild=discord.Object(id=discord_object_id))


def run_bot():
    client.run("YOUR DISCORD BOT TOKEN HERE")
