import discord
import sys


class SpoilerBot(discord.Client):
    async def spoiler_attachments(self, attachments):
        files = []
        for attachment in attachments:
            f = await attachment.to_file()
            f.filename = "SPOILER_" + f.filename
            files.append(f)
        return files

    async def on_message(self, message):
        # Determine whether user is trying to use *spoiler
        content = message.content
        is_spoiler_command = (content.lower().startswith("*spoiler ") or
                              content == "*spoiler")
        # Check if *spioler and if there are any attachments anyways
        if is_spoiler_command and len(message.attachments):
            attachments = message.attachments
            channel = message.channel
            files = await self.spoiler_attachments(attachments)
            text = content[9:]

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

    sb = SpoilerBot()
    sb.run(sys.argv[1])
