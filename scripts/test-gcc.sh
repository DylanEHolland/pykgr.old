cd /tmp;
    echo "int main(){}" > dummy.c;
    gcc dummy.c;
    readelf -l a.out | grep '/ld-linux';
    echo "===";
    ld --verbose | grep SEARCH_DIR | tr -s ' ;' \\012
cd -;