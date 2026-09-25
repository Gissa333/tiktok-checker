[Setup]
AppName=TikTok Username Checker
AppVersion=1.0
AppPublisher=Gissa333
DefaultDirName={autopf}\TikTokChecker
DefaultGroupName=TikTok Checker
OutputDir=installer_output
OutputBaseFilename=TikTokChecker-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes

[Files]
Source: "dist\TikTokChecker.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\TikTok Checker"; Filename: "{app}\TikTokChecker.exe"
Name: "{autodesktop}\TikTok Checker"; Filename: "{app}\TikTokChecker.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional:"

[Run]
Filename: "{app}\TikTokChecker.exe"; Description: "Launch TikTok Checker"; Flags: nowait postinstall skipifsilent
