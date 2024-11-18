import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio


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

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about)
        self.add_action(action)
        
        menu.append("About", "win.about") 


        # Signals
        self.open_folder_button.connect("clicked", self.show_open_dialog)

    
    def show_open_dialog(self, button):
        dialog = Gtk.FileDialog()

        def on_select(dialog, result):
            try:
                folder = dialog.select_folder_finish(result)
                # print(f"Selected folder: {folder.get_path()}")
                self.load_images_from_folder(folder.get_path())
            except Gtk.DialogError:
                # user cancelled or backend error
                pass

        dialog.select_folder(self, None, on_select)

    
    def load_images_from_folder(self, folder_path):
        # self.image_paths = [p for p in Path(folder_path).iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS]
        # self.image_index = 0
        # self.load_and_display_image()

        print(f"{folder_path = }")
    
    
    def show_about(self, action, param):
        # Deprecrated method sorry no time to fix it.

        dialog = Adw.AboutWindow(transient_for=app.get_active_window()) 
        dialog.set_application_name("Sorter") 
        dialog.set_version("1.0") 
        dialog.set_developer_name("enfff") 
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0)) 
        dialog.set_comments("Adw about Window example") 
        dialog.set_website("https://github.com/enfff/jackal-watch/") 
        dialog.set_issue_url("https://github.com/enfff/jackal-watch/issues") 
        dialog.add_credit_section("Contributors", ["Francesco Paolo Carmone https://github.com/enfff"]) 
        # dialog.set_translator_credits("Name1 url") 
        # dialog.set_copyright("© 2024 Reply") 
        dialog.set_developers(["enfff"]) 
        # dialog.set_application_icon("com.github.enfff.jackal-watch") # icon must be uploaded in ~/.local/share/icons or /usr/share/icons
        dialog.set_visible(True)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.set_title("Sorter")
        self.win.set_default_size(800, 600)
        self.win.present()

app = MyApp(application_id="com.github.enfff.sorter")
app.run(sys.argv)