#!/bin/sh

shebang=$(head -n1 $1)
if [ "$shebang" != "#!/bin/sh" ]; then
    echo "Your script must have '#!/bin/sh' on the first line"
    exit 1
fi

if ! sh -n $1; then
    echo "You script has invalid syntax"
    exit 1
fi

echo "ok"
