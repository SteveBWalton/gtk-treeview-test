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
    from gi.repository import Gtk, Adw
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

        # Add a vertical box.
        self.boxMain = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.boxMain)

        # Add a horizontal box.
        self.boxDetails = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.boxMain.append(self.boxDetails)

        # Add a button.
        self.button = Gtk.Button(label="Hello")
        self.boxDetails.append(self.button)
        self.button.connect('clicked', self.helloClicked)

        # Add a label.
        self.labelSelection = Gtk.Label(label="Goodbye World.")
        self.boxDetails.append(self.labelSelection)

        # Add a button into the header bar.
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.openButton = Gtk.Button(label='Open')
        self.openButton.set_icon_name('document-open_symbolic')
        self.header.pack_start(self.openButton)

        return
        # Positive to ignore signals.
        self.no_events = 0

        # The GTK+ builder for the main window.
        self.builder = Gtk.Builder()
        self.builder.new_from_file(f'{os.path.dirname(os.path.realpath(__file__))}/main_window.ui')
        # The actual GTK+ window.
        self.window = self.builder.get_object('windowMain')
        if self.window:
            self.window.connect('destroy', Gtk.main_quit)

        #dic = {
        #    'on_menuFileRefresh_activate'           : self._fileRefresh,
        #    'on_menuFileOpen_activate'              : self._fileOpen,
        #    'on_menuFileExit_activate'              : self._fileQuit,
        #    'on_menuViewOpenFolder_activate'        : self._viewOpenFolder,
        #
        #    'on_treeselectionFiles_changed'         : self._treeSelectionChanged,
        #}
        #self.builder.connect_signals(dic)

        # Get the initial folder.  This is probably from args.
        self.folderName = os.path.dirname(os.path.realpath(__file__))
        self.scanFolder()

        # Move the focus off the toolbar.
        # self.webview.grab_focus()

        # An initial message.
        print('GTK+ Version {}.{}.{} (expecting GTK+4).'.format(Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version()))




    def helloClicked(self, button):
        print('Hello World')
        self.labelSelection.set_label("Hello World.")
        myText = self.labelSelection.get_label()
        print(f'{myText=}')
        self.labelSelection.set_text("Hello")
        myText = self.labelSelection.get_text()
        print(f'{myText=}')



    def _treeSelectionChanged(self, treeSelection):
        ''' Signal handler for the selection on tree changing. '''
        selection = ''

        liststoreFiles = self.builder.get_object('liststoreFiles')
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
        labelSelection = self.builder.get_object('labelSelection')
        labelSelection.set_text(selection)



    def _fileRefresh(self, widget):
        ''' Signal handler for the 'File' → 'Refresh' menu point. '''
        self.scanFolder()



    def _fileOpen(self, widget):
        ''' Signal handler for the 'File' → 'Open' menu point. '''
        # Create a folder chooser dialog.
        dialog = Gtk.FileChooserDialog(title = 'Select Source Folder', parent = self.window, action = Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)

        # Set the current source as the initial value for the dialog if not empty.
        dialog.set_current_folder(self.folderName)

        # Display the file chooser dialog.
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.folderName = dialog.get_filename()
            # self.configuration.SetFolderName(self.folderName)
            self.scanFolder()

        # Close the file chooser dialog.
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
        liststoreFiles = self.builder.get_object('liststoreFiles')
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
            fileName , extension = os.path.splitext(theFile)
            extension = extension.lower()
            if True:
                count += 1
                iterFiles = liststoreFiles.append()
                liststoreFiles.set(iterFiles, 0, theFile)

        treeviewcolumnFilename = self.builder.get_object('treeviewcolumnFilename')
        treeviewcolumnFilename.set_title('Files ({})'.format(count))



class TreeViewApp(Adw.Application):



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.onActivate)



    def onActivate(self, app):
        ''' Create the main window. '''
        self.window = MainWindow(application=app)
        self.window.present()



