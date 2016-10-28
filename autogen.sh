#! /bin/sh

# This file is part of S3FS.
# 
# Copyright 2009, 2010 Free Software Foundation, Inc.
# 
# S3FS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
# 
# S3FS is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/. 
# 
#  See the file ChangeLog for a revision history. 

echo "--- Make commit hash file -------"

SHORTHASH="unknown"
type git > /dev/null 2>&1
if [ $? -eq 0 -a -d .git ]; then
	RESULT=`git rev-parse --short HEAD`
	if [ $? -eq 0 ]; then
		SHORTHASH=${RESULT}
	fi
fi
echo ${SHORTHASH} > default_commit_hash

echo "--- Finished commit hash file ---"

echo "--- Start autotools -------------"

aclocal \
&& autoheader \
&& automake --add-missing \
&& autoconf

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

#CXXFLAGS = -std=c++11 -g -fstack-protector -fno-omit-frame-pointer -fsanitize=address -ggdb -Wall -D_FILE_OFFSET_BITS=64
#CXXFLAGS = -g -fstack-protector -fstack-protector-all -Wall -D_FILE_OFFSET_BITS=64
#CXXFLAGS = -g -fsanitize=thread -fPIE -pie -Wall -D_FILE_OFFSET_BITS=64
#DEPS_LIBS = -ltsan -pthread -L/usr/local/lib -lfuse -lrt -ldl -lcurl -lxml2 -lcrypto
#DEPS_LIBS = -lasan -pthread -L/usr/local/lib -lfuse -lrt -ldl -lcurl -lxml2 -lcrypto
echo "--- Finished autotools ----------"

exit 0

