from setuptools import setup

APP = ['app.py']
APP_NAME = "İnşaat Asistanı"
DATA_FILES = []
OPTIONS = {
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "İnşaat Asistanı Demo Uygulaması",
        'CFBundleIdentifier': "com.bariskahraman.osx.inşaatasistanı", # Benzersiz bir kimlik
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
    }
}

setup(
    app=APP,
    name=APP_NAME,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)