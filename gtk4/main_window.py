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
    from gi.repository import Gtk, Adw, Gio, GLib
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



    def __init__(self, *args, **kwargs):
        '''
        Class constructor for the :py:class:`MainWindow` class.

        :param object args: The program arguments.
        '''
        super().__init__(*args, **kwargs)
        self.set_title('Treeview GTK4')
        self.set_default_size(600, 250)

        # Add a liststore
        self.liststoreFiles = Gtk.ListStore(str)

        iterFiles = self.liststoreFiles.append()
        self.liststoreFiles.set(iterFiles, 0, 'Hello')
        iterFiles = self.liststoreFiles.append()
        self.liststoreFiles.set(iterFiles, 0, 'World')

        # Add a vertical box.
        self.boxMain = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.boxMain)

        # Add a horizontal box.
        self.boxDetails = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.boxMain.append(self.boxDetails)

        # Add a button.
        #self.button = Gtk.Button(label="Hello")
        #self.boxDetails.append(self.button)
        #self.button.connect('clicked', self.helloClicked)

        # Add a TreeView
        self.treeviewFiles = Gtk.TreeView(model=self.liststoreFiles)

        # Add a column,
        cell = Gtk.CellRendererText()
        self.treeviewColumnFileName = Gtk.TreeViewColumn('File', cell, text=0)
        self.treeviewFiles.append_column(self.treeviewColumnFileName)
        self.boxDetails.append(self.treeviewFiles)

        # When a row of the treeview is selected send a signal.
        self.selection = self.treeviewFiles.get_selection()
        self.selection.connect('changed', self._treeSelectionChanged)

        # Add a label.
        self.labelSelection = Gtk.Label(label="Goodbye World.")
        self.boxDetails.append(self.labelSelection)

        # Create a header bar.
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        # Add a button into the header bar.
        self.openButton = Gtk.Button(label='Open')
        self.openButton.set_icon_name('document-open_symbolic')
        self.openButton.connect('clicked', self._fileOpen)
        self.header.pack_start(self.openButton)

        # Create a new action.
        action = Gio.SimpleAction.new('something', None)
        action.connect('activate', self.simpleAction)
        self.add_action(action)

        # Create a new menu, containing the simple action.
        menu = Gio.Menu.new()
        menu.append('Do Something', 'win.something')

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

        # Create an action to run a show about dialog function.
        action = Gio.SimpleAction.new('about', None)
        action.connect('activate', self.simpleAction)
        self.add_action(action)
        menu.append('About', 'win.about')

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



    def simpleAction(self, action, param):
        print('Simple Action')



    def _treeSelectionChanged(self, treeSelection):
        ''' Signal handler for the selection on tree changing. '''
        selection = ''

        # liststoreFiles = self.builder.get_object('liststoreFiles')
        liststoreFiles = self.liststoreFiles
        mode = treeSelection.get_mode()
        if mode == Gtk.SelectionMode.SINGLE or mode == Gtk.SelectionMode.BROWSE:
            model, treeIter = treeSelection.get_selected()
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



    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # An initial message.
        print('GTK+ Version {}.{}.{} (expecting GTK+4).'.format(Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version()))

        self.connect('activate', self.onActivate)




    def onActivate(self, app):
        ''' Create the main window. '''
        self.window = MainWindow(application=app)
        self.window.present()



