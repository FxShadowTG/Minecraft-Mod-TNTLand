# -*- coding: utf-8 -*-
from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi


@Mod.Binding(name="TNTLandMod", version="0.0.1")
class TNTLandMod(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def TNTLandModServerInit(self):
        serverApi.RegisterSystem("TNTLandMod","TNTLandModServerSystem","TNTLandMod.TNTLandModServerSystem.TNTLandModServerSystem")
        print("服务注册成功")

    @Mod.DestroyServer()
    def TNTLandModServerDestroy(self):
        print("服务销毁成功")
        pass

    @Mod.InitClient()
    def TNTLandModClientInit(self):
        clientApi.RegisterSystem("FightMod","FightModClientSystem","FightMod.FightModClientSystem.FightModClientSystem")
        print("客户注册成功")

    @Mod.DestroyClient()
    def TNTLandModClientDestroy(self):
        print("客户销毁成功")
