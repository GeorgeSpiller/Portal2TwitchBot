from threading import Timer

from twitchbot import *

from cmdPipelineHandler import newIncommingCommand
from ConsoleCommands import setup

# https://twitchtokengenerator.com/


def run_bot(txn, cmdDict):
    @Command('thirdperson',
         help='This command toggles between firstperson and thirdperson.',
         syntax='!thirdperson',
         aliases=['firstperson'])
    async def cmd_thirdperson(msg: Message, *args):
        # thirdperson
        result, e_msg = newIncommingCommand(txn, cmdDict, 'thirdperson', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, Toggled thirdperson.', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @Command('allowallportals',
            help='This command toggles between normal portal placement, and placment of portals anywhere.',
            syntax='!allowallportals',
            aliases=['allowportals', 'allowall', 'alowallportals', 'alowallportals'])
    async def cmd_allowallportals(msg: Message, *args):
        # sv_portal_placement_never_fail
        result, e_msg = newIncommingCommand(txn, cmdDict, 'sv_portal_placement_never_fail', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, Portal placement anywhere is now #ON/OFF#.', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @Command('shake',
            help='This command shakes the screen',
            syntax='!shake')
    async def cmd_shake(msg: Message, *args):
        # shake
        result, e_msg = newIncommingCommand(txn, cmdDict, 'shake', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, Screen Shooketh\'', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)
    @Command('explode',
            help='This command makes me explode.',
            syntax='!explode',
            aliases=['kill', 'crash', 'restart', 'reset'])
    async def cmd_explode(msg: Message, *args):
        # explode
        result, e_msg = newIncommingCommand(txn, cmdDict, 'explode', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, has been boom\'ed', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @Command('fizzle',
            help='This command fizzles (removes) all portals.',
            syntax='!fizzle',
            aliases=['flizle', 'removeportals'])
    async def cmd_fizzle(msg: Message, *args):
        # ent_fire prop_portal fizzle
        result, e_msg = newIncommingCommand(txn, cmdDict, 'ent_fire prop_portal fizzle', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, All portals have been fizzled', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @Command('resize_portals',
            help='This command resizes portals to the given width and height for 30 seconds.',
            syntax='!resize_portals <width> <height>. Default: !resize_portals 33 55',
            aliases=['resize'])
    async def cmd_resize_portals(msg: Message, *args):
        # portals_resizeall
        result, e_msg = newIncommingCommand(txn, cmdDict, 'portals_resizeall', msg.author, parameterList=list(args))
        if result:
            await msg.reply(f'{msg.mention} portals resized to width:{args[0]} and height:{args[1]} for 30 seconds', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)
        t = Timer(10, newIncommingCommand, [txn, cmdDict, 'portals_resizeall', msg.author], {'reset':True, 'parameterList':list(args)})
        t.start()

    # the 'create' commands
    cmd_create = DummyCommand('create',         
        help='This command creates an object.',
        syntax='!create <object>. Use !create to see a list of spawnable objects.',
        aliases=['c'])

    @SubCommand(cmd_create, 'cube')
    async def cmd_cmd_create_cube(msg, *args):
        # ent_create_portal_companion_cube
        result, e_msg = newIncommingCommand(txn, cmdDict, 'ent_create_portal_companion_cube', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, Creating cube.', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @SubCommand(cmd_create, 'gel_portal')
    async def cmd_cmd_create_gel_portal(msg, *args):
        # ent_create_paint_bomb_portal
        result, e_msg = newIncommingCommand(txn, cmdDict, 'ent_create_paint_bomb_portal', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, Creating gel_portal.', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @SubCommand(cmd_create, 'gel_jump')
    async def cmd_cmd_create_gel_jump(msg, *args):
        # ent_create_paint_bomb_jump
        result, e_msg = newIncommingCommand(txn, cmdDict, 'ent_create_paint_bomb_jump', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, Creating gel_jump.', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @SubCommand(cmd_create, 'gel_speed')
    async def cmd_cmd_create_gel_speed(msg, *args):
        # ent_create_paint_bomb_speed
        result, e_msg = newIncommingCommand(txn, cmdDict, 'ent_create_paint_bomb_speed', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, Creating gel_speed.', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @SubCommand(cmd_create, 'turret')
    async def cmd_cmd_create_turret(msg, *args):
        # npc_create npc_portal_turret_floor
        result, e_msg = newIncommingCommand(txn, cmdDict, 'npc_create npc_portal_turret_floor', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, Creating turret.', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @SubCommand(cmd_create, 'wheatly')
    async def cmd_cmd_create_wheatly(msg, *args):
        # ent_create npc_personality_core
        result, e_msg = newIncommingCommand(txn, cmdDict, 'ent_create npc_personality_core', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, Creating wheatly.', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @SubCommand(cmd_create, 'rocket')
    async def cmd_cmd_create_rocket(msg, *args):
        # fire_rocket_projectile
        result, e_msg = newIncommingCommand(txn, cmdDict, 'fire_rocket_projectile', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, Creating rocket.', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @SubCommand(cmd_create, 'door')
    async def cmd_cmd_create_door(msg, *args):
        # give prop_testchamber_door
        result, e_msg = newIncommingCommand(txn, cmdDict, 'give prop_testchamber_door', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, Creating door.', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @SubCommand(cmd_create, 'error')
    async def cmd_cmd_create_error(msg, *args):
        # ent_create prop_dynamic
        result, e_msg = newIncommingCommand(txn, cmdDict, 'ent_create prop_dynamic', msg.author)
        if result:
            await msg.reply(f'{msg.mention}, Creating error.', whisper=True)
        else:
            await msg.reply(f'{msg.mention}, {e_msg}', whisper=True)

    @event_handler(Event.on_privmsg_received)
    async def on_privmsg_received(msg: Message):
        print(f'{msg.author} sent message {msg.content} to channel {msg.channel_name}')

    BaseBot().run()


if __name__ == '__main__':
    print("no")
    exit()
