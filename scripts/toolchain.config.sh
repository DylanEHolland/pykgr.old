export source_packager_environment="/home/dylan/pykgr";

export source_packager_builder_environment="$source_packager_environment/builder";
export source_packager_library="$source_packager_builder_environment/lib";
export source_packager_library_64="$source_packager_builder_environment/lib64";
export source_packager_include="$source_packager_builder_environment/include";
export source_packager_source_dir="/var/storage/environment-sources";
export source_packager_source_archives_dir="$source_packager_source_dir/tarballs";
export source_packager_target="x86_64-pc-linux-gnu";#$(uname -m)-src_pkgr-linux-gnu";
export source_packager_number_of_jobs="10";

export LC_ALL=POSIX;
export PATH="$source_packager_builder_environment/bin:/usr/bin:/bin";

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