#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Class show to a GTK3+ window with a treeview control.
'''

import sys
# Import Gtk3 libraries.
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GObject, Gdk
    from gi.repository import GdkPixbuf
except:
    print("GTK3 Not Available. ({})".format(__file__))
    sys.exit(0)
import os
import subprocess
import shutil
import datetime

# Application libraries.



class MainWindow():
    '''
    Class to represent the main window for the rename program.

    :ivar Gtk.Builder builder: The GTK+ builder for the dialog.
    :ivar Gtk.Window window: The actual GTK+ window.
    '''



    def __init__(self, args):
        '''
        Class constructor for the :py:class:`MainWindow` class.

        :param object args: The program arguments.
        '''
        # Positive to ignore signals.
        self.no_events = 0

        # The GTK+ builder for the main window.
        self.builder = Gtk.Builder()
        self.builder.add_from_file('{}/main_window.glade'.format(os.path.dirname(os.path.realpath(__file__))))
        # The actual GTK+ window.
        self.window = self.builder.get_object('windowMain')
        if self.window:
            self.window.connect('destroy', Gtk.main_quit)

        dic = {
            'on_menuFileRefresh_activate'           : self._fileRefresh,
            'on_menuFileOpen_activate'              : self._fileOpen,
            'on_menuFileExit_activate'              : self._fileQuit,
            'on_menuViewOpenFolder_activate'        : self._viewOpenFolder,

            'on_treeselectionFiles_changed'         : self._treeSelectionChanged,
        }
        self.builder.connect_signals(dic)

        # Get the initial folder.  This is probably from args.
        self.folderName = os.path.dirname(os.path.realpath(__file__))
        self.scanFolder()

        # An initial message.
        print('GTK+ Version {}.{}.{} (expecting GTK+3).'.format(Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version()))





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



    def runMainLoop(self):
        ''' Run the Gtk main loop. '''
        self.window.show_all()
        Gtk.main()
