from discord.ext import commands
import requests
import discord


__AUTHOR__ = 'LFBS'
__VERSION__ = '0.0.1'
__LICENSE__ = 'GPL-3.0'


class GitHub(commands.Cog):
    """
    Get public repositories of a user
    """

    API_URL = 'https://api.github.com'
    session = requests.Session()

    def __init__(self, bot):
        self.bot = bot
        self.session.headers.update(
            {'User-Agent': 'OpenPega BOT'}
        )

    @commands.command(aliases=['gh'])
    async def github_user(self, ctx, user):
        """
        Get the GitHub user's profile.
        """
        url = f'{self.API_URL}/users/{user}'
        response = self.session.get(url)
        if response.status_code != 200:
            await ctx.send(f'User {user} not found.')
            return


        data = response.json()
        embed = discord.Embed(
            title=data['name'],
            url=data['html_url'],
            description=data['bio'],
            color=0x00ff00,
        )


        if data['public_repos'] > 0:
            embed.add_field(
                name='Public Repositories',
                value=data['public_repos'],
                inline=True
            )
        
        if data['public_gists'] > 0:
            embed.add_field(
                name='Public Gists',
                value=data['public_gists'],
                inline=True
            )


        embed.set_thumbnail(url=data['avatar_url'])
        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
    

    # repro y gits se puede refactorizar

    @commands.command(name='github_repo', aliases=['ghr'])
    async def github_repo(self, ctx, user):
        """
        Get the GitHub user's repositories.
        """
        data = await self.github_get_list(user, 'repos')
        if data is None:
            await ctx.send(f'User {user} not found.')
            return
        
        embed = discord.Embed(
            title=f'{user}\'s repositories',
            color=0x00ff00,
        )

        for repo in data:
            embed.add_field(
                name=repo['name'],
                value=repo['description'],
                inline=False
            )

        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
    
    
    @commands.command(name='github_gist', aliases=['ghg'])
    async def github_gist(self, ctx, user):
        """
        Get github user's gists.
        """
        data = await self.github_get_list(user, 'gists')
        if data is None:
            await ctx.send(f'User {user} not found.')
            return
        
        embed = discord.Embed(
            title=f'{user}\'s gists',
            color=0x00ff00,
        )

        for gist in data:
            embed.add_field(
                name=gist['description'],
                value=gist['html_url'],
                inline=False
            )

        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)


    async def github_get_list(self, user, type):
        url = f'{self.API_URL}/users/{user}/repos'
        response = self.session.get(url)
        if response.status_code != 200:
            return None

        data = response.json()
        return data



def setup(bot):
    bot.add_cog(GitHub(bot))