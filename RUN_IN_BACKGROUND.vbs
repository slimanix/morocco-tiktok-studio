Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\elidr\.gemini\antigravity\scratch\morocco_tiktok_pipeline"
WshShell.Run "python full_autonomous_service.py", 0, False
