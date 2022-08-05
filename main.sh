#!/usr/bin/env sh

echo "<ul>" >> README.md
for i in {1..62}
do
    echo "<li><img src='https://github.com/adityastomar67/Wallpapers/blob/main/wall$i.jpg' alt='wall$i' width=400px></li>" >> README.md
done

echo "</ul>" >> README.md
