from Rigid2D.App import *

def update(app):
    app.SceneManager.loadSceneContents()
    app.Camera.setToTarget()
    app.ObjectManager.Start()
    updateScripts(app)

pg.init()
info = pg.display.Info()
width, height = info.current_w, info.current_h

app = App("Python Palooza", width, height)
app.Renderer.createScreenTex()

# 0–1 RGBA — this is what glClearColor wants
app.clear_color = [0.2, 0.3, 0.3]

imgui.create_context()
impl = ImGuiGL()
imgui.get_io().display_size = (app.width, app.height)

test_Text = ""

showTest = True

def main():
    global showTest 
    global test_Text
    while app.running:


        # inside the loop, before you draw/upload the surface:
        rgb = (
            int(app.clear_color[0] * 255),
            int(app.clear_color[1] * 255),
            int(app.clear_color[2] * 255),
        )

        app.Renderer.display.fill(rgb)
        for event in app.getEvent():

            if event.type == pg.WINDOWMOVED:
                print("Yo")
            if event.type == pg.QUIT:
                app.running = False

            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_o):
                    showTest = True

                if (event.key == pg.K_ESCAPE):
                    app.running = False
                            
            app.updateWindowScale(event)
            impl.process_event(event)

        impl.process_inputs()
        imgui.new_frame()

        app.Renderer.clear(UColor4(0.2, 0.3, 0.3, 1.0))
        update(app)
        
        if (showTest):
            expanded, open = imgui.begin("Debug", True)

            if (not open):
                showTest = False

            clicked, index = imgui.combo("Scene", 0, app.SceneManager.Scenes)
            if clicked:
                app.SceneManager.setNewScene(app.SceneManager.Scenes[index])
            

            imgui.text(f"FPS: {app.fps:.7f}")
            imgui.label_text("objects", str(len(app.ObjectManager.objects))) 
            imgui.end()

        imgui.render()
        impl.render(imgui.get_draw_data())

        
        app.fps = app.clock.get_fps()
        app.deltaTime = app.clock.tick(app.targetFPS) / 1000.0
        app.input.update()
        pg.display.flip()

    impl.shutdown()


if __name__ == "__main__":
    try:
        main()
        app.quit()
    except Exception:
        import traceback
        traceback.print_exc()