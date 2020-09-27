#!/bin/bash
#
# TL;DR: How to tell when you should have written a function by now
#   But I wanna do that in python :\

. scripts/toolchain.config.sh;

m4_stage_one() {
    FILEURL="http://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.xz"
    NAME="m4-1.4.18";
    SRCDIR="$source_packager_source_dir/$NAME"

    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR;"
    fi;

    from_tz_file "$FILEURL" "$NAME";

    cd "$SRCDIR";
        sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c;
        echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h;
        ./configure \
            --prefix="$source_packager_builder_environment" \
            --build=$(build-aux/config.guess) && \
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install;
    cd -;
}

ncurses_stage_one() {
    FILEURL="http://ftp.gnu.org/gnu/ncurses/ncurses-6.2.tar.gz";
    NAME="ncurses-6.2";
    SRCDIR="$source_packager_source_dir/$NAME"

    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR";
    fi;

    from_tz_file "$FILEURL" "$NAME";

    cd "$SRCDIR";
        sed -i s/mawk// configure;
        
        if [ -d build ]; then
            rm -rf build;
        fi;

        mkdir -p build;
        
        pushd build;        
            ../configure;
            make -j$source_packager_number_of_jobs -C include;
            make -j$source_packager_number_of_jobs -C progs tic;
        popd;

        ./configure --prefix="$source_packager_builder_environment" \
            --build=$(./config.guess) \
            --with-shared \
            --without-debug \
            --without-ada \
            --without-normal \
            --enable-widec;
        make -j$source_packager_number_of_jobs;
        make TIC_PATH=$(pwd)/build/progs/tic install;
        echo "INPUT(-lncursesw)" > "$source_packager_library"/libncurses.so;
    cd -;
}

bash_stage_one() {
    FILEURL="http://ftp.gnu.org/gnu/bash/bash-5.0.tar.gz"
    NAME="bash-5.0";
    SRCDIR="$source_packager_source_dir/$NAME"
    from_tz_file "$FILEURL" "$NAME";

    cd "$SRCDIR";
        ./configure --prefix="$source_packager_builder_environment" \
            --build=$(support/config.guess) \
            --without-bash-malloc &&
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install;
        ln -sv bash "$source_packager_builder_environment"/bin/sh;
    cd -;
}

coreutils_stage_one() {
    BRANCH="master";
    REPO="https://github.com/coreutils/coreutils";
    NAME="coreutils";
    BLDDIR="/tmp/build-$NAME";
    SRCDIR="$source_packager_source_dir/$NAME"
    PATCH_FILE_URL="http://www.linuxfromscratch.org/patches/lfs/10.0/coreutils-8.32-i18n-1.patch";
    PATCH_FILE="coreutils-8.32-i18n-1.patch";
    
    if ! [ -d "$SRCDIR" ]; then
        generate_git_clone "$REPO" "$SRCDIR" "$BRANCH";
    fi;

    if ! [ -f /tmp/"$PATCH_FILE" ]; then
        cd /tmp && wget -c "$PATCH_FILE_URL"; cd -;
    fi;

    cd "$SRCDIR";
        if ! [ -f ./configure ]; then 
            ./bootstrap;
        fi;

        # Sort causes an issue with manpage generating :\
        ./configure --prefix="$source_packager_builder_environment" \
            --build=$(build-aux/config.guess) \
            --enable-install-program=hostname \
            --enable-no-install-program=kill,uptime,sort \
            --disable-werror && \
            make -j$source_packager_number_of_jobs && \
                make -j$source_packager_number_of_jobs install;
    cd -;
}

diffutils_stage_one() {
    FILE_URL="http://ftp.gnu.org/gnu/diffutils/diffutils-3.7.tar.xz";

    NAME="diffutils-3.7";
    SRCDIR="$source_packager_source_dir/$NAME"
    
    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR";
    fi;
    
    from_tz_file "$FILE_URL" "$NAME";

    cd "$SRCDIR";
        ./configure --prefix="$source_packager_builder_environment" && \
        make -j$source_packager_number_of_jobs && \
                make -j$source_packager_number_of_jobs install;
    cd -;
}

file_stage_one() {
    FILE_URL="ftp://ftp.astron.com/pub/file/file-5.39.tar.gz";

    NAME="file-5.39";
    SRCDIR="$source_packager_source_dir/$NAME"

    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR";
    fi;

    from_tz_file "$FILE_URL" "$NAME";

    cd "$SRCDIR";
        ./configure --prefix="$source_packager_builder_environment" && \
        make -j$source_packager_number_of_jobs && \
                make -j$source_packager_number_of_jobs install;
    cd -;
}

findutils_stage_one() {
    FILE_URL="http://ftp.gnu.org/gnu/findutils/findutils-4.7.0.tar.xz";

    NAME="findutils-4.7.0";
    SRCDIR="$source_packager_source_dir/$NAME"

    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR";
    fi;

    from_tz_file "$FILE_URL" "$NAME";

    cd "$SRCDIR";
        ./configure \
            --prefix="$source_packager_builder_environment" \
            --build=$(build-aux/config.guess) && \
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install;   
    cd -;
}

gawk_stage_one() {
    FILE_URL="http://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.xz";

    NAME="gawk-5.1.0";
    SRCDIR="$source_packager_source_dir/$NAME"

    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR";
    fi;

    from_tz_file "$FILE_URL" "$NAME";

    cd "$SRCDIR";
        sed -i 's/extras//' Makefile.in;
        ./configure \
            --prefix="$source_packager_builder_environment" \
            --build=$(./config.guess) && \
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install;         
    cd -;
}

grep_stage_one() {
    FILE_URL="http://ftp.gnu.org/gnu/grep/grep-3.4.tar.xz";

    NAME="grep-3.4";
    SRCDIR="$source_packager_source_dir/$NAME"

    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR";
    fi;

    from_tz_file "$FILE_URL" "$NAME";

    cd "$SRCDIR";
        ./configure \
            --prefix="$source_packager_builder_environment" \
            --bindir="$source_packager_builder_environment"/bin && \
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install; 
    cd -;
}

gzip_stage_one() {
    FILE_URL="http://ftp.gnu.org/gnu/gzip/gzip-1.10.tar.xz";

    NAME="gzip-1.10";
    SRCDIR="$source_packager_source_dir/$NAME"

    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR";
    fi;

    from_tz_file "$FILE_URL" "$NAME";

    cd "$SRCDIR";
        ./configure \
            --prefix="$source_packager_builder_environment" && \
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install; 
    cd -;
}

make_stage_one() {
    FILE_URL="http://ftp.gnu.org/gnu/make/make-4.3.tar.gz";

    NAME="make-4.3";
    SRCDIR="$source_packager_source_dir/$NAME"

    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR";
    fi;

    from_tz_file "$FILE_URL" "$NAME";

    cd "$SRCDIR";
        ./configure \
            --prefix="$source_packager_builder_environment" \
            --without-guile \
            --build=$(build-aux/config.guess) && \
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install; 
    cd -;
}

patch_stage_one() {
    FILE_URL="http://ftp.gnu.org/gnu/patch/patch-2.7.6.tar.xz";

    NAME="patch-2.7.6";
    SRCDIR="$source_packager_source_dir/$NAME"

    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR";
    fi;

    from_tz_file "$FILE_URL" "$NAME";

    cd "$SRCDIR";
        ./configure \
            --prefix="$source_packager_builder_environment" \
            --build=$(build-aux/config.guess) && \
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install; 
    cd -;
}

sed_stage_one() {
    FILE_URL="http://ftp.gnu.org/gnu/sed/sed-4.8.tar.xz";

    NAME="sed-4.8";
    SRCDIR="$source_packager_source_dir/$NAME"

    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR";
    fi;

    from_tz_file "$FILE_URL" "$NAME";

    cd "$SRCDIR";
        ./configure \
            --prefix="$source_packager_builder_environment" \
            --bindir="$source_packager_builder_environment"/bin && \
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install; 
    cd -;
}

tar_stage_one() {
    FILE_URL="http://ftp.gnu.org/gnu/tar/tar-1.32.tar.xz";

    NAME="tar-1.32";
    SRCDIR="$source_packager_source_dir/$NAME"

    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR";
    fi;

    from_tz_file "$FILE_URL" "$NAME";

    cd "$SRCDIR";
        ./configure \
            --prefix="$source_packager_builder_environment" \
            --build=$(build-aux/config.guess) \
            --bindir="$source_packager_builder_environment"/bin && \
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install; 
    cd -;
}

xz_stage_one() {
    FILE_URL="https://tukaani.org/xz/xz-5.2.5.tar.xz";

    NAME="xz-5.2.5";
    SRCDIR="$source_packager_source_dir/$NAME";

    if [ -d "$SRCDIR" ]; then
        rm -rf "$SRCDIR";
    fi;

    from_tz_file "$FILE_URL" "$NAME";

    cd "$SRCDIR";
        ./configure \
            --prefix="$source_packager_builder_environment" \
            --docdir="$source_packager_builder_environment"/share/doc/xz-5.2.5 && \
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install; 
    cd -;
}

base_shell() {
    m4_stage_one;
    ncurses_stage_one;
    bash_stage_one
    coreutils_stage_one;
}

dev_tools() {
    diffutils_stage_one;
    # file_stage_one; : wont build!
    findutils_stage_one;
    gawk_stage_one;
    grep_stage_one;
    gzip_stage_one;
    make_stage_one;
    patch_stage_one;
    sed_stage_one;
    tar_stage_one;
    # xz_stage_one; : compiling this kills tar :(
}

#base_shell;
dev_tools;