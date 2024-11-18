import os
import gi
import sys
from pathlib import Path

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, Gio, GLib

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        GLib.set_application_name("Sorter")

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.open_folder_button = Gtk.Button(label="Open")
        self.header.pack_start(self.open_folder_button)

        self.open_folder_button.set_icon_name("document-open-symbolic")

        self.open_dialog = Gtk.FileDialog()
        self.open_dialog.set_title("Select a folder")

        # Create a new "Action"
        action = Gio.SimpleAction.new("something", None)
        self.add_action(action)  # Here the action is being added to the window, but you could add it to the
                                 # application or an "ActionGroup"

        # Create a new menu, containing that action
        menu = Gio.Menu.new()
        # menu.append("Do Something", "win.something")  # Or you would do app.something if you had attached the
                                                      # action to the application

        self.popover = Gtk.PopoverMenu()  # Create a new popover menu
        self.popover.set_menu_model(menu)

        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")  # Give it a nice icon

        self.header.pack_start(self.hamburger)

        self.open_folder_button.connect("clicked", self.show_open_dialog)

        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(container)

        self.status_page = Adw.StatusPage()
        self.status_page.set_title("Welcome to Sorter")
        self.status_page.set_description("Choose a folder to start sorting images")
        self.status_page.set_icon_name("folder-pictures-symbolic")
        self.status_page.set_hexpand(True)
        self.status_page.set_vexpand(True)
        container.append(self.status_page)

        # Default values
        self.class_shortcuts = {
            "anomaly": "a",
            "background": "b",
            # "trash": "t"
        }

        self.image_container = container
        self.picture = Gtk.Picture()
        container.append(self.picture)

        # Create the action bar with buttons
        self.action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.action_bar.set_margin_top(10)
        self.action_bar.set_margin_bottom(10)
        self.action_bar.set_margin_start(10)
        self.action_bar.set_margin_end(10)
        container.append(self.action_bar)

        self.create_action_button("Anomaly", "anomaly")
        self.create_action_button("Background", "background")
        self.create_action_button("Trash", "trash")

        # Set up actions for each class
        self.add_action(Gio.SimpleAction.new("anomaly", None))
        self.add_action(Gio.SimpleAction.new("background", None))
        self.add_action(Gio.SimpleAction.new("trash", None))

    
    
    def create_action_button(self, label, action_name):

        button = Gtk.Button(label=label)

        if label == "Trash":
            button.get_style_context().add_class("destructive-action")
        
        button.connect("clicked", lambda btn: self.activate_action(action_name))
        self.action_bar.append(button)
        
    

    def create_action_buttons(self):
        for class_name, shortcut in self.class_shortcuts.items():
            button = Gtk.Button(label=class_name.capitalize())
            button.connect("clicked", lambda btn, name=class_name: self.activate_action(name))
            self.action_bar.append(button)

    def show_open_dialog(self, button):
        dialog = Gtk.FileDialog()

        def on_select(dialog, result):
            try:
                folder = dialog.select_folder_finish(result)
                print(f"Selected folder: {folder.get_path()}")
                self.current_folder = folder.get_path()
                self.load_images_from_folder(folder.get_path())
            except Gtk.DialogError:
                # user cancelled or backend error
                pass

        dialog.select_folder(self, None, on_select)

    def load_images_from_folder(self, folder_path):
        self.image_paths = [p for p in Path(folder_path).iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS]
        self.image_index = 0
        if self.image_paths:
            self.show_picture()
            self.load_and_display_image()
        else:
            self.show_status_page()

    def load_and_display_image(self):
        if self.image_index < len(self.image_paths):
            image_path = self.image_paths[self.image_index]
            self.display_image(image_path)
        else:
            self.show_status_page()
            print("No more images to display.")

    def display_image(self, image_path):
        try:
            file = Gio.File.new_for_path(str(image_path))
            texture = Gdk.Texture.new_from_file(file)
            self.picture.set_paintable(texture)
        except Exception as e:
            print(f"Failed to load image {image_path}: {e}")

    
    def show_status_page(self):
        self.status_page.show()
        self.picture.hide()

    
    def show_picture(self):
        self.status_page.hide()
        self.picture.show()


    def move_image_to_class(self, class_name):
        if self.image_index < len(self.image_paths):
            image_path = self.image_paths[self.image_index]
            class_folder = os.path.join(self.current_folder, class_name)
            class_folder.mkdir(exist_ok=True)
            new_path = class_folder / image_path.name
            image_path.rename(new_path)
            print(f"Moved {image_path} to {new_path}")
            self.image_index += 1
            self.load_and_display_image()

    def on_key_press(self, controller, keyval, keycode, state):
        key = Gdk.keyval_name(keyval)
        if key == "n":  # Shortcut key 'n' for next image
            print("Next image shortcut pressed")
            self.image_index += 1
            self.load_and_display_image()

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.set_title("Sorter")
        self.win.set_default_size(800, 600)
        self.win.set_size_request(400, 400)  # Set minimum size (width, height)
        self.win.present()

def main():
    Adw.init()
    app = MyApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())