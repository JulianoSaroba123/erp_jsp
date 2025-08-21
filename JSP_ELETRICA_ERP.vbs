Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Obter diretório do script
strScriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Mudar para diretório do projeto
objShell.CurrentDirectory = strScriptDir

' Executar o inicializador
objShell.Run "iniciar_sistema.bat", 1, False
