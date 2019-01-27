#/bin/sh

#nvm use v8.2.1
#npm run build
rm -rf /home/code/LaundryVue_v2/server/app/static/
echo "delete app/static done"
rm -rf /home/code/LaundryVue_v2/server/app/templates/index.html
echo "deltee app/templates/index.html done"
/bin/cp -rf /home/code/LaundryVue_v2/dist/index.html  /home/code/LaundryVue_v2/server/app/templates/.
echo " copy index.html done"
/bin/cp -rf /home/code/LaundryVue_v2/dist/static/ /home/code/LaundryVue_v2/server/app/.
echo "copy done"
