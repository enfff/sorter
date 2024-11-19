import os
import gi
import sys
from pathlib import Path

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, Gio, GLib

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}

# Used while developing to locate the GSettings schema
os.environ["GSETTINGS_SCHEMA_DIR"] = str(Path(__file__).resolve().parent)

# The reason the UI was hard coded is because the documentation for libadwaita is still in alpha.
# The use of blueprints is well advised but awful to use in practice.

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Can't get the Gsetting schema to work...
        self.image_index = 0
        self.image_paths = []
        self.buttons = {}

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
        self.hamburger.set_icon_name("open-menu-symbolic")

        self.header.pack_end(self.hamburger)

        self.open_folder_button.connect("clicked", self.show_open_dialog)

        self.container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.container)

        self.status_page = Adw.StatusPage()
        self.status_page.set_title("Welcome to Sorter")
        self.status_page.set_description("Choose a folder to start sorting images")
        self.status_page.set_icon_name("folder-pictures-symbolic")
        self.status_page.set_hexpand(True)
        self.status_page.set_vexpand(True)
        self.container.append(self.status_page)

        self.image_container = self.container
        self.picture_container = Gtk.Picture()
        self.picture_container.set_margin_top(10)  # Add top margin to the picture
        self.picture_container.set_margin_start(10)  # Add top margin to the picture
        self.picture_container.set_margin_end(10)  # Add top margin to the picture
        self.container.append(self.picture_container)

        # Create the action bar with buttons
        self.action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.action_bar.set_margin_top(10)
        self.action_bar.set_margin_bottom(10)
        self.action_bar.set_margin_start(10)
        self.action_bar.set_margin_end(10)
        self.action_bar.set_halign(Gtk.Align.CENTER)
        self.container.append(self.action_bar)

        self.create_action_button("Anomaly", "anomaly")
        self.create_action_button("Background", "background")
        self.create_action_button("Trash", "trash")

        action_anomaly = Gio.SimpleAction.new("anomaly", None)
        action_anomaly.connect("activate", lambda action, param: self.move_image_to_class(action, param, "anomaly"))
        self.add_action(action_anomaly)

        action_background = Gio.SimpleAction.new("background", None)
        action_background.connect("activate", lambda action, param: self.move_image_to_class(action, param, "background"))
        self.add_action(action_background)

        action_trash = Gio.SimpleAction.new("trash", None)
        action_trash.connect("activate", lambda action, param: self.move_image_to_class(action, param, "trash"))
        self.add_action(action_trash)

        self.update_button_states()
        self.connect("destroy", self.on_window_close)

        self.set_default_settings()


    def set_default_settings(self):
        self.settings = Gio.Settings.new("com.github.enfff.sorter")
        width = self.settings.get_int("window-width")
        height = self.settings.get_int("window-height")
        self.set_default_size(width, height)
        print("Default settings set")

    
    def create_action_button(self, label, action_name):
        button = Gtk.Button(label=label)
        if label == "Trash":
            button.get_style_context().add_class("destructive-action")
        button.connect("clicked", lambda btn: self.activate_action(action_name))
        self.action_bar.append(button)
        self.buttons[action_name] = button
            

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
        self.update_button_states()

        if self.image_paths:
            self.show_picture()
            self.load_and_display_image()
        else:
            self.show_status_page()

    def load_and_display_image(self):
        if self.image_index < len(self.image_paths):
            self.display_image(self.image_paths[self.image_index])
        else:
            self.show_status_page()
            self.image_paths = []
            print("No more images to display.")
            self.update_button_states()

    def display_image(self, image_path):
        try:
            file = Gio.File.new_for_path(str(image_path))
            texture = Gdk.Texture.new_from_file(file)
            self.picture_container.set_paintable(texture)
        except Exception as e:
            print(f"Failed to load image {image_path}: {e}")

    
    def show_status_page(self):
        self.status_page.show()
        self.picture_container.hide()
    
    def show_picture(self):
        self.status_page.hide()
        self.picture_container.show()

    def update_button_states(self):
        state = bool(self.image_paths)
        for button in self.buttons.values():
            button.set_sensitive(state)

    def move_image_to_class(self, action, parameter, class_name):
        """
            Moves the image to the correct subfolder, specified by the class-name.
            It's activated by pressing the shortcut keys associated with the action.
            Defaults
                - anomaly: a
                - background: b
                - trash: t
        """

        if self.image_index < len(self.image_paths):
            image_path = self.image_paths[self.image_index]
            class_folder = os.path.join(self.current_folder, class_name)
            
            if class_name == "trash":
                image_path.unlink()
            else:
                os.makedirs(class_folder, exist_ok=True)
                new_path = os.path.join(class_folder, image_path.name)
                image_path.rename(new_path)

            self.image_index += 1
            self.load_and_display_image()
    
    def on_window_close(self, window):
        width, height = window.get_size()
        self.settings.set_int("window-width", width)
        self.settings.set_int("window-height", height)
        return False

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.set_title("Sorter")
        # self.win.set_default_size(800, 600)
        # self.win.set_size_request(400, 440)  # Set minimum size (width, height)
        
        self.set_accels_for_action("win.anomaly", ["a"])
        self.set_accels_for_action("win.background", ["b"])
        self.set_accels_for_action("win.trash", ["t"])
        self.set_accels_for_action("win.quit", ["<super>t"])
        
        self.win.present()


def main():
    Adw.init()
    app = MyApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())