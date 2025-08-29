#!/usr/bin/env bash

set -euxo pipefail

mkdir ~/src

(cd ~/src && tar xf ~/code.tgz)

(cd ~/src && ./ya test -T -DCI=github -DCONSISTENT_BUILD=yes -DCONSISTENT_DEBUG=yes ./perforator)

