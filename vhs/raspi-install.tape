Output raspi-install.gif

Set FontSize 12
Set Width 800
Set Height 450

Type 'ssh -l pi 192.168.1.214'
Sleep 600ms
Enter
Sleep 1s
Enter

Type 'mkdir demo && cd demo'
Sleep 600ms
Enter
Enter
Sleep 100ms

Type 'sh -c "$(curl -fsSL https://machbase.com/install.sh)"'
Sleep 1s
Enter
Sleep 2s
Sleep 2s
Sleep 2s
Sleep 2s
Sleep 2s
Sleep 2s
Sleep 500ms

Enter 2
Sleep 100ms
Type 'unzip machbase-neo-edge-v0.2.1-linux-arm64.zip'
Enter
Sleep 3s
Type 'cd machbase-neo-edge-v0.2.1-linux-arm64'
Sleep 500ms
Enter

Sleep 100ms
Type './machbase-neo serve'
Sleep 600ms
Enter

Sleep 2s
Sleep 2s
Sleep 2s
Sleep 2s
