#!/bin/bash

export source_packager_environment="$HOME/environment";
export source_packager_library="$source_packager_environment/lib";
export source_packager_library_64="$source_packager_environment/lib64";
export source_packager_include="$source_packager_environment/usr/include";
export source_packager_source_dir="/var/storage/environment-sources";
export source_packager_source_archives_dir="$source_packager_source_dir/tarballs";
export source_packager_target="$(uname -m)-src_pkgr-linux-gnu";
export source_packager_number_of_jobs="6";

export LC_ALL=POSIX;

generate_git_clone() {
    BRANCH="$3";
    REPO="$1"
    SRCDIR="$2";
    
    git clone "$REPO" "$SRCDIR" --depth 1 --branch "$BRANCH";
}

from_tz_file() {
    if ! [ -d "$source_packager_source_archives_dir" ]; then
        mkdir -pv "$source_packager_source_archives_dir";
    fi;

    TZ_URL="$1";
    TMP_FILENAME=$(basename $TZ_URL)

    if [ "$2" != "" ]; then
        DIRNAME="$2";
    fi;
    
    if ! [ -f "$source_packager_source_archives_dir"/"$TMP_FILENAME" ]; then
        cd "$source_packager_source_archives_dir"; wget --output-document "$TMP_FILENAME" -c "$TZ_URL"; cd -;
    fi;

    if ! [ -d "$source_packager_source_dir"/"$DIRNAME" ]; then
        tar xvf "$source_packager_source_archives_dir"/"$TMP_FILENAME" -C "$source_packager_source_dir";
    fi;
}
 
binutils_stage_one() {
    SRCDIR="$source_packager_environment/binutils";
    FILEURL="https://ftp.gnu.org/gnu/binutils/binutils-2.35.tar.gz";
    NAME="binutils-2.35";
    BLDDIR="/tmp/build-$NAME";
    SRCDIR="$source_packager_source_dir/$NAME"
    from_tz_file "$FILEURL" "$NAME";

    if [ -d "$BLDDIR" ]; then
        rm -rf "$BLDDIR";
    fi;

    mkdir "$BLDDIR" -pv;

    cd "$BLDDIR";
        "$SRCDIR"/configure \
            --prefix="$source_packager_environment" \
            --with-sysroot="/" \
            --with-lib-path="$source_packager_environment"/lib \
            --target="$source_packager_target" \
            --disable-nls \
            --disable-werror;
        make -j$source_packager_number_of_jobs && make -j$source_packager_number_of_jobs install;
        case $(uname -m) in
            x86_64) mkdir -pv "$source_packager_library" && ln -sv "$source_packager_library" "$source_packager_library_64";;
        esac
    cd -;
    rm -rf "$BLDDIR";
}

gcc_stage_one() {
    GLIBC_LIMITS_H="https://raw.githubusercontent.com/lattera/glibc/master/include/limits.h";
    FILEURL="http://ftp.gnu.org/gnu/gcc/gcc-10.2.0/gcc-10.2.0.tar.xz";
    NAME="gcc-10.2.0";
    BLDDIR="/tmp/build-$NAME";
    SRCDIR="$source_packager_source_dir/$NAME"
    from_tz_file "$FILEURL" "$NAME";

    if [ -d "$BLDDIR" ]; then
        rm -rf "$BLDDIR";
    fi;

    mkdir "$BLDDIR" -pv;

    # Get GCC Prereqs and fix lib path
    cd "$SRCDIR"; 
        sh contrib/download_prerequisites;
        case $(uname -m) in
            x86_64)
                sed -e '/m64=/s/lib64/lib/' \
                    -i.orig gcc/config/i386/t-linux64
            ;;
        esac
    cd -;

    # Configure and build a barely useable gcc
    cd "$BLDDIR";
        "$SRCDIR"/configure \
            --target="$source_packager_target" \
            --prefix="$source_packager_environment" \
            --with-glibc-version=2.11 \
            --with-sysroot="/" \
            --with-newlib \
            --without-headers \
            --enable-initfini-array \
            --disable-nls \
            --disable-shared \
            --disable-multilib \
            --disable-decimal-float \
            --disable-threads \
            --disable-libatomic \
            --disable-libgomp \
            --disable-libquadmath \
            --disable-libssp \
            --disable-libvtv \
            --disable-libstdcxx \
            --enable-languages=c,c++;
        make -j$source_packager_number_of_jobs; 
        make -j$source_packager_number_of_jobs install;
        cd `dirname $($source_packager_target-gcc -print-libgcc-file-name)`/install-tools/include && wget -c "$GLIBC_LIMITS_H";
        cd -;
    rm -rf "$BLDDIR";
}

