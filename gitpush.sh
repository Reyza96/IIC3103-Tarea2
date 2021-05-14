git add .

echo 'Introduzca fecha en formato dd-mm-aaaa:'
read commitMessage

git commit -m "$commitMessage"

git push origin master

read