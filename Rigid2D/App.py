from Rigid2D.Utilities.util import *
from Rigid2D.Utilities.math import *
from Rigid2D.Utilities.Engine import *

from Rigid2D.SceneManager import *
from Rigid2D.ObjectManager import *
from Rigid2D.Camera import *
from Rigid2D.Physics import *
from Rigid2D.Renderer import *
import pygame as pg


scripts = []
loadedScripts = []

scriptInstances = []
moduleInstances = []

ModuleScripts = []

scriptsLoaded = False
modScriptsLoaded = False
scriptsStarted = False

def getScriptsFolder(app):
    scene = app.SceneManager.Scene
    return f"Scenes/{scene}/Scripts"

def loadModScripts(app):
    global modScriptsLoaded
    global ModuleScripts 

    if modScriptsLoaded: return
    path = os.path.abspath(os.path.join("ModuleScripts"))
    modList = os.listdir(path)

    for mod in modList:
        if mod == "__pycache__": continue
        
        path = os.path.abspath(os.path.join("ModuleScripts", mod))
        name = os.path.basename(path)[:-3]

        spec = importlib.util.spec_from_file_location(name, path)

        if spec is None:
            print("Could not load:", path)
            continue

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, name):
            print(f"{name} class not found in {path}")
            continue

        scriptClass = getattr(module, name)

        moduleInstances.append(scriptClass(app))

        print(f"Module Loaded Successfully: {name}")

    print("All Modules Loaded Successfully\n")
    
    modScriptsLoaded = True

def loadScripts(app):
    global scriptsLoaded
    global scripts
    global loadedScripts

    if scriptsLoaded: return
    
    for script in scripts:
        
        path = os.path.abspath(os.path.join(getScriptsFolder(app), script))
        
        name = os.path.basename(path)[:-3]

        spec = importlib.util.spec_from_file_location(name, path)

        if spec is None:
            print("Could not load:", path)
            continue

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, name):
            print(f"{name} class not found in {path}")
            continue

        scriptClass = getattr(module, name)

        loadedScripts.append(scriptClass)
        print(f"Scripts Loaded Successfully: {name}")
    
    print("All Scripts Loaded Successfully\n")

    scriptsLoaded = True

def runScripts(app):

    global scriptsStarted
    global scriptInstances
    global loadedScripts

    if not scriptsStarted:
        for scriptClass in loadedScripts:
            
            try:
                instance = scriptClass(app)
                scriptInstances.append(instance)
                print(f"Script Initzialized {instance}")
            except Exception as e:
                print(f"Engine Error Script Initialization Failed: {e}")
            
        print("All Scripts Initalized\n")
        scriptsStarted = True

    for script in scriptInstances:
        try:
            script.update(app.deltaTime)
        except Exception as e:
            print(f"Engine Error Script Failed To Run: {e}")

def updateScripts(app):
    
    loadScripts(app)
    runScripts(app)  

class App:

    def __init__(self, name, width, height):
        pg.init()
        pg.mixer.init()

        self.projectName = name

        self.initialWidth = width
        self.initialHeight = height

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, 
            pg.GL_CONTEXT_PROFILE_CORE
            )

        self.window = pg.display.set_mode( (width, height),pg.OPENGL | pg.DOUBLEBUF | pg.FULLSCREEN)
        pg.display.set_caption(self.projectName)

        self.width = width
        self.height = height

        self.worldScaleWidth = self.width/self.initialWidth
        self.worldScaleHeight = self.height/self.initialHeight

        self.worldScaleFactor = 100

        self.SceneManager = SceneManager(self)
        self.ObjectManager = ObjectManagerClass(self)
        self.Camera = Camera(self)
        self.Physics = Physics(self)
        self.Renderer = Renderer(self)
        self.input = Input()

        self.deltaTime = 0
        self.fps = 0
        self.targetFPS = 80
        self.clock = pg.time.Clock()
                
        self.running = True  
        self.projectPath = None

        self.rect_mesh = self.Renderer.createRectMesh()
        self.shaderProgram_Objects = self.Renderer.createShaderProgram("Rigid2D/Shaders/ObjectShaders/vert.vert","Rigid2D/Shaders/ObjectShaders/frag.frag")
        self.shaderProgram_Screen = self.Renderer.createShaderProgram("Rigid2D/Shaders/ScreenShaders/vert.vert", "Rigid2D/Shaders/ScreenShaders/frag.frag")

        self.Renderer.tex = glGetUniformLocation(self.shaderProgram_Screen, "uTex")
        self.Renderer.createRectUniforms()
        glViewport(0, 0, width, height)

        self.mod = loadModScripts

    def updateWindowScale(self, event): 
        if event.type == pg.VIDEORESIZE:

            self.Renderer.display = pg.surface.Surface(
                (event.w, event.h)
            )

            self.width = event.w
            self.height = event.h

            self.worldScaleWidth = self.width/self.initialWidth
            self.worldScaleHeight = self.height/self.initialHeight

    def _addScripts(self,path, script):
        scripts.append(os.path.join(path, script)) 

    def GetModule(self, name):
        global moduleInstances
        for mod in moduleInstances:      
            if mod.__class__.__name__ == name:
                return mod
        return None

    def getWindowSize(self):
        return Vector2(self.width, self.height)

    def getWorldScale(self):
        return Vector2(self.worldScaleWidth, self.worldScaleHeight)

    def getEvent(self):
        return pg.event.get()

    def getWindowInfo(self):
        info = pg.display.Info()
        return info

    def resetScripts(self):
        global scriptsLoaded
        global scripts
        global loadedScripts
        global scriptsStarted
        global scriptInstances

        scripts = []
        loadedScripts = []

        scriptInstances = []

        scriptsLoaded = False
        scriptsStarted = False
            
    def quit(self):
        pg.quit()
        print("The exit was successful")

    