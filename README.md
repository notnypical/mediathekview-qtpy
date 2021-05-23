
# MediathekView-QtPy

A front-end tool for the MediathekView database written in Qt for Python.


## Description

MediathekView-QtPy is an open source front-end tool written in Qt for Python and designed for easy access to the [MediathekView](https://mediathekview.de) database.


## Usage


### Resources

The resource collection files are converted to Python modules by using the resource compiler rcc:  

Qt 5.14 or later:  
```rcc -g python icons.qrc -o icons_rc.py```  
```rcc -g python translations.qrc -o translations_rc.py```

Qt 5.13 or older:  
```pyside2-rcc icons.qrc -o icons_rc.py```  
```pyside2-rcc translations.qrc -o translations_rc.py```


### Translations

The translation TS files are converted to QM files by using the lrelease command line tool:  

```lrelease translations/*.ts```  


## Copyright

Copyright &copy; 2020-2021 [NotNypical](https://notnypical.github.io).


## License

This application is released under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).


## Credits

Application logo and icons made by [BreezeIcons project](https://api.kde.org/frameworks/breeze-icons/html/index.html) from [KDE](https://kde.org)
are licensed under [LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.en.html).
