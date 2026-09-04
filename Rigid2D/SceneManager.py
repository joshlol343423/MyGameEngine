from Rigid2D.Utilities.util import *
from Rigid2D.Utilities.math import *
from Rigid2D.Utilities.Engine import *

class SceneManager:
    def __init__(self,app):
        self.app = app
        self.sceneLoaded = False

        self.Scene = "Scene1"

        self.Scenes = os.listdir("Scenes")

    def setSceneList(self):
        self.Scenes = os.listdir("Scenes")

    def createScene(name):
        pass

    def setNewScene(self, Scene):
        if (self.Scene == Scene): return 
        self.Scene = Scene
        self.app.resetScripts()
        self.app.ObjectManager.objects = []
        self.sceneLoaded = False

    def createNewScenePath(self) -> str:
        path = os.path.join("Scenes", self.Scene)
        path = os.path.abspath(path)
        return path
    
    def loadSceneContents(self) -> None:
        if self.sceneLoaded: return
        try:
            start = time.time()
            path = self.createNewScenePath()
            
            with open(getFile(path, "Objects.json"), "r") as file:
                objectData = json.load(file)

            with open(getFile(path, "BackGround.json"), "r") as file:
                bgData = json.load(file)

            with open(getFile(path, "Camera.json"), "r") as file:
                camearData = json.load(file)

            print(f"Scene data fetch was successful\n")
            self.app.color = (
                bgData["Color"][0],
                bgData["Color"][1],
                bgData["Color"][2]
            )

            self.app.Camera.target = camearData["Target"]
            self.app.Camera.camera_scale = camearData["Zoom"]
            
            for Obj in objectData["Objects"]:
                texture = Obj["Texture"]
                size = Vector2(Obj["Size"]["w"], Obj["Size"]["h"])
                pos = Vector2(Obj["Position"]["x"], Obj["Position"]["y"])
                rect = Vector2(Obj["RectSize"]["w"], Obj["RectSize"]["h"])
                rotation = Obj["Rotation"]
                name = Obj["Name"]

                gameObj = GameObject(self.app)
                gameObj.Name = name
                gameObj.Position = pos
                gameObj.Size = size
                gameObj.Rotation = rotation
                gameObj.CanCollide = Obj["CanCollide"]
                gameObj.Anchored = Obj["Anchored"]
                gameObj.Id = Obj["ID"]
                gameObj.RectSize = rect
                gameObj.Transparency = Obj["Transparency"]
                gameObj.setObjectTexture(texture)
                gameObj.start()

                print(f"Game Object {gameObj.Name} was successfully created")
            
            print(f"All Game Objects were created\n")
            self.scripts = os.path.abspath(os.path.join("Scenes", self.Scene, "Scripts"))
            
            if os.path.exists(self.scripts):
                for script in os.listdir(self.scripts):
                    if script == "__pycache__": continue
                    self.app._addScripts(self.scripts,script)
                    print(f"Script Fetched: {script}")

            print(f"All Scripts successfully Fetched\n")
            
            end = time.time()
            print(f"Scene Fully Loaded. Time: {end - start} sec \n")
     
            self.sceneLoaded = True
        except Exception as e:
            print("Engine Error Scene Failed To Load: ", e)
            traceback.print_exc()
