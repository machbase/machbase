Output instant-install.gif

Set FontSize 12
Set Width 800
Set Height 400

Type 'sh -c "$(curl -fsSL https://neo.machbase.com/install.sh)"'
Sleep 500ms
Enter

Sleep 5000ms
Enter

Type `unzip -p machbase-*.zip '*machbase-neo' > machbase-neo && chmod +x machbase-neo`
Enter
Sleep 1000ms

Type `./machbase-neo version`
Sleep 500ms
Enter

Sleep 5s