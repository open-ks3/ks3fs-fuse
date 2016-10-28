
sh autogen.sh
./configure

INCTCMALLOC="-I../third-party/tcmalloc/output/include"
LIBTCMALLOC="-L../third-party/tcmalloc/output/lib -L../third-party/libunwind/output/lib -ltcmalloc -lunwind -lprofiler"
DEPS_CFLAGS=`grep "^DEPS_CFLAGS = " src/Makefile|grep -v tcmalloc`
DEPS_LIBS=`grep "^DEPS_LIBS = " src/Makefile|grep -v tcmalloc`
if [ "$DEPS_CFLAGS" != "" ]; then
    sed -i "s:^DEPS_CFLAGS = .*:$DEPS_CFLAGS $INCTCMALLOC:g" src/Makefile
fi
if [ "$DEPS_LIBS" != "" ]; then
    sed -i "s:^DEPS_LIBS = .*:$DEPS_LIBS $LIBTCMALLOC:g" src/Makefile
fi

make USE_PROFILE=True -j
make install

#CXXFLAGS = -std=c++11 -g -fstack-protector -fno-omit-frame-pointer -fsanitize=address -ggdb -Wall -D_FILE_OFFSET_BITS=64
#CXXFLAGS = -g -fstack-protector -fstack-protector-all -Wall -D_FILE_OFFSET_BITS=64
#CXXFLAGS = -g -fsanitize=thread -fPIE -pie -Wall -D_FILE_OFFSET_BITS=64
#DEPS_LIBS = -ltsan -pthread -L/usr/local/lib -lfuse -lrt -ldl -lcurl -lxml2 -lcrypto
#DEPS_LIBS = -lasan -pthread -L/usr/local/lib -lfuse -lrt -ldl -lcurl -lxml2 -lcrypto
