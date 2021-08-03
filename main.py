import discord
import time
import asyncio
from discord.ext import commands

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
client.remove_command('help')
hello_words = ['hello', 'wats up', 'ky']
answer_words = ['че за серв', 'шо тут делать']
good_bye_words = ['пок']


@client.event
async def on_ready():
    print('Bot connected')


@client.event  # выдача роли при входе пользователя
async def on_member_join(member):
    channel = client.get_channel(837981733243715587)
    role = discord.utils.get(member.guild.roles, id=842060132107419648)
    await member.add_roles(role)
    await channel.send(
        embed=discord.Embed(description=f'Пользователь ``{member.name}``, присоединился к нам', color=0x0c0c))


@client.event
async def on_raw_reaction_add(payload):
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    if payload.emoji.name == '👍':
        role = discord.utils.get(guild.roles, id=842048881432068097)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        await member.add_roles(role)
    if payload.emoji.name == '👀':
        role = discord.utils.get(guild.roles, id=842060132107419648)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        await member.add_roles(role)
    print(payload.emoji.name)


@client.command(pass_context=True)  # отправка самому себе
async def send_a(ctx):
    await ctx.author.send('Hello World')


@client.command(pass_context=True)  # отправка любому пользователю
async def send_m(ctx, member: discord.Member):
    await member.send(f'{member.name} привет от {ctx.author.name}')


@client.command(pass_context=True)  # удаление сообщений
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


@client.command(pass_context=True)  # hello
async def hello(ctx, mes=''):
    author = ctx.message.author
    await ctx.send(f'Hello {author.mention}' + mes)


@client.command(pass_context=True)  # kick
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    await ctx.send(f'kick {member.mention}')


@client.command(pass_context=True)  # ban
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title=time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()), colour=discord.Color.red())
    await ctx.channel.purge(limit=1)
    await member.ban(reason=reason)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Ban user', value='Banned user : {}'.format(member.mention))
    emb.set_footer(text='Был забанен {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


@client.command(pass_context=True)  # help
async def help(ctx):
    emb = discord.Embed(title='Навигация по командам')
    emb.add_field(name='{}clear'.format(client.command_prefix), value='Очистка чата')
    emb.add_field(name='{}hello'.format(client.command_prefix), value='Приветствие')
    emb.add_field(name='{}kick'.format(client.command_prefix), value='Кик участника')
    emb.add_field(name='{}ban'.format(client.command_prefix), value='Бан участника')
    emb.add_field(name='{}search'.format(client.command_prefix), value='Ссылки на поисковики')
    await ctx.send(embed=emb)


@client.command(pass_context=True)  # тест картинок и тд
async def search(ctx):
    emb = discord.Embed(title='Google', description='Вы сможете найти что-то в инете', color=discord.Color.green(),
                        url="https://www.google.com/")
    emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    emb.set_footer(text='Спасибо ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    emb.set_image(url='https://for-travels.ru/wp-content/uploads/2017/08/vlazhniy-korzh-dlya-torta-foto-3.jpg')
    emb.set_thumbnail(
        url='https://im0-tub-ru.yandex.net/i?id=d9948657e6f2a6964eac4469be865448&ref=rim&n=33&w=207&h=188')
    emb.add_field(name='Yandex', value='https://yandex.ru/')
    await ctx.send(embed=emb)


@client.event  # ответ на всякие словечки
async def on_message(message):
    await client.process_commands(message)
    msg = message.content.lower()
    if msg in hello_words:
        await message.channel.send('Шо надо пес?')
    if msg in answer_words:
        await message.channel.send('Пропиши в чат команду !help')
    if msg in good_bye_words:
        await message.channel.send('Земля те пухом')


@client.command()  # mute
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, t='навсегда'):
    await ctx.channel.purge(limit=2)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Mute')
    if t == 'навсегда':
        await member.add_roles(mute_role)
        await ctx.send(f'Mute {member.mention}, ограничение чата за нарушение прав')
    else:
        await member.add_roles(mute_role)
        await ctx.send(f'Mute {member.mention}, ограничение чата за нарушение прав')
        await asyncio.sleep(int(t))
        await unmute(ctx, member)


@client.command()  # unmute
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    await ctx.channel.purge(limit=2)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Mute')
    await member.remove_roles(mute_role)
    await ctx.send(f'Unmute {member.mention}, за хорошее поведение')


@client.command()  # mute channel
@commands.has_permissions(administrator=True)
async def mute_channel(ctx, kanal=837981733243715588):
    await ctx.channel.purge(limit=2)
    for i in client.get_channel(id=kanal).members:
        if i != ctx.author:
            await i.edit(mute=True)


@client.command()  # unmute chanenl
@commands.has_permissions(administrator=True)
async def unmute_channel(ctx, kanal=837981733243715588):
    await ctx.channel.purge(limit=2)
    for i in client.get_channel(id=kanal).members:
        if i != ctx.author:
            await i.edit(mute=False)


@client.command()  # крестики-нолики
async def XO(ctx, x, y=int()):
    if x == 'game':
        place = []
        for i in range(3):
            place.append([])
            for j in range(3):
                place[i].append("~ ")
        for i in range(len(place)):
            f = ''
            for j in range(len(place[i])):
                g = place[i][j]
                f += g
        await ctx.send(f"```{f}\n{f}\n{f}```")
        lm = ctx.channel.last_message_id

    combination = [[[1, 1], [2, 1], [3, 1]], [[1, 2], [2, 2], [3, 2]], [[1, 3], [2, 3], [3, 3]],
                   [[1, 1], [1, 2], [1, 3]], [[2, 1], [2, 2], [2, 3]], [[3, 1], [3, 2], [3, 3]],
                   [[1, 1], [2, 2], [3, 3]], [[1, 3], [2, 2], [3, 1]]]
    combinationX = []
    combinationO = []
    X = "O "
    O = "X "
    what = ''
    like = 0
    round = 0
    win = False
    who = True
    while win != True:
        if who == True:
            what = O
            await ctx.send(f"Ход {what}")
            who = False
        else:
            what = X
            await ctx.send(f"Ход {what}: ")
            who = True

        while True:
            mes = await client.wait_for('message')
            try:
                if type(int(mes.content[0])) == int and type(int(mes.content[2])) == int:
                    ryd = int(mes.content[0])
                    mesto = int(mes.content[2])
                    break
            except ValueError:
                await ctx.channel.purge(limit=1)

        await ctx.channel.purge(limit=2)
        for i in range(ryd):
            for j in range(mesto):
                if i == ryd - 1 and j == mesto - 1:
                    place[i].insert(j, what)
                    place[i].pop(j + 1)
        z = ''
        for i in range(len(place)):
            f = ''
            for j in range(len(place[i])):
                g = place[i][j]
                f += g
            z = z + f + '\n'
        b = await ctx.fetch_message(lm)
        await b.edit(content=f"```{z}```")
        if what == O:
            combinationX += [[ryd, mesto]]
        else:
            combinationO += [[ryd, mesto]]
        if what == O:
            for i in range(len(combination)):
                like = 0
                for g in combinationX:
                    for j in combination[i]:
                        if j == g:
                            like += 1
                            if like == 3:
                                win = True
                                await ctx.send("Игра закончена. Победитель Крестик")
        else:
            for i in range(len(combination)):
                like = 0
                for g in combinationO:
                    for j in combination[i]:
                        if j == g:
                            like += 1
                            if like == 3:
                                win = True
                                await ctx.send("Игра закончена. Победитель Нолик")
        round += 1
        if round == 9:
            win = True
            await ctx.send("Игра закончена. Ничья")


client.run('TOKEN')
'''нельязя палить токен)))'''
