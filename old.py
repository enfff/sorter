import gi
import sys
from pathlib import Path

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, Gio

IMAGE_DIR = Path.home() / "Downloads" / "Prova"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}

class ImageApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.example.ImageApp")

        
        self.connect("activate", self.on_activate)
        self.image_paths = list(IMAGE_DIR.iterdir())
        self.image_index = 0

    def on_activate(self, app):
        window = Adw.ApplicationWindow(application=app)
        window.set_title("Simple Image Viewer")
        window.set_default_size(800, 600)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)
        window.set_content(vbox)

        self.image_container = vbox
        self.picture = Gtk.Picture()

        # Create an EventControllerKey to handle key presses
        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self.on_key_press)
        window.add_controller(key_controller)

        window.present()

    def load_and_display_image(self):
        if self.image_index < len(self.image_paths):
            image_path = self.image_paths[self.image_index]
            self.display_image(self.image_container, image_path)
        else:
            print("No more images to display.")

    def display_image(self, container, image_path):
        try:
            file = Gio.File.new_for_path(str(image_path))
            texture = Gdk.Texture.new_from_file(file)
            # picture = Gtk.Picture.new_for_texture(texture)
            self.picture.set_paintable(texture)
            container.append(self.picture)

        except Exception as e:
            print(f"Failed to load image {image_path}: {e}")

    def on_key_press(self, controller, keyval, keycode, state):
        key = Gdk.keyval_name(keyval)
        if key == "n":  # Shortcut key 'n' for next image
            print("Next image shortcut pressed")
            self.image_index += 1
            self.load_and_display_image()

def main():
    Adw.init()
    app = ImageApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())