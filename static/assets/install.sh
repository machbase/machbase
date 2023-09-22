UNAMES=`uname -s`
UNAMEP=`uname -m`

VERSION="$1"

if [ -z "$VERSION" ]; then
    VERSION=`curl -fsSL https://api.github.com/repos/machbase/neo-server/releases/latest |grep tag_name | awk '{print $2}' | tr -d '",'`
fi

if [ -z "$VERSION" ]; then
    echo "no version is specified"
    exit 1
fi

case $UNAMES in
    Linux)
        UNAMES="linux"
    ;;
    Darwin)
        UNAMES="darwin"
    ;;
    Windows)
        UNAMES="windows"
    ;;
    *)
        echo "Unsupported OS $UNAMES"
        exit 1
    ;;
esac

case $UNAMEP in
    aarch64)
        UNAMEP="arm64"
    ;;
    arm64)
        UNAMEP="arm64"
    ;;
    armv6l)
        UNAMEP="arm32"
    ;;
    armv7l)
        UNAMEP="arm32"
    ;;
    x86_64)
        UNAMEP="amd64"
    ;;
    *)
        echo "Unsupported ARCH $UNAMEP"
        exit 1
    ;;
esac

# echo $UNAMES $UNAMEP $VERSION

FNAME="machbase-neo-$VERSION-$UNAMES-$UNAMEP.zip"

echo "Downloading... $FNAME"

curl -L -o $FNAME \
    "https://github.com/machbase/neo-server/releases/download/${VERSION}/${FNAME}" \
    && echo "\n\nDownload complete $FNAME"

