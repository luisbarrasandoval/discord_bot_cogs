from discord.ext import commands
import discord
import argparse
import json
import asyncio

class Poll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, *args):
        """
        Create a poll.
        """

        # format question !poll -t "titulo" -d "descripcion" -a "opcion1" -i 'icono opcion 1' -a "opcion 2" -i 'icono opcion 2' -a "opcion n..." -i 'icono m...'

        parser = argparse.ArgumentParser(description='Create a poll.')
        parser.add_argument('-t', '--title', type=str, help='Title of the poll.')
        parser.add_argument('-d', '--description', type=str, help='Description of the poll.')
        parser.add_argument('-a', '--answer', type=str, action='append', help='Answers of the poll.')
        parser.add_argument('-i', '--icon', type=str, help='Icon of the poll.', action='append')



        args = parser.parse_args(args)

        if args.title is None:
            await ctx.send('You must specify a title.')
            return

        if args.description is None:
            await ctx.send('You must specify a description.')
            return

        if args.answer is None:
            await ctx.send('You must specify at least one answer.')
            return

        embed = discord.Embed(
            title=args.title,
            description=args.description,
            color=0x00ff00,
        )

        for i, answer in enumerate(args.answer):
            embed.add_field(
                name=f"{answer} {args.icon[i]}",
                value='0',
                inline=False
            )


        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)

        for icon in args.icon:
            await msg.add_reaction(icon)
            print (icon)


        def check(reaction, user):
            return str(reaction.emoji) in args.icon
        

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                break

            for i, answer in enumerate(args.answer):
                if str(reaction.emoji) == args.icon[i]:
                    embed.set_field_at(i,
                        name=f"{answer} {args.icon[i]}",
                        value=str(int(embed.fields[i].value) + 1),
                        inline=False)
                
                    await msg.edit(embed=embed)



       
        
        
        


def setup(bot):
    bot.add_cog(Poll(bot))
