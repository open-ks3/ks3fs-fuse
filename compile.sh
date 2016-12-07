export PKG_CONFIG_PATH=/usr/lib/pkgconfig:/usr/lib64/pkgconfig/:/usr/local/lib/pkgconfig/
sh version.sh
./autogen.sh
./configure
make -j
