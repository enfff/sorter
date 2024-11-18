import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Things will go here

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.open_button = Gtk.Button(label="Open")
        self.header.pack_start(self.open_button)

        self.open_button.set_icon_name("document-open-symbolic")

        self.open_dialog = Gtk.FileDialog.new()
        self.open_dialog.set_title("Select a File")

        # Commentato il filtro si aggiunge dopo
        # TOOD
        # file_filter = Gtk.FileFilter()
        # file_filter.set_name("Image files")
        # file_filter.add_mime_type("image/jpeg")
        # file_filter.add_mime_type("image/png")

        # filters = Gio.ListStore.new(Gtk.FileFilter)  # Create a ListStore with the type Gtk.FileFilter
        # filters.append(file_filter)  # Add the file filter to the ListStore. You could add more.

        # self.open_dialog.set_filters(filters)  # Set the filters for the open dialog
        # self.open_dialog.set_default_filter(file_filter)

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

        GLib.set_application_name("Sorter")

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about)
        self.add_action(action)
        
        menu.append("About", "win.about") 



        # Signals
        self.open_button.connect("clicked", self.show_open_dialog)


    
    def show_open_dialog(self, button):
        self.open_dialog.open(self, None, self.open_dialog_open_callback)
        
    
    def open_dialog_open_callback(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file is not None:
                print(f"File path is {file.get_path()}")
                # Handle loading file from here
        except GLib.Error as error:
            print(f"Error opening file: {error.message}")
    
    
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
        dialog.add_credit_section("Contributors", ["Name1 url"]) 
        dialog.set_translator_credits("Name1 url") 
        dialog.set_copyright("© 2022 developer") 
        dialog.set_developers(["Developer"]) 
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