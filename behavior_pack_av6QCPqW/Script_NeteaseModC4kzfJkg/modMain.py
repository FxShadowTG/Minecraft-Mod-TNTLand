# -*- coding: utf-8 -*-

from mod.common.mod import Mod


@Mod.Binding(name="Script_NeteaseModC4kzfJkg", version="0.0.1")
class Script_NeteaseModC4kzfJkg(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def Script_NeteaseModC4kzfJkgServerInit(self):
        pass

    @Mod.DestroyServer()
    def Script_NeteaseModC4kzfJkgServerDestroy(self):
        pass

    @Mod.InitClient()
    def Script_NeteaseModC4kzfJkgClientInit(self):
        pass

    @Mod.DestroyClient()
    def Script_NeteaseModC4kzfJkgClientDestroy(self):
        pass
