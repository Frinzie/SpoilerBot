import discord
import sys
from discord.ext import commands

description = 'use "*spoiler" to spoiler file or "*spoiler <text> "' + \
              'to include text as well!'


class SpoilerBot(commands.Cog):
    async def spoiler_attachments(self, attachments):
        files = []
        for attachment in attachments:
            f = await attachment.to_file()
            f.filename = "SPOILER_" + f.filename
            files.append(f)
        return files

    @commands.command()
    async def spoiler(self, ctx, text: str = ""):
        message = ctx.message
        if len(message.attachments):
            message = ctx.message
            attachments = message.attachments
            channel = message.channel
            files = await self.spoiler_attachments(attachments)
            text = message.content[9:]

            # Checks if the message wasn't in DMs
            if not isinstance(channel, discord.DMChannel):
                user_mention = message.author.mention
                await message.delete()
                text = user_mention + ": " + text
                await channel.send(text, files=files)
            else:
                await channel.send(files=files)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invalid arguments")
        print("Please call spoiler_bot with <token>")
        exit(0)

    bot = commands.Bot(command_prefix='*', description=description)
    bot.add_cog(SpoilerBot(bot))

    bot.run(sys.argv[1])
