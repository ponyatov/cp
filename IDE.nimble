# Package

version = "0.0.1"
author = "Dmitry Ponyatov <dponyatov@gmail.com>"
description = "native IDE written in Nim"
license = "MIT"
binDir = "bin"
srcDir = "src"
installExt = @["nim"]
bin = @["IDE"]

# Dependencies

requires "nim >= 1.4.4"
requires "ui >=0.9.4"
