import sys
import os
from os import path
import errno
import platform
import logging
import logging.handlers

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
import appdirs

from annotator import Annotator



def qt_message_handler(mode, context, message):
    logger = logging.getLogger(__name__)
    if mode == QtCore.QtInfoMsg:
        logger.info(message)
    elif mode == QtCore.QtWarningMsg:
        logger.warning(message)
    elif mode == QtCore.QtCriticalMsg:
        logger.error(message)
    elif mode == QtCore.QtFatalMsg:
        logger.critical(message)
    else:
        logger.debug(message)


if __name__ == '__main__':
    # make the Python warnings go to logger
    logging.captureWarnings(True)

    log_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    formatter = logging.Formatter(log_format)

    log_filename = 'log.txt'
    dirs = appdirs.AppDirs('Annotator', '')
    log_dir = dirs.user_data_dir
    try:
        os.makedirs(log_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    log_fp = path.join(log_dir, log_filename)

    # log to file
    file_handler = logging.handlers.RotatingFileHandler(log_fp, maxBytes=100000, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)
    rootLogger.addHandler(file_handler)

    if hasattr(sys, 'frozen'):
        # redirect stdout and stderr to the logger if this is a py2app or pyinstaller bundle
        sys.stdout = StreamToLogger(logging.getLogger('STDOUT'), logging.INFO)
        sys.stderr = StreamToLogger(logging.getLogger('STDERR'), logging.ERROR)
    else:
        # log to console if this is not a py2app or pyinstaller bundle
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        rootLogger.addHandler(console)

    # make Qt logs go to logger
    QtCore.qInstallMessageHandler(qt_message_handler)

    logger = logging.getLogger(__name__)

    logger.info('Annotator %s starting on %s (%s)', '0.0.0.0', platform.system(), sys.platform)

    # make sure Qt loads the desktop OpenGL stack, rather than OpenGL ES or a software OpenGL
    # only the former option is compatible with the use of PyOpenGL
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseDesktopOpenGL)

    if platform.system() == 'Windows':
        logger.info('Applying Windows-specific setup')

        # enable automatic scaling for high-DPI screens
        os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

        # set the App ID for Windows 7 to properly display the icon in the
        # taskbar.
        import ctypes
        myappid = '??????'  # arbitrary string
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            logger.error('Could not set the app model ID. If the plaftorm is older than Windows 7, this is normal.')

    app = QApplication(sys.argv)

    if platform.system() == 'Darwin':
        logger.info('Applying Mac OS-specific setup')
        # # help the py2app-packaged application find the Qt plugins (imageformats and platforms)
        # pluginsPath = os.path.normpath(os.path.join(QApplication.applicationDirPath(), os.path.pardir, 'PlugIns'))
        # logger.info('Adding the following to the Library paths: %s', pluginsPath)
        # QApplication.addLibraryPath(pluginsPath)

        # # on macOS, OpenGL 2.1 does not work well
        # # request a 3.2 Core context instead
        # format = QSurfaceFormat()
        # format.setDepthBufferSize(24)
        # format.setStencilBufferSize(8)
        # format.setVersion(3, 2)
        # format.setProfile(QSurfaceFormat.CoreProfile)
        # QSurfaceFormat.setDefaultFormat(format)

    # # Splash screen
    # pixmap = QPixmap(':/images/splash.png')
    # splash = QSplashScreen(pixmap)
    # splash.show()
    # splash.showMessage('Initializing the audio subsystem')
    # app.processEvents()

    if len(sys.argv) < 2:
        print('You must supply either a saved session textfile or the datapath, savepath, \
and csvfilename. See python main.py -h for more info.')
    else:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', dest='datapath', type=str, 
            help='Full path to folder with audio clips.')
        parser.add_argument('-s', dest='savepath', type=str,
            help='Full path to existing folder where new clips will be saved.')
        parser.add_argument('-f', dest='csvfile', type=str,
            help='The full path and filename of the csvfile where data tags will be saved.')
        parser.add_argument('-t', dest='savesession', default='./support/ss.txt', type=str,
            help='The filepath of the saved session you want to save.')
        parser.add_argument('-l', dest='loadsession', type=str,
            help='The filepath of the saved session you want to load. This will be overwritten in next save.')
        parser.add_argument('-m', dest='min_dur', default=1.0, type=float,
            help='The minimum duration in seconds of a miniclip.')
        args = parser.parse_args()

        if args.loadsession is not None:  # if provided with a session to load
            with open(args.loadsession, 'r') as f:
                data_folder, save_folder, csv_filename, min_dur, f_ind, d_ind = f.readline().strip().split(',')
                window = Annotator(data_folder, save_folder, csv_filename, args.loadsession, 
                    float(min_dur), int(f_ind), int(d_ind))
        else:
            if '.csv' not in args.csvfile:
                raise Exception('must be a csvfile (got {})'.format(args.csvfile))
            window = Annotator(args.datapath, args.savepath, args.csvfile, args.savesession, args.min_dur)

        window.show()

        return_code = app.exec_()

        # explicitly delete the main windows instead of waiting for the interpreter shutdown
        # tentative to prevent errors on exit on macos
        del window
        sys.exit(return_code)