get_kernel_headers() {
    LINUX_VERSION=$(uname -r | cut -c 1-3)
    FILEURL="https://github.com/torvalds/linux/archive/v$LINUX_VERSION.tar.gz"
    NAME="linux-$LINUX_VERSION";
    SRCDIR="$source_packager_source_dir/$NAME"

    if [ -d "$SRCDIR" ]; then
        rm -rfv "$SRCDIR";
    fi;

    from_tz_file "$FILEURL" "$NAME";

    mkdir "$source_packager_environment"/usr -pv;
    cd "$SRCDIR"; 
        make -j$source_packager_number_of_jobs mrproper && \
        make -j$source_packager_number_of_jobs headers;
        find usr/include -name '.*' -delete;
        rm usr/include/Makefile;
        cp -rfv usr/include/ "$source_packager_environment"/usr/include;
    cd -;
}

glibc_stage_one() {
    BRANCH="release/2.32/master";
    REPO="https://github.com/bminor/glibc";
    NAME="glibc";
    BLDDIR="/tmp/build-$NAME";
    SRCDIR="$source_packager_source_dir/$NAME";

    if ! [ -d "$SRCDIR" ]; then
        echo generate_git_clone "$REPO" "$SRCDIR" "$BRANCH";
    fi;

    if [ -d "$BLDDIR" ]; then
        rm -rf "$BLDDIR";
    fi;

    if ! [ -f "$source_packager_environment"/lib64/ld-lsb-x86-64.so.3 ]; then
        echo "Run lib updater";
        case $(uname -m) in
            i?86) ln -sfv ld-linux.so.2 "$source_packager_environment"/lib/ld-lsb.so.3
            ;;

            x86_64) ln -sfv ../lib/ld-linux-x86-64.so.2 "$source_packager_environment"/lib64
                    ln -sfv ../lib/ld-linux-x86-64.so.2 "$source_packager_environment"/lib64/ld-lsb-x86-64.so.3
            ;;
        esac
    fi;

    mkdir "$BLDDIR" -pv;
    cd "$BLDDIR";
        "$SRCDIR"/configure \
            --prefix=/usr \
            --host="$source_packager_target" \
            --build=$("$SRCDIR"/scripts/config.guess) \
            --enable-kernel=3.2 \
            --with-headers="$source_packager_include" \
            --without-selinux \
            libc_cv_slibdir=/lib;
        make -j$source_packager_number_of_jobs && \ 
            make DESTDIR="$source_packager_environment" -j$source_packager_number_of_jobs install;
    cd -;
    "$source_packager_environment"/libexec/gcc/"$source_packager_target"/10.2.0/install-tools/mkheaders
}

lib_cpp_stage_one() {
    GCC_NAME="gcc-10.2.0";
    NAME="libcpp";
    BLDDIR="/tmp/build-$NAME";
    FILEURL="http://ftp.gnu.org/gnu/gcc/gcc-10.2.0/gcc-10.2.0.tar.xz";
    SRCDIR="$source_packager_source_dir/$GCC_NAME"
    from_tz_file "$FILEURL" "$GCC_NAME";

    if [ -d "$BLDDIR" ]; then
        rm -rf "$BLDDIR";
    fi;

    mkdir "$BLDDIR" -pv;
    cd "$BLDDIR";
        "$SRCDIR"/libstdc++-v3/configure \
            --host="$source_packager_target" \
            --build=$("$SRCDIR"/config.guess) \
            --prefix=/usr \
            --disable-multilib \
            --disable-nls \
            --disable-libstdcxx-pch \
            --with-gxx-include-dir=/"$source_packager_target"/include/c++/10.2.0;
        make -j$source_packager_number_of_jobs && \ 
            make DESTDIR="$source_packager_environment" -j$source_packager_number_of_jobs install;
    cd -;
}

