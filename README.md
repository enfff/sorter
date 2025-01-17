# Sorter

App to sort images in user-defined classes, useful for classifying AI-generated images for Computer Vision tasks

![Preview](media/app-preview.gif)

**TODO**
- Generalize to any class
- Load preferred settings
- Log statistics

# Development

Starting from this repo root, execute

  export GSETTINGS_SCHEMA_DIR = $(pdw)

then

  python3 sorter.py

This program requires a working GTK environment. If missing, install it according to your distribution needs. In WSL2, use the following instructions

  sudo apt install libgtk-4-dev libadwaita-1-dev

and then install the libraries in requirements.txt

  pip3 install -r requirements.txt


### Issues to fix

``` bash
sorter.py:122: DeprecationWarning: Gtk.StyleContext.add_class is deprecated
  button.get_style_context().add_class("destructive-action")
  
sorter.py:177: DeprecationWarning: Gtk.Widget.hide is deprecated
  self.status_page.hide()

sorter.py:178: DeprecationWarning: Gtk.Widget.show is deprecated
  self.picture_container.show()
```

### Sources
- [Folder picker](https://www.reddit.com/r/GTK/comments/16mv5fl/unsure_how_to_use_gtkfiledialog_to_return_the/)
- [Add shortcuts](https://www.reddit.com/r/GTK/comments/utesgp/quit_doesnt_work_in_gtk4_with_python/)