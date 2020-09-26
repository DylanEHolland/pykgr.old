#!/bin/bash

. scripts/toolchain.config.sh;

binutils_stage_two() {
    SRCDIR="$source_packager_builder_environment/binutils";
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
            --prefix="$source_packager_builder_environment" \
            --build=$("$SRCDIR"/config.guess) \
            --enable-shared \
            --disable-werror \
            --enable-64-bit-bfd;
        make -j$source_packager_number_of_jobs && \
        make -j$source_packager_number_of_jobs install;
    cd -;
    rm -rf "$BLDDIR";
}

gcc_stage_two() {
    GLIBC_LIMITS_H="https://raw.githubusercontent.com/lattera/glibc/master/include/limits.h";
    FILEURL="http://ftp.gnu.org/gnu/gcc/gcc-10.2.0/gcc-10.2.0.tar.xz";
    NAME="gcc-10.2.0";
    BLDDIR="/tmp/build-$NAME";
    SRCDIR="$source_packager_source_dir/$NAME"

    # if [ -d "$SRCDIR" ]; then
    #     rm -rf "$SRCDIR";
    # fi;

    # if [ -d "$BLDDIR" ]; then
    #     rm -rf "$BLDDIR";
    # fi;

    # from_tz_file "$FILEURL" "$NAME";
    # mkdir "$BLDDIR" -pv;

    cd "$SRCDIR";
        #sh contrib/download_prerequisites;
        #sed -e '/m64=/s/lib64/lib/' -i.orig gcc/config/i386/t-linux64;
        #mkdir -pv "$source_packager_target"/libgcc
        #ln -s "$SRCDIR"/libgcc/gthr-posix.h "$source_packager_target"/libgcc/gthr-default.h;
    cd -;

    # Configure and build a barely useable gcc
    cd "$BLDDIR";
    echo "$source_packager_builder_environment";
        # "$SRCDIR"/configure \
        #     --build=$("$SRCDIR"/config.guess) \
        #     --enable-initfini-array \
        #     --disable-bootstrap \
        #     --disable-nls \
        #     --disable-multilib \
        #     --disable-decimal-float \
        #     --disable-libatomic \
        #     --disable-libgomp \
        #     --disable-libquadmath \
        #     --disable-libssp \
        #     --disable-libvtv \
        #     --disable-libstdcxx \
        #     --enable-languages=c,c++;
        # make -j$source_packager_number_of_jobs; 
        # make -j$source_packager_number_of_jobs install;
        # ln -sv gcc "$source_packager_builder_environment"/bin/cc;
        cd -;
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

    cd "$SRCDIR"; 
        make -j$source_packager_number_of_jobs mrproper && \
        make -j$source_packager_number_of_jobs headers;
        find usr/include -name '.*' -delete;
        rm usr/include/Makefile;
        cp -rfv usr/include/* "$source_packager_include"/;
    cd -;
    rm -rf "$BLDDIR";
}

glibc_stage_two() {
    BRANCH="release/2.32/master";
    REPO="https://github.com/bminor/glibc";
    NAME="glibc";
    BLDDIR="/tmp/build-$NAME";
    SRCDIR="$source_packager_source_dir/$NAME";

    if ! [ -d "$SRCDIR" ]; then
        generate_git_clone "$REPO" "$SRCDIR" "$BRANCH";
    fi;

    if [ -d "$BLDDIR" ]; then
        rm -rf "$BLDDIR";
    fi;

    if ! [ -f "$source_packager_library"/ld-lsb.so.3 ]; then
        ln -sv /lib/ld-linux.so.2 "$source_packager_library"/ld-lsb.so.3;
        ln -sfv /usr/lib64/ld-linux-x86-64.so.2 "$source_packager_library_64";
        ln -sfv "$source_packager_library_64"/ld-linux-x86-64.so.2 "$source_packager_library_64"/ld-lsb-x86-64.so.3;
    fi;

    cd "$SRCDIR";
        mkdir "$BLDDIR" -pv;
        pushd "$BLDDIR";
            "$SRCDIR"/configure \
                --prefix="$source_packager_builder_environment" \
                --build=$("$SRCDIR"/scripts/config.guess) \
                --enable-kernel=3.2 \
                --with-headers="$source_packager_include" \
                --without-selinux \
                libc_cv_slibdir="$source_packager_library";
            make -j$source_packager_number_of_jobs && \ 
                make -j$source_packager_number_of_jobs install;
        popd;
    cd -;
    "$source_packager_builder_environment"/libexec/gcc/"$source_packager_target"/10.2.0/install-tools/mkheaders
}

lib_cpp_stage_two() {
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
            --build=$("$SRCDIR"/config.guess) \
            --prefix="$source_packager_builder_environment" \
            --disable-multilib \
            --disable-nls \
            --with-gxx-include-dir="$source_packager_include"/c++/10.2.0;
        make -j$source_packager_number_of_jobs && \ 
            make -j$source_packager_number_of_jobs install;
    cd -;
}

# Build intermediate compiler

binutils_stage_two;
# gcc_stage_two;
# get_kernel_headers;
# glibc_stage_two;
# lib_cpp_stage_two;