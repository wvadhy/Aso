from discord import (
    Embed as ebd,
    Game as gm,
    utils as ut
)
from requests import (
    get
)
from json import (
    loads
)
from random import (
    choice
)
from time import (
    localtime as lt
)
from discord.ext import commands

client = commands.Bot(command_prefix='-')

URLS = {
    "villager": 'https://obufilsoc.com/imgs/villager-r.png',
    "creeper": 'https://obufilsoc.com/imgs/creeper-r.png',
    "wave_1": 'https://obufilsoc.com/imgs/wave.png',
    "wave_3": 'https://obufilsoc.com/imgs/wave_3.png',
    "kanye": 'https://api.kanye.rest/'
}

CMD_LIST = {
    '-h': "Displays commands",
    '-mc': "Displays minecraft realm information",
    '-joinmc': "Sends a request to join the realm ( ~5m )",
    '-inspire': "Get some life advice",
    '-website': "Provides a link to our website",
    '-verify': "Get access to the member role",
}

SLAPS = ['hard', 'soft', 'strong', 'delicate', 'humongous', 'devastating', 'bitch', 'clown', 'weak']

SERVER_ID = 1156034805033619536


@client.event
async def on_ready():
    print(f"Started {client.user}")
    await client.change_presence(activity=gm(name=f"type -h for help!"))


@client.event
async def on_message(msg):
    ct = msg.content.startswith

    if ct('-h'):
        """
        Outputs a list of commands
        
        :rtype -> None
        """
        embed = ebd(title="Commands:",
                    description=f"""
                                **~ General**
                                -h: {CMD_LIST['-h']}
                                -inspire: {CMD_LIST['-inspire']}
                                -website: {CMD_LIST['-website']}
                                -verify: {CMD_LIST['-verify']}

                                **~ Minecraft**
                                -mc: {CMD_LIST['-mc']}
                                -joinmc: {CMD_LIST['-joinmc']}
                                """,
                    color=0x6C3428)
        embed.set_thumbnail(url=URLS["villager"])
        embed.set_image(url=URLS["wave_1"])
        await msg.channel.send(embed=embed)

    if ct("-inspire"):
        """
        Gives some inspiring advice
        
        :rtype -> None
        """
        await msg.channel.send(f"A wise man once said '{loads(get(URLS['kanye']).text)['quote']}'")

    if ct("-slap"):
        """
        Slaps a server member
        
        :rtype -> None
        """
        member = msg.content.split('-slap ', 1)
        if len(member) > 1:
            await msg.channel.send(f"You give @{member[1]} a {choice(SLAPS)} slap!")
        else:
            await msg.channel.send(f"Pick someone to slap!")

    if ct('-joinmc'):
        """
        Sends a join request to the minecraft Realm server as proxy 
        through azure and via XBL 3.0 authentication and the Realms API pipeline
        
        :arg -> A valid java edition username
        :rtype -> None (Optional)
            L:True -> On valid response sends a invite to user
            L:False -> On invalid response outputs *error to channel chat
                L:exception -> ConnectionError
                    L:raise -> Request failure
        """
        u = msg.content.split('-joinmc ', 1)
        if len(u) < 2:
            await msg.channel.send(embed=
            ebd
                (
                description=f"Please send a valid **java edition** username",
                color=0xFFB000
            ))
        else:
            user = f"{u[1]}\n"
            with open("local-data/logins.txt", 'r+') as f:
                if user in f.readlines():
                    await msg.channel.send(embed=
                    ebd(
                        description=f"**Error** user {user} has already been added",
                        color=0xD71313
                    ))
                else:
                    f.write(user)
                    await msg.channel.send(embed=
                    ebd(
                        description=f"Join request from **{user[1]}** sent today at **{lt().tm_hour}:{lt().tm_min}**",
                        color=0xD1282
                    ))
                    await msg.author.send(embed=
                    ebd(
                        description=f"Woof woof you have been successfully added!",
                        colour=0xA6FF96
                    ))

    if ct('-mc'):
        """
        Outputs minecraft realm information via XBL 3.0 authentication and the Realms API
        
        :rtype -> None
        """
        with open("local-data/logins.txt", 'r') as f:
            players = ''.join(f.readlines()).split('\n')
            store = ["**Server data:**", "Server time: ~", "Server age: ~",
                     "Server difficulty: Normal", "", "**Active players:**"]
            for i in players:
                store.append(i)
            embed = ebd(title="OBU TROPAS",
                        description='\n'.join(store), colour=0x04225)
            embed.set_thumbnail(url=URLS["creeper"])
            embed.set_image(url=URLS["wave_3"])
            await msg.channel.send(embed=embed)

    if ct('-website'):
        """
        Outputs a link to the fil-soc website
        
        :rtype -> None
        """
        await msg.channel.send(embed=
        ebd
            (
            description="**->** https://obufilsoc.com/",
            colour=0xD1282
        ))

    if ct('-verify'):
        """
        Validates a 10-digit key
        
        :param -> Key
        :arg -> 10-digit key
        :rtype -> None (Optional)
            L:True -> Assign member role to user
            L:False -> Outputs an *error to channel chat
                L:exception -> Exception
                    L:raise -> Role assignment failure
        """
        code = msg.content.split('-verify ', 1)
        server = client.get_guild(SERVER_ID)
        member = await server.fetch_member(msg.author.id)
        if len(code) > 1:
            key = f"{code[1]}\n"
            if len(key) >= 10:
                if key not in (x := open('local-data/used_keys.txt', 'r+')).readlines():
                    x.close()
                    with open("local-data/keys.txt", 'r+') as f:
                        if key in f.readlines():
                            try:
                                await member.add_roles(ut.get(server.roles, name="Members"))

                                with open("local-data/used_keys.txt", 'a') as e:
                                    e.write(f"{code[1]}\n")

                            except Exception as e:
                                await msg.channel.send(embed=
                                ebd
                                    (
                                    description=f"**Error**: role assignment failure",
                                    color=0xD71313
                                ))
                            else:
                                await msg.channel.send(embed=
                                ebd
                                    (
                                    description=f"Member role granted woof!",
                                    color=0xD2DE32
                                ))
                        else:
                            await msg.channel.send(embed=
                            ebd
                                (
                                description=f"**Error**: invalid key",
                                color=0xD71313
                            ))
                else:
                    await msg.channel.send(embed=
                    ebd
                        (
                        description=f"**Error**: key has already been registered",
                        color=0xD71313
                    ))

            else:
                await msg.channel.send(embed=
                ebd
                    (
                    description=f"Please submit the **10 digit code** which was sent to your **email**",
                    color=0xD71313
                ))
        else:
            error_embed = ebd(description=f"**Error**: no code submitted", color=0xFFB000)
            await msg.channel.send(embed=error_embed)


client.run("MTE1Njk1NTM2MjE4OTExNTU5Mw.GPY7sm.JJRh5vY-DNPetneNz-y2zFQPZpG-BcvpIt75Fc")
