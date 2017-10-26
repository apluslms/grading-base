#!/bin/bash
if [ $# -ne 2 ]; then
  echo $0 charset_name file_path
  exit 0
fi
FROM=$(file -b --mime-encoding $2)
if [ "$FROM" != "binary" ] && [[ "$FROM" != ERROR:* ]]; then
  iconv -f $FROM -t $1 -c $2 > $2.iconvtmp
  mv $2.iconvtmp $2
fi
