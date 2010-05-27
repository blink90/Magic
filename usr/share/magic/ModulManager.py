import os
import simplejson as json
class ModulManager(object):

    def __init__(self, root):
        self.root = root
        self.module = {}
        self.manifests = {}
        
        self.LoadManifests()
        
    def StartModul(self, ModulClass):
        if ModulClass not in self.module:
            if self._RequirementsMatched(ModulClass):
                exec("from magic.modul import " + str(self.root.config["ClassToModul"][ModulClass]) + " as TmpModul")
                self.module[ModulClass] = TmpModul.NewModul(self)
            else:
                logging.log(logging.ERROR, "Die Modul Class " + ModulClass + " (" + self.root.config["ClassToModul"][ModulClass] +") konnte nicht gestartet werden, abhangigkeiten nicht gestartet werden")

    def _RequirementsMatched(ModulClass):
        if self.root.config["ClassToModul"][ModulClass] in self.manifests:
            if "requires" in self.manifests[self.root.config["ClassToModul"][ModulClass]]:
                for RequiredClass in self.manifest[self.root.config["ClassToModul"][ModulClass]]["requires"]:
                    if RequiredClass not in self.root.config["ActiveClasses"]:
                        logging.log(logging.ERROR, "Die Modul Classe " + RequiredClass + " wird von " + ModulClass + " benotigt und ist nicht aktiv..")
                        return False
        return True          
            
        
    def GetModul(self, ModulClass):
        if ModulClass not in self.module:
            self.StartModul(ModulClass)
        return self.module[ModulClass]
        
    def Stop(self):
        pass
    
    def End(self):
        pass

    
class tem():
        self.root = root
        self.manifests = {}
        self.module = {}
        self.classes = {}
        
        self.ModulStartList = ()

        ConfigFile = open("/home/robin/Labs/Python/Magic/usr/magic/config.json")
        self.Config = json.load(ConfigFile)
        ConfigFile.close()
        
        self.LoadManifests("/home/robin/Labs/Python/Magic/magic/modul")
        
        for ActiveClass in self.root.config["ActiveClasses"]:
            self.LoadModul(self.root.config["ClassToModul"][ActiveClass]))
        
        
    def LoadModul(self, ModulName):
        self.StartList = []
        self.StartList.append(ModulName)
        if self._RequirementsMatched(ModulName):
            if self._LoadModule(StartList):
                self._StartModule(StartList)
        self.StartList = []
        
    def GetModul(ClassName):
        if ClassName not in self.module:
            self.LoadModul(self.root.config["ClassToModul"][ClassName])
        if ClassName in self.module:
            return self.module[ClassName]  
 
#helper funktionen    
    def LoadManifests(self, path):
        for x in os.listdir(path):
            if os.path.isfile(path + "/" + x + "/manifest"):
                ManifestFile = open(path + "/" + x + "/manifest", "r")
                self.manifests[x] = json.loads(ManifestFile)
                ManifestFile.close()
                
        for manifest in self.manifests:
            #self.classes["gui"]["0"]["01"] = ("gtk")
            for ClassName in manifest["classes"]:
                if ClassName not in self.classes:
                    self.classes[ClassName] = {}
                for version in manifest["classes"][ClassName]:
                    v, vsub = version.split(".")
                    if v not in self.classes[ClassName]:
                        self.classes[ClassName][v] = {}
                        
                    if vsub not in self.classes[ClassName][v]:
                        self.classes[ClassName][v][vsub] = []
                        
                    self.classes[ClassName][v][vsub].append(manifest["name"])
            
       
    def _RequirementsMatched(ModulName):
        self.StartList.append(ModulName)
        if "requires" in self.manifest[ModulName]:
            for ModulClass in self.manifest[ModulName]["requires"]:
                if ModulClass == "gui":
                    if self.root.config["gui"] != self.manifest[ModulName]["requires"][ModulClass]:
                        print "Gui nicht kompatibel(eingestellt)"
                        return False
                else:
                    version = self.manifest[ModulName]["requires"][ModulClass]
                    if ModulClass not in self.root.config["ClassToModul"]:
                        return False
                    
                    if ModulClass not in self.manifest[self.root.config["ClassToModul"][ModulClass]]["classes"]:
                        return False
                        
                    version_available = self.manifest[self.root.config["ClassToModul"][ModulClass]]["classes"][ModulClass]
                    
                    v, vsub = version.split(".")
                    for x in version_available:
                        x1, x2 = x.split(".")
                        if v == x1:
                            if v <= x2:
                                if self._RequirementsMatched(self.root.config["ClassToModul"][ModulClass]):
                                    return True
                    return False
        else:
            return True
            
    def _LoadModule(self, StartList):
        for ModulName in StartList:
            if ModulName not in self.module:
                exec("from magic.modul import " + str(ModulName) + " as TmpModul")
                self.module[ModulName] = TmpModul.NewModul(self)
        
    def _StartModule(self, StartList):
        for ModulName in StartList:
            if ModulName not in self.module:
                if ModulName not in self.ModulStartList
                    self.ModulStartList.append(ModulName)
                    self.module[ModulName].Start()
    
    def End(self):
        for modul in self.module:
            try:
                return modul.End()
            except AttributeError:
                pass
    
    def Stop(self):
        for modul in self.module:
            try:
                modul.Stop()
            except AttributeError:
                pass
                
    def StopModul(self, ModulName):
        self.module[ModulName].Stop()
          
            
        
def NewModulManager(root):
    return  ModulManager(root)
