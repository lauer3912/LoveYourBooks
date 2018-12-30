# 各平台系统标准路径

参照 [http://doc.qt.io/qt-5/qstandardpaths.html](http://doc.qt.io/qt-5/qstandardpaths.html)

| 常量                                  | 枚举值       | 描述                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| QStandardPaths::DesktopLocation       | 0            | Returns the user's desktop directory. This is a generic value. On systems with no concept of a desktop, this is the same as QStandardPaths::HomeLocation.                                                                                                                                                                                                                     |
| QStandardPaths::DocumentsLocation     | 1            | Returns the directory containing user document files. This is a generic value. The returned path is never empty.                                                                                                                                                                                                                                                              |
| QStandardPaths::FontsLocation         | 2            | Returns the directory containing user's fonts. This is a generic value. Note that installing fonts may require additional, platform-specific operations.                                                                                                                                                                                                                      |
| QStandardPaths::ApplicationsLocation  | 3            | Returns the directory containing the user applications (either executables, application bundles, or shortcuts to them). This is a generic value. Note that installing applications may require additional, platform-specific operations. Files, folders or shortcuts in this directory are platform-specific.                                                                 |
| QStandardPaths::MusicLocation         | 4            | Returns the directory containing the user's music or other audio files. This is a generic value. If no directory specific for music files exists, a sensible fallback for storing user documents is returned.                                                                                                                                                                 |
| QStandardPaths::MoviesLocation        | 5            | Returns the directory containing the user's movies and videos. This is a generic value. If no directory specific for movie files exists, a sensible fallback for storing user documents is returned.                                                                                                                                                                          |
| QStandardPaths::PicturesLocation      | 6            | Returns the directory containing the user's pictures or photos. This is a generic value. If no directory specific for picture files exists, a sensible fallback for storing user documents is returned.                                                                                                                                                                       |
| QStandardPaths::TempLocation          | 7            | Returns a directory where temporary files can be stored. The returned value might be application-specific, shared among other applications for this user, or even system-wide. The returned path is never empty.                                                                                                                                                              |
| QStandardPaths::HomeLocation          | 8            | Returns the user's home directory (the same as QDir::homePath()). On Unix systems, this is equal to the HOME environment variable. This value might be generic or application-specific, but the returned path is never empty.                                                                                                                                                 |
| QStandardPaths::DataLocation          | 9            | Returns the same value as AppLocalDataLocation. This enumeration value is deprecated. Using AppDataLocation is preferable since on Windows, the roaming path is recommended.                                                                                                                                                                                                  |
| QStandardPaths::CacheLocation         | 10           | Returns a directory location where user-specific non-essential (cached) data should be written. This is an application-specific directory. The returned path is never empty.                                                                                                                                                                                                  |
| QStandardPaths::GenericCacheLocation  | 15           | Returns a directory location where user-specific non-essential (cached) data, shared across applications, should be written. This is a generic value. Note that the returned path may be empty if the system has no concept of shared cache.                                                                                                                                  |
| QStandardPaths::GenericDataLocation   | 11           | Returns a directory location where persistent data shared across applications can be stored. This is a generic value. The returned path is never empty.                                                                                                                                                                                                                       |
| QStandardPaths::RuntimeLocation       | 12           | Returns a directory location where runtime communication files should be written, like Unix local sockets. This is a generic value. The returned path may be empty on some systems.                                                                                                                                                                                           |
| QStandardPaths::ConfigLocation        | 13           | Returns a directory location where user-specific configuration files should be written. This may be either a generic value or application-specific, and the returned path is never empty.                                                                                                                                                                                     |
| QStandardPaths::DownloadLocation      | 14           | Returns a directory for user's downloaded files. This is a generic value. If no directory specific for downloads exists, a sensible fallback for storing user documents is returned.                                                                                                                                                                                          |
| QStandardPaths::GenericConfigLocation | 16           | Returns a directory location where user-specific configuration files shared between multiple applications should be written. This is a generic value and the returned path is never empty.                                                                                                                                                                                    |
| QStandardPaths::AppDataLocation       | 17           | Returns a directory location where persistent application data can be stored. This is an application-specific directory. To obtain a path to store data to be shared with other applications, use QStandardPaths::GenericDataLocation. The returned path is never empty. On the Windows operating system, this returns the roaming path. This enum value was added in Qt 5.4. |
| QStandardPaths::AppLocalDataLocation  | DataLocation | Returns the local settings path on the Windows operating system. On all other platforms, it returns the same value as AppDataLocation. This enum value was added in Qt 5.4.                                                                                                                                                                                                   |
| QStandardPaths::AppConfigLocation     | 18           | Returns a directory location where user-specific configuration files should be written. This is an application-specific directory, and the returned path is never empty. This enum value was added in Qt 5.5.                                                                                                                                                                 |

---

## macOS 系统的标准路径

| 路径类型              | macOS                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------------ |
| DesktopLocation       | "~/Desktop"                                                                                                  |
| DocumentsLocation     | "~/Documents"                                                                                                |
| FontsLocation         | "/System/Library/Fonts" (not writable)                                                                       |
| ApplicationsLocation  | "/Applications" (not writable)                                                                               |
| MusicLocation         | "~/Music"                                                                                                    |
| MoviesLocation        | "~/Movies"                                                                                                   |
| PicturesLocation      | "~/Pictures"                                                                                                 |
| TempLocation          | randomly generated by the OS                                                                                 |
| HomeLocation          | "~"                                                                                                          |
| DataLocation          | "~/Library/Application Support/<APPNAME>", "/Library/Application Support/<APPNAME>". "<APPDIR>/../Resources" |
| CacheLocation         | "~/Library/Caches/<APPNAME>", "/Library/Caches/<APPNAME>"                                                    |
| GenericDataLocation   | "~/Library/Application Support", "/Library/Application Support"                                              |
| RuntimeLocation       | "~/Library/Application Support"                                                                              |
| ConfigLocation        | "~/Library/Preferences"                                                                                      |
| GenericConfigLocation | "~/Library/Preferences"                                                                                      |
| DownloadLocation      | "~/Downloads"                                                                                                |
| GenericCacheLocation  | "~/Library/Caches", "/Library/Caches"                                                                        |
| AppDataLocation       | "~/Library/Application Support/<APPNAME>", "/Library/Application Support/<APPNAME>". "<APPDIR>/../Resources" |
| AppLocalDataLocation  | "~/Library/Application Support/<APPNAME>", "/Library/Application Support/<APPNAME>". "<APPDIR>/../Resources" |
| AppConfigLocation     | "~/Library/Preferences/<APPNAME>"                                                                            |

## Windows 系统的标准路径

| 路径类型              | Windows                                                                                                                         |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| DesktopLocation       | "C:/Users/<USER>/Desktop"                                                                                                       |
| DocumentsLocation     | "C:/Users/<USER>/Documents"                                                                                                     |
| FontsLocation         | "C:/Windows/Fonts" (not writable)                                                                                               |
| ApplicationsLocation  | "C:/Users/<USER>/AppData/Roaming/Microsoft/Windows/Start Menu/Programs"                                                         |
| MusicLocation         | "C:/Users/<USER>/Music"                                                                                                         |
| MoviesLocation        | "C:/Users/<USER>/Videos"                                                                                                        |
| PicturesLocation      | "C:/Users/<USER>/Pictures"                                                                                                      |
| TempLocation          | "C:/Users/<USER>/AppData/Local/Temp"                                                                                            |
| HomeLocation          | "C:/Users/<USER>"                                                                                                               |
| DataLocation          | "C:/Users/<USER>/AppData/Local/<APPNAME>", "C:/ProgramData/<APPNAME>", "<APPDIR>", "<APPDIR>/data", "<APPDIR>/data/<APPNAME>"   |
| CacheLocation         | "C:/Users/<USER>/AppData/Local/<APPNAME>/cache"                                                                                 |
| GenericDataLocation   | "C:/Users/<USER>/AppData/Local", "C:/ProgramData", "<APPDIR>", "<APPDIR>/data"                                                  |
| RuntimeLocation       | "C:/Users/<USER>"                                                                                                               |
| ConfigLocation        | "C:/Users/<USER>/AppData/Local/<APPNAME>", "C:/ProgramData/<APPNAME>"                                                           |
| GenericConfigLocation | "C:/Users/<USER>/AppData/Local", "C:/ProgramData"                                                                               |
| DownloadLocation      | "C:/Users/<USER>/Documents"                                                                                                     |
| GenericCacheLocation  | "C:/Users/<USER>/AppData/Local/cache"                                                                                           |
| AppDataLocation       | "C:/Users/<USER>/AppData/Roaming/<APPNAME>", "C:/ProgramData/<APPNAME>", "<APPDIR>", "<APPDIR>/data", "<APPDIR>/data/<APPNAME>" |
| AppLocalDataLocation  | "C:/Users/<USER>/AppData/Local/<APPNAME>", "C:/ProgramData/<APPNAME>", "<APPDIR>", "<APPDIR>/data", "<APPDIR>/data/<APPNAME>"   |
| AppConfigLocation     | "C:/Users/<USER>/AppData/Local/<APPNAME>", "C:/ProgramData/<APPNAME>"                                                           |

## Linux 系统的标准路径

| 路径类型              | macOS                                                                                     |
| --------------------- | ----------------------------------------------------------------------------------------- |
| DesktopLocation       | "~/Desktop"                                                                               |
| DocumentsLocation     | "~/Documents"                                                                             |
| FontsLocation         | "~/.fonts"                                                                                |
| ApplicationsLocation  | "~/.local/share/applications", "/usr/local/share/applications", "/usr/share/applications" |
| MusicLocation         | "~/Music"                                                                                 |
| MoviesLocation        | "~/Videos"                                                                                |
| PicturesLocation      | "~/Pictures"                                                                              |
| TempLocation          | "/tmp"                                                                                    |
| HomeLocation          | "~"                                                                                       |
| DataLocation          | "~/.local/share/<APPNAME>", "/usr/local/share/<APPNAME>", "/usr/share/<APPNAME>"          |
| CacheLocation         | "~/.cache/<APPNAME>"                                                                      |
| GenericDataLocation   | "~/.local/share", "/usr/local/share", "/usr/share"                                        |
| RuntimeLocation       | "/run/user/<USER>"                                                                        |
| ConfigLocation        | "~/.config", "/etc/xdg"                                                                   |
| GenericConfigLocation | "~/.config", "/etc/xdg"                                                                   |
| DownloadLocation      | "~/Downloads"                                                                             |
| GenericCacheLocation  | "~/.cache"                                                                                |
| AppDataLocation       | "~/.local/share/<APPNAME>", "/usr/local/share/<APPNAME>", "/usr/share/<APPNAME>"          |
| AppLocalDataLocation  | "~/.local/share/<APPNAME>", "/usr/local/share/<APPNAME>", "/usr/share/<APPNAME>"          |
| AppConfigLocation     | "~/.config/<APPNAME>", "/etc/xdg/<APPNAME>"                                               |

## Android 及 iOS 相关的系统路径

请参考 [http://doc.qt.io/qt-5/qstandardpaths.html](http://doc.qt.io/qt-5/qstandardpaths.html)
