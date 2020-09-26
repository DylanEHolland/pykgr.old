#!/bin/bash

. scripts/toolchain.config.sh;

m4_stage_one() {
    FILEURL="http://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.xz"
    NAME="m4-1.4.18";
    BLDDIR="/tmp/build-$NAME";
    SRCDIR="$source_packager_source_dir/$NAME"
    from_tz_file "$FILEURL" "$NAME";

    cd "$SRCDIR";
        sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c;
        echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h;
        ./configure \
            --prefix="$source_packager_environment" \
            --build=$(build-aux/config.guess) && \
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install;
            #make DESTDIR="$source_packager_environment" -j$source_packager_number_of_jobs install;
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

        ./configure --prefix="$source_packager_environment" \
            --build=$(./config.guess) \
            --mandir=/usr/share/man \
            --with-manpage-format=normal \
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
        ./configure --prefix="$source_packager_environment" \
            --build=$(support/config.guess) \
            --without-bash-malloc &&
        make -j$source_packager_number_of_jobs && \
            make -j$source_packager_number_of_jobs install;
        ln -sv bash "$source_packager_environment"/bin/sh;
    cd -;
}

coreutils_stage_one() {
    #FILEURL="http://ftp.gnu.org/gnu/coreutils/coreutils-8.32.tar.xz"
    BRANCH="master";
    REPO="https://github.com/coreutils/coreutils";
    NAME="coreutils";
    BLDDIR="/tmp/build-$NAME";
    SRCDIR="$source_packager_source_dir/$NAME"
    
    if ! [ -d "$SRCDIR" ]; then
        generate_git_clone "$REPO" "$SRCDIR" "$BRANCH";
    fi;

    cd "$SRCDIR";
        if ! [ -f ./configure ]; then 
            ./bootstrap;
        fi;
        # echo ./configure --prefix="$source_packager_environment" \
        #     --build=$(build-aux/config.guess) \
        #     --enable-install-program=hostname \
        #     --enable-no-install-program=kill,uptime
            # && \
            #make -j$source_packager_number_of_jobs;# && \
                #make -j$source_packager_number_of_jobs install;
    cd -;
}

# m4_stage_one;
# ncurses_stage_one;
# bash_stage_one
coreutils_stage_one