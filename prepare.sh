yum remove fuse fuse fuse-devel
yum install gcc libstdc++-devel gcc-c++ curl curl curl-devel libxml2 libxml2* libxml2-devel openssl-devel mailcap
tar -xzvf fuse-2.9.7.tar.gz
cd fuse-2.9.7
./configure
make
make install
export PKG_CONFIG_PATH=/usr/lib/pkgconfig:/usr/lib64/pkgconfig/:/usr/local/lib/pkgconfig/
ldconfig
modprobe fuse
pkg-config --odversion fuse
