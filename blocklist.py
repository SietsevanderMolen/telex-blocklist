import tgl
from telex import plugin, auth
import re

class AccessError(Exception):
    pass


class BlocklistPlugin(plugin.TelexPlugin):
    """
    Blocklist plugin for Telex bot.
    """
    patterns = {
        "^{prefix}block$": "block",
        "^{prefix}block (\d+)$$": "block_by_id",
        "^{prefix}unblock (\d+)$": "unblock"
    }

    usage = [
        "Reply to somebody's message with {prefix} to block them.",
        "{prefix}block 12345: block by user id"
    ]

    def __init__(self):
        super().__init__()
        self.blocked_user_ids = []

    def pre_process(self, msg):
        if not hasattr(msg, 'text'):
            return

        # check if user addresses bot
        for plugin_info in self.bot.plugin_manager.getAllPlugins():
            if type(plugin_info.plugin_object.patterns) is dict:
                for pattern, func in plugin_info.plugin_object.patterns.items():
                    if plugin_info.plugin_object.is_activated and msg.text is not None:
                        pattern = pattern.replace("{prefix}", self.bot.pfx)
                        matches = re.search(pattern, msg.text)
                        if matches is not None:
                            uid = msg.src.id
                            if uid in self.blocked_user_ids:
                                raise AccessError("acces denied for {}".format(uid))
            elif  type(plugin_info.plugin_object.patterns) is list:
                for pattern in plugin_info.plugin_object.patterns:
                    if plugin_info.plugin_object.is_activated and msg.text is not None:
                        pattern = pattern.replace("{prefix}", self.bot.pfx)
                        matches = re.search(pattern, msg.text)
                        if matches is not None:
                            uid = msg.src.id
                            if uid in self.blocked_user_ids:
                                raise AccessError("acces denied for {}".format(uid))

    @auth.authorize(groups=['admins'])
    def block(self, msg, matches):
        print("block called")
        try:
            peer = msg.reply.src
            self.blocked_user_ids = list(set(self.blocked_user_ids + [peer.id]))
            return peer.send_msg("you're now blocked")
        except AttributeError:
            return "please reply to a fresh message to block"

    @auth.authorize(groups=['admins'])
    def block_by_id(self, msg, matches):
        print("block_by_id called")
        uid = int(matches.group(1))
        self.blocked_user_ids = list(set(self.blocked_user_ids + [uid]))
        return "blocked " + str(uid) 

    @auth.authorize(groups=['admins'])
    def unblock(self, msg, matches):
        uid = int(matches.group(1))
        if uid in self.blocked_user_ids:
            self.blocked_user_ids.remove(uid)
            msg.dest.send_msg("unblocked user")
        return

