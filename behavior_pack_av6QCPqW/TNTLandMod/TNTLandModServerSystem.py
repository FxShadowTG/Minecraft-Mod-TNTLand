# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from math import floor
ServerSystem = serverApi.GetServerSystemCls()
factory = serverApi.GetEngineCompFactory()

class TNTLandModServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        print("服务器准备监听")
        self.ListenEvent()
        print("服务器监听完毕")
        self.playerIdList = []
        #获取levelId
        self.levelId = serverApi.GetLevelId()

    def ListenEvent(self):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddServerPlayerEvent", self, self.OnAddServerPlayerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerAttackEntityEvent", self, self.OnPlayerAttackEntityEvent)
        
    def OnPlayerAttackEntityEvent(self,args):
        compCreateItem = factory.CreateItem(args["playerId"])
        itemDict = compCreateItem.GetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        print(itemDict)
        if itemDict["newItemName"] == 'ggvcc:tnt_sword' and itemDict["newItemName"] != None:
            compCreateAttr = factory.CreateAttr(args["victimId"])
            compCreateAttr.SetEntityOnFire(1, 2)
            print("ok")
        
    def OnAddServerPlayerEvent(self,args):
        self.playerIdList.append(args["id"])

    def UpdatePlayerBlock(self):
        for playerId in self.playerIdList:
            compCreateDimension = factory.CreateDimension(playerId)
            dimension = compCreateDimension.GetEntityDimensionId()

            compCreatePos = factory.CreatePos(playerId)
            playerIdPos = compCreatePos.GetFootPos()

            playerIdPosX = round(floor((playerIdPos[0])),0)
            playerIdPosY = round(floor((playerIdPos[1])),0)
            playerIdPosZ = round(floor((playerIdPos[2])),0)

            blockDict = {
                'name': 'minecraft:tnt',
            }

            compCreateBlockInfo = factory.CreateBlockInfo(self.levelId)
            #脚下方块是否为空气/地狱传送/末地传送，是的话就不覆盖脚下
            currentPositionBlockDict = compCreateBlockInfo.GetBlockNew((playerIdPosX, playerIdPosY-1, playerIdPosZ), dimension)
            print(currentPositionBlockDict)
            if(currentPositionBlockDict["name"] != "minecraft:air"):
                if(currentPositionBlockDict["name"] == "minecraft:obsidian" or currentPositionBlockDict["name"] == "minecraft:end_portal" or currentPositionBlockDict["name"] == "minecraft:portal"):
                    continue
                compCreateBlockInfo.SetBlockNew((playerIdPosX, playerIdPosY-1, playerIdPosZ), blockDict, 0, dimension, True)

            #获取四周是否为空气，是的话就不覆盖
            currentPositionBlockDict = compCreateBlockInfo.GetBlockNew((playerIdPosX+1, playerIdPosY, playerIdPosZ), dimension)
            if(currentPositionBlockDict["name"] != "minecraft:air"):
                compCreateBlockInfo.SetBlockNew((playerIdPosX+1, playerIdPosY, playerIdPosZ), blockDict, 0, dimension, True)

            #获取四周是否为空气，是的话就不覆盖
            currentPositionBlockDict = compCreateBlockInfo.GetBlockNew((playerIdPosX-1, playerIdPosY, playerIdPosZ), dimension)
            if(currentPositionBlockDict["name"] != "minecraft:air"):
                compCreateBlockInfo.SetBlockNew((playerIdPosX-1, playerIdPosY, playerIdPosZ), blockDict, 0, dimension, True)

            #获取四周是否为空气，是的话就不覆盖（此面特殊，免疫紫地狱传送）
            currentPositionBlockDict = compCreateBlockInfo.GetBlockNew((playerIdPosX, playerIdPosY, playerIdPosZ+1), dimension)
            if(currentPositionBlockDict["name"] != "minecraft:air"):
                if(currentPositionBlockDict["name"] == "minecraft:portal"):
                    continue
                compCreateBlockInfo.SetBlockNew((playerIdPosX, playerIdPosY, playerIdPosZ+1), blockDict, 0, dimension, True)

            #获取四周是否为空气，是的话就不覆盖
            currentPositionBlockDict = compCreateBlockInfo.GetBlockNew((playerIdPosX, playerIdPosY, playerIdPosZ-1), dimension)
            if(currentPositionBlockDict["name"] != "minecraft:air"):
                compCreateBlockInfo.SetBlockNew((playerIdPosX, playerIdPosY, playerIdPosZ-1), blockDict, 0, dimension, True)


    # OnScriptTickServer的回调函数，会在引擎tick的时候调用，1秒30帧（被调用30次）
    def OnTickServer(self):
        pass

    # 这个Update函数是基类的方法，同样会在引擎tick的时候被调用，1秒30帧（被调用30次）
    def Update(self):
        self.UpdatePlayerBlock()
        pass

    def UnListenEvent(self):
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddServerPlayerEvent", self, self.OnAddServerPlayerEvent)

    def Destroy(self):
        self.UnListenEvent()
        pass
