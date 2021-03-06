from io import BytesIO
from string import hexdigits

import discord

from bot.bot import Bot
from discord.ext.commands import Cog, Context, command
from PIL import Image


class Color(Cog):
    @staticmethod
    def parse_color(color_code: str) -> str:
        color_code = color_code.replace("0x", "#")
        color_code = "#" + color_code if len(color_code) == 6 and all(i in hexdigits for i in color_code) else color_code
        color_code = color_code.replace(",", " ")

        if len(ls := color_code.split()) == 3:
            color_code = "rgb(" + ", ".join(ls) + ")"
        elif len(ls := color_code.split()) == 4:
            color_code = "rgba(" + ", ".join(ls) + ")"

        return color_code

    @command(
        help="""color <color value>
            Get a visual picture for color given as input, valid formats are \
            hex (with or without #/0x), rgb.

            Hex color codes must be 6 character long valid colors.
            For rgb, give input as follows -
            color rgb(v1, v2, v3), color hsv(v1, v2, v3) etc.
            """,
        brief="Get a image of the color given as input",
        name="color",
        aliases=("col",),
    )
    async def color_command(self, ctx: Context, *, color_code) -> None:
        try:
            color_code = self.parse_color(color_code)
            new_col = Image.new("RGB", (128, 128), color_code)
            bufferio = BytesIO()
            new_col.save(bufferio, format="PNG")
            bufferio.seek(0)

            file = discord.File(bufferio, filename="color.png")

            await ctx.send(file=file)
        except ValueError:
            await ctx.send(f"Unknown color specifier '{color_code}'")


def setup(bot: Bot) -> None:
    """Load the Color cog."""
    bot.add_cog(Color(bot))
