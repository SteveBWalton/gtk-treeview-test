#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to a GTK+ window with a treeview control.
'''

# System libraries for the initial phase.
import sys
import os
import argparse


if __name__ == '__main__':
    # Process the command line arguments.
    # This might end the program (--help).
    oParse = argparse.ArgumentParser(prog='gtk_treeview_test', description='Display a treeview control.')
    oParse.add_argument('-i', '--install', help='Install the program and desktop link.', action='store_true')
    oParse.add_argument('-u', '--uninstall', help='Uninstall the program.', action='store_true')
    oArgs = oParse.parse_args()

    if oArgs.install:
        print('Not implemented.')

    if oArgs.uninstall:
        print('Not implemented.')

    # Welcome message.
    print('\033[1;31mGTK+ Treeview Test\033[0;m by Steve Walton.')
    print('Python Version {}.{}.{} (expecting 3).'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))

# Import Gtk3+ libraries.
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GObject, Gdk
    from gi.repository import GdkPixbuf
except:
    print("GTK Not Available. ({})".format(__file__))
import os
import platform
import subprocess
import shutil
import datetime
# import urllib
import sqlite3

# Application libraries.



class CMainWindow():
    '''
    Class to represent the main window for the rename program.

    :ivar Gtk.Builder builder: The GTK+ builder for the dialog.
    :ivar Gtk.Window window: The actual GTK+ window.
    '''



    def __init__(self, oArgs):
        '''
        Class constructor for the :py:class:`CMainWindow` class.

        :param object oArgs: The program arguments.
        '''
        # Positive to ignore signals.
        self.no_events = 0

        # The GTK+ builder for the main window.
        self.builder = Gtk.Builder()
        self.builder.add_from_file('{}/gtk_treeview_test.glade'.format(os.path.dirname(os.path.realpath(__file__))))
        # The actual GTK+ window.
        self.window = self.builder.get_object('windowMain')
        if self.window:
            self.window.connect('destroy', Gtk.main_quit)

        dic = {
            'on_menuFileRefresh_activate'           : self._FileRefresh,
            'on_menuFileOpen_activate'              : self._FileOpen,
            'on_menuFileExit_activate'              : self._FileQuit,
            'on_menuViewOpenFolder_activate'        : self._ViewOpenFolder,

            'on_treeselectionFiles_changed'         : self._TreeSelectionChanged,
        }
        self.builder.connect_signals(dic)

        # Get the initial folder.  This is probably from oArgs.
        self.folder_name = os.path.dirname(os.path.realpath(__file__))
        self.ScanFolder()

        # Move the focus off the toolbar.
        # self.webview.grab_focus()





    def _TreeSelectionChanged(self, oTreeSelection):
        ''' Signal handler for the selection on tree changing. '''
        sSelection = ''

        liststoreFiles = self.builder.get_object('liststoreFiles')
        nMode = oTreeSelection.get_mode()
        if nMode == Gtk.SelectionMode.SINGLE or nMode == Gtk.SelectionMode.BROWSE:
            nModel, oTreeIter = oTreeSelection.get_selected()
        elif nMode == Gtk.SelectionMode.MULTIPLE:
            nModel, oPathList = oTreeSelection.get_selected_rows()

            for oPath in oPathList:
                oTreeIter = liststoreFiles.get_iter(oPath)
                sFilename = liststoreFiles.get_value(oTreeIter, 0)
                if sSelection == '':
                    sSelection = sFilename
                else:
                    sSelection = '{}\n{}'.format(sSelection, sFilename)

        # Display the filename.
        labelSelection = self.builder.get_object('labelSelection')
        labelSelection.set_text(sSelection)



    def _FileRefresh(self, oWidget):
        ''' Signal handler for the 'File' → 'Refresh' menu point. '''
        self.ScanFolder()



    def _FileOpen(self, oWidget):
        ''' Signal handler for the 'File' → 'Open' menu point. '''
        # Create a folder chooser dialog.
        oDialog = Gtk.FileChooserDialog('Select Source Folder', self.window, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        oDialog.set_default_response(Gtk.ResponseType.OK)

        # Set the current source as the initial value for the dialog if not empty.
        oDialog.set_current_folder(self.folder_name)

        # Display the file chooser dialog.
        nResponse = oDialog.run()
        if nResponse == Gtk.ResponseType.OK:
            self.folder_name = oDialog.get_filename()
            self.configuration.SetFolderName(self.folder_name)
            self.ScanFolder()

        # Close the file chooser dialog.
        oDialog.destroy()



    def _FileQuit(self, oWidget):
        ''' Signal handler for the 'File' → 'Quit' menu point. '''
        # Close the main window and hence exit the Gtk loop.
        self.window.destroy()



    def _ViewOpenFolder(self, oWidget):
        ''' Signal handler for the 'View' → 'Open Folder' menu point. '''
        subprocess.Popen(['xdg-open', self.folder_name])



    def ScanFolder(self):
        ''' Scan the images in the specified folder. '''
        liststoreFiles = self.builder.get_object('liststoreFiles')
        liststoreFiles.clear()
        try:
            oEverything = os.listdir(self.folder_name)
        except:
            oEverything = []

        oEverything.sort()

        nCount = 0
        for oFile in oEverything:
            sFilename , sExtension = os.path.splitext(oFile)
            sExtension = sExtension.lower()
            if True:
                nCount = nCount+1
                oIter = liststoreFiles.append()
                liststoreFiles.set(oIter, 0, oFile)

        treeviewcolumnFilename = self.builder.get_object('treeviewcolumnFilename')
        treeviewcolumnFilename.set_title('Files ({})'.format(nCount))



if __name__ == '__main__':
    # An initial message.
    print('Operating System is "{}".  Desktop is "{}".'.format(platform.system(), os.environ.get('DESKTOP_SESSION')))
    print('GTK+ Version {}.{}.{} (expecting GTK+3).'.format(Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version()))

    # Main GTK loop.
    oMainWindow = CMainWindow(oArgs)
    oMainWindow.window.show_all()
    Gtk.main()

    # A final message
    print('Goodbye from the \033[1;31mGTK+ Treeview Test\033[0;m program.')