m4_stage_one() {
    FILEURL="http://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.xz"
    NAME="m4-1.4.18";
    BLDDIR="/tmp/build-$NAME";
    SRCDIR="$source_packager_source_dir/$NAME"
    from_tz_file "$FILEURL" "$NAME";

    cd "$SRCDIR";
        sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c;
        echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h;
        ./configure --prefix=/usr \
            --host="$source_packager_target" \
            --build=$(build-aux/config.guess);
        make -j$source_packager_number_of_jobs && \
            make DESTDIR="$source_packager_environment" -j$source_packager_number_of_jobs install;
    cd -;
}

ncurses_stage_one() {
    FILEURL="http://ftp.gnu.org/gnu/ncurses/ncurses-6.2.tar.gz";
    NAME="ncurses-6.2";
    BLDDIR="/tmp/build-$NAME";
    SRCDIR="$source_packager_source_dir/$NAME"
    from_tz_file "$FILEURL" "$NAME";

    cd "$SRCDIR";
        sed -i s/mawk// configure;
        
        if [ -d build ]; then
            rm -rf build;
        fi;

        mkdir -p build;
        
        # pushd build;
        
        ./configure;
        make -j$source_packager_number_of_jobs -C include;
        make -j$source_packager_number_of_jobs -C progs tic;
        
        #popd;

        ./configure --prefix=/usr \
            --host="$source_packager_target" \
            --build=$(./config.guess) \
            --mandir=/usr/share/man \
            --with-manpage-format=normal \
            --without-shared \
            --without-debug \
            --without-ada \
            --without-normal \
            --enable-widec;
        make -j$source_packager_number_of_jobs;
        # make DESTDIR="$source_packager_environment" TIC_PATH=$(pwd)/build/progs/tic install;
        # echo "INPUT(-lncursesw)" > "$source_packager_environment"/usr/lib/libncurses.so;
        # mv -v "$source_packager_environment"/usr/lib/libncursesw.so.6* "$source_packager_environment"/lib;
        # ln -sfv ../../lib/$(readlink $source_packager_environment/usr/lib/libncursesw.so) "$source_packager_environment"/usr/lib/libncursesw.so;
    cd -;
}

bash_stage_one() {
    FILEURL="http://ftp.gnu.org/gnu/bash/bash-5.0.tar.gz"
    NAME="bash-5.0";
    BLDDIR="/tmp/build-$NAME";
    SRCDIR="$source_packager_source_dir/$NAME"
    from_tz_file "$FILEURL" "$NAME";

    cd "$SRCDIR";
        ./configure --prefix=/usr \
            --build=$(support/config.guess) \
            --host="$source_packager_target" \
            --without-bash-malloc;
        make -j$source_packager_number_of_jobs && \
            make DESTDIR="$source_packager_environment" install
        mv -v "$source_packager_environment"/usr/bin/bash "$source_packager_environment"/bin/bash;
        ln -sv bash "$source_packager_environment"/bin/sh;
    cd -;
}

coreutils_stage_one() {
    FILEURL="http://ftp.gnu.org/gnu/coreutils/coreutils-8.32.tar.xz"
    NAME="coreutils-8.32";
    BLDDIR="/tmp/build-$NAME";
    SRCDIR="$source_packager_source_dir/$NAME"
    from_tz_file "$FILEURL" "$NAME";

    if [ -d "$BLDDIR" ]; then
        rm -rf "$BLDDIR";
    fi;

    mkdir "$BLDDIR" -pv;
    cd "$BLDDIR";
        ls "$SRCDIR";
    cd -;
}


#mkdir "$source_packager_environment" "$source_packager_include" -pv;
export PATH="$source_packager_environment/bin:/usr/bin:/bin";

# Stage one compiler
binutils_stage_one;
gcc_stage_one;
get_kernel_headers;
glibc_stage_one;
lib_cpp_stage_one;

# m4_stage_one;
# ncurses_stage_one;
# bash_stage_one