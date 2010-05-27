import os
import simplejson as json
import threading
import logging

import ModulManager
import PluginManager

class root(object):

    def __init__(self):
        self.Event = threading.Event()

        ConfigFile = open("/home/robin/Labs/Python/Magic/usr/magic/config.json")
        self.config = json.load(ConfigFile)
        ConfigFile.close()
        
        self.ModulManager = ModulManager.NewModulManager(self)
        self.PluginManager = PluginManager.NewPluginManager(self)
        
        for ModulClass in self.config["ActiveClasses"]:
            self.StartModul(ModulClass)
            
        for ModulClass in self.config["ActiveClasses"]:
            self.PluginManager.StartClass(ModulClass)
   
   
    def StartModul(self, ModulClass):
        self.ModulManager.StartModul(ModulClass)
        self.PluginManager.StartClass(ModulClass)
   
    def GetModul(self, ModulClass):
        return self.ModulManager.GetModul(ModulClass)
        
    def CallHook(self, ModulClass, Hook, *args, **kwargs):
        self.PluginManager.CallHook(ModulClass, Hook, *args, **kwargs)
        
    def StartPlugin(self, ModulClass, PluginName):
        if ModulClass not in self.config["ActivePlugins"]:
            self.config["ActivePlugins"][ModulClass] = []
        if PluginName not in self.config["ActivePlugins"][ModulClass]:
            self.config["ActivePlugins"][ModulClass].append(PluginName)
        
        self.PluginManager.StartPlugin(ModulClass, PluginName)
        
    def StopPlugin(self, ModulClass, PluginName):
        if ModulClass in self.config["ActivePlugins"]:
            if PluginName in self.config["ActivePlugins"][ModulClass]:
                self.config["ActivePlugins"][ModulClass].remove(PluginName)
                
        self.PluginManager.StopPlugin(ModulClass, PluginName)
        
    def Wait(self):
        self.Event.wait()
        
    def Stop(self):
        if self.ModulManager.Stop():
            self.End()
    
    def End(self):
        self.PluginManager.End()
        self.ModulManager.End()
        self.Event.Set()
   
   
   
   
   
class tmp():
   
               

    def StartPlugin(self, ModulClass, PluginName):
        if ModulClass not in self.plugins:
            self.plugins[ModulClass] = {}
            
        if PluginName not in self.plugins[ModulClass]:
            exec("from magic.plugin." + str(ModulClass) + " import " + str(PluginName) + " as TmpPlugin")
            self.plugins[ModulClass][PluginName] = TmpPlugin.NewPlugin(self)
            
    def StopPlugin(self, ModulClass, PluginName):
        if ModulClass in self.plugins[ModulClass]:
            if PluginName in self.plugins[ModulClass]:
                del(self.plugins[ModulClass][PluginName])


    def CallHook(self, ModulClass, Hook, *args, **kwargs):
        if ModulClass in self.plugins:
            for Plugin in self.plugins[ModulClass]:
                try:
                    m = getattr(self.plugins[ModulClass][Plugin], Hook)
                    m(*args, **kwargs)
                except AttributeError:
                    pass
          
        
def NewRoot():
    return root()

