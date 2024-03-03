TotalObserver WCX Plugin for Total Commander
Copyright: 2016, Egor Vlaznev

-------------------------------------------------------------------

1. General information.

This plug-in assists in listing and extracting content from several types of containers.
This plug-in uses modules from Observer Plug-in for FAR Manager Copyright: 2009-2015, Ariman

1.1. Supported formats:

- Installation packages
  - MSI packages for Windows Installer
  - Installation packages made with Wise Installer
  - Install Shield packages.
  - Setup Factory packages.
  - Create Install(gentee) packages.

- Images of the optical disc (CD/DVD/Blu-ray)
  - ISO-images. Following formats are supported:
    - ISO-9660 (incl. Joliet, RockRidge)
    - UDF (ISO 13346) up to revision 2.60
  - NRG-images Nero Burning ROM
  - BIN-images CDRWIN (CUE/BIN)
  - MDF-images Alcohol 120% (MDF/MDS)
  - ISZ-images UltraISO

- MIME
  - MIME containers (.eml, .mht, etc.)
  - MS Outlook databases (*.pst)
  - MBox containers
  - The Bat! databases (*.tbb)

- Containers used in various games
  - CAT, PCK, PBD, PBB - used by Egosoft for X-series games
  - VP - Volition Pack V2 (from FreeSpace 1/2/Open)
  - BIG, SGA - containers from games made by Relic (Homeworld 1/2, CoH, WH40k DoW 1/2)
  - GCF, WAD, XZP, PAK, BSP, VBSP - used inside Steam
  - MoPaQ packages (used by Blizzard)

- Other
  - Embedded files from PDF.

1.2. Settings.

Main plugin options are in [General] section.
Settings for each individual module will reside with section with module name.

Currently you can configure following options:

1.2.1 General settings.

[General] -> VerboseModuleLoad
Turns on/off warning message on plugin start if any if the modules failed to load.
Possible values: 1 (show message) or 0 (don't show).

[General] -> UseExtensionFilters
Enable/disable using of extesion filters (see 1.2.2).
Possible values: 1 (enable) or 0 (disable).


1.2.2 Filters.

[Filters]
This section sets file extention masks for modules to speed up files processing.
Filters are used when entering file by Enter or Ctrl-PgDn keys.
Values are set in following format: ModuleName=.ext1;.ext2;.ext3
Module names are from [Modules] section and case sensitive. Extentions in list are seprated
by semicolon and have dot in front. They are case-insensitive.
If any module don't have filters set or extentions list is empty, then it is considered
that module accepts all files.

1.2.3 Module-specific configuration.

Values marked with * are default values.

[ISO] -> Charset
[ISO] -> RockRidge
Enables (1)* / disables (0) support for RockRidge extension.

[PST] -> HideEmptyFolder
Enables (1) / disables (0)* hiding of empty folders.

2. System requirements.
OS: WinXP or higher.
MSI module requires Windows Installer 4+
