#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Class show to a GTK4+ window with a treeview control.
'''

import sys
# Import Gtk4 libraries.
try:
    import gi
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Gdk, Adw, Gio, GLib
    # from gi.repository import GdkPixbuf
except:
    print(f"GTK4 Not Available. ({__file__})")
    sys.exit(0)
import os
import subprocess
import shutil
import datetime

# Application libraries.



class MainWindow(Gtk.ApplicationWindow):
    '''
    Class to represent the main window for the rename program.

    :ivar Gtk.Builder builder: The GTK+ builder for the dialog.
    :ivar Gtk.Window window: The actual GTK+ window.
    '''



    def __init__(self, myArgs, *args, **kwargs):
        '''
        Class constructor for the :py:class:`MainWindow` class.

        :param object args: The program arguments.
        '''
        self.args = myArgs
        super().__init__(*args, **kwargs)
        self.set_title('Treeview GTK4')
        self.set_default_size(600, 250)

        # Add a liststore
        self.liststoreFiles = Gtk.ListStore(str)

        # Add a vertical box.
        self.boxMain = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        #self.boxMain.set_spacing(10)
        #self.boxMain.set_margin_top(10)
        #self.boxMain.set_margin_bottom(100)
        #self.boxMain.set_margin_start(10)
        #self.boxMain.set_margin_end(10)
        #self.boxMain.set_vexpand(True)
        self.boxMain.set_halign(Gtk.Align.FILL)
        self.boxMain.set_valign(Gtk.Align.FILL)
        self.set_child(self.boxMain)

        # Add a horizontal box.
        self.boxDetails = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        # self.boxDetails.set_css_classes(['border'])
        self.boxMain.append(self.boxDetails)

        # Add a scrolled window.
        self.scrolledFiles = Gtk.ScrolledWindow()
        self.scrolledFiles.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        # self.scrolledFiles.set_vexpand(True)
        #self.scrolledFiles.set_halign(Gtk.Align.FILL)
        #self.scrolledFiles.set_valign(Gtk.Align.FILL)
        self.scrolledFiles.set_css_classes(['border'])

        # Add a TreeView.
        self.treeviewFiles = Gtk.TreeView(model=self.liststoreFiles)
        self.treeviewFiles.set_vexpand(True)
        # self.treeviewFiles.set_css_classes(['border'])

        # Add a column.
        cell = Gtk.CellRendererText()
        self.treeviewColumnFileName = Gtk.TreeViewColumn('File', cell, text=0)
        self.treeviewFiles.append_column(self.treeviewColumnFileName)
        self.scrolledFiles.set_child(self.treeviewFiles)
        self.boxDetails.append(self.scrolledFiles)

        # When a row of the treeview is selected send a signal.
        self.selection = self.treeviewFiles.get_selection()
        self.selection.connect('changed', self._treeSelectionChanged)

        # Add a label.
        self.labelSelection = Gtk.Label(label="Goodbye World.")
        self.labelSelection.set_css_classes(['labeltext', 'border'])
        #self.labelSelection.set_halign(Gtk.Align.FILL)
        #self.labelSelection.set_valign(Gtk.Align.FILL)
        self.labelSelection.set_hexpand(True)
        self.boxDetails.append(self.labelSelection)

        # Create a header bar.
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)


        # Create new actions.
        action = Gio.SimpleAction.new('something', None)
        action.connect('activate', self.actionSomething)
        self.add_action(action)
        action = Gio.SimpleAction.new('about', None)
        action.connect('activate', self.actionAbout)
        self.add_action(action)

        # Create a new menu, containing the simple actions.
        menu = Gio.Menu.new()
        menu.append('Do Something', 'win.something')
        menu.append('About', 'win.about')

        # Create a popover.
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        # Create a menu button.
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name('open-menu-symbolic')

        # Add menu button to the header bar.
        self.header.pack_start(self.hamburger)

        # Set application name.
        GLib.set_application_name('Treeview GTK4')

        # Add a button into the header bar.
        self.openButton = Gtk.Button(label='Open')
        # Default icons at /usr/share/icons/Adwaita/...
        self.openButton.set_icon_name('document-open-symbolic')
        # self.openButton.set_icon_name('folder')
        self.openButton.connect('clicked', self._fileOpen)
        self.header.pack_start(self.openButton)

        # Initialise the dialog.
        self.folderName = os.path.dirname(os.path.realpath(__file__))
        self.scanFolder()



    def helloClicked(self, button):
        print('Hello World')
        self.labelSelection.set_label("Hello World.")
        myText = self.labelSelection.get_label()
        print(f'{myText=}')
        self.labelSelection.set_text("Hello")
        myText = self.labelSelection.get_text()
        print(f'{myText=}')



    def actionSomething(self, action, param):
        print('Something is done.')



    def actionAbout(self, action, param):
        dialog = Adw.AboutWindow(transient_for=self)
        dialog.set_application_name("GTK TreeView Example")
        dialog.set_version("1.0")
        dialog.set_developer_name("Developer")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_comments("An example GTK program.")
        dialog.set_website("https://docs.gtk.org/gtk4/")
        dialog.set_issue_url("https://docs.gtk.org/gtk4/")
        dialog.add_credit_section("Contributors", ["Name1 url", "Name2 url"])
        dialog.set_translator_credits("Name1 url")
        dialog.set_copyright("© 2024 Developer")
        dialog.set_developers(["Developer"])
        dialog.set_application_icon("com.github.devname.appname") # icon must be uploaded in ~/.local/share/icons or /usr/share/icons

        dialog.set_visible(True)



    def _treeSelectionChanged(self, treeSelection):
        ''' Signal handler for the selection on tree changing. '''
        selection = ''

        # liststoreFiles = self.builder.get_object('liststoreFiles')
        liststoreFiles = self.liststoreFiles
        mode = treeSelection.get_mode()
        if mode == Gtk.SelectionMode.SINGLE or mode == Gtk.SelectionMode.BROWSE:
            model, treeIter = treeSelection.get_selected()
            if treeIter is not None:
                fileName = liststoreFiles.get_value(treeIter, 0)
                selection = fileName
        elif mode == Gtk.SelectionMode.MULTIPLE:
            model, pathList = treeSelection.get_selected_rows()

            for path in pathList:
                treeIter = liststoreFiles.get_iter(path)
                fileName = liststoreFiles.get_value(treeIter, 0)
                if selection == '':
                    selection = fileName
                else:
                    selection = '{}\n{}'.format(selection, fileName)

        # Display the filename.
        # labelSelection = self.builder.get_object('labelSelection')
        self.labelSelection.set_text(selection)



    def _fileRefresh(self, widget):
        ''' Signal handler for the 'File' → 'Refresh' menu point. '''
        self.scanFolder()



    def _fileOpen(self, widget):
        ''' Signal handler for the 'File' → 'Open' menu point. '''
        # Create a folder chooser dialog.
        print('_fileOpen() Start')
        dialog = Gtk.FileChooserDialog(title = 'Select Source Folder', transient_for=self, action=Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.add_buttons(("_Cancel"), Gtk.ResponseType.CANCEL, ("_Open"), Gtk.ResponseType.ACCEPT)
        dialog.connect('response', self.fileChooserDialogCallBack)

        dialog.set_default_response(Gtk.ResponseType.OK)
        dialog.set_modal(True)

        # Set the current source as the initial value for the dialog if not empty.
        # dialog.set_current_folder(self.folderName)

        # Display the file chooser dialog.
        response = dialog.present()
        print(f'{response=}')

        # Close the file chooser dialog.
        # dialog.destroy()
        print('_fileOpen() Finished')



    def fileChooserDialogCallBack(self, dialog, result):
        ''' Signal handler for the open file chooser dialog responding. '''
        # print(f'{result=}')
        if result == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            if file is not None:
                self.folderName = file.get_path()
                self.scanFolder()

        dialog.destroy()



    def _fileQuit(self, widget):
        ''' Signal handler for the 'File' → 'Quit' menu point. '''
        # Close the main window and hence exit the Gtk loop.
        self.window.destroy()



    def _viewOpenFolder(self, widget):
        ''' Signal handler for the 'View' → 'Open Folder' menu point. '''
        subprocess.Popen(['xdg-open', self.folderName])



    def scanFolder(self):
        ''' Scan the images in the specified folder. '''
        # liststoreFiles = self.builder.get_object('liststoreFiles')
        liststoreFiles = self.liststoreFiles
        if liststoreFiles is None:
            print('Error: Can\'t find liststoreFiles in builder.')
            return
        liststoreFiles.clear()
        try:
            everyThing = os.listdir(self.folderName)
        except:
            everyThing = []

        everyThing.sort()

        count = 0
        for theFile in everyThing:
            fileName, extension = os.path.splitext(theFile)
            extension = extension.lower()
            if True:
                count += 1
                iterFiles = liststoreFiles.append()
                liststoreFiles.set(iterFiles, 0, theFile)

        self.treeviewColumnFileName.set_title(f'Files ({count})')



class TreeViewApp(Adw.Application):



    def __init__(self, myArgs, **kwargs):
        self.args = myArgs
        super().__init__(**kwargs)

        # An initial message.
        print('GTK+ Version {}.{}.{} (expecting GTK+4).'.format(Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version()))

        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path('gtk4/style.css')
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.connect('activate', self.onActivate)




    def onActivate(self, app):
        ''' Create the main window. '''
        self.window = MainWindow(self.args, application=app)
        self.window.present()



