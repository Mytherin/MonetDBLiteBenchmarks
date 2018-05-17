
import os

MAJOR_VERSION="0.6"
MINOR_VERSION="2"
REVISION="d386e40c17"
BUILD_DIR=os.path.join(os.getcwd(), "julia-${REVISION}".replace("${REVISION}", "d386e40c17"))

def install():
	if is_installed():
		return

	os.system('wget https://julialang-s3.julialang.org/bin/linux/x64/${MAJOR}/julia-${MAJOR}.${MINOR}-linux-x86_64.tar.gz'.replace("${MAJOR}", MAJOR_VERSION).replace("${MINOR}", MINOR_VERSION))
	os.system('tar xvf julia-${MAJOR}.${MINOR}-linux-x86_64.tar.gz'.replace("${MAJOR}", MAJOR_VERSION).replace("${MINOR}", MINOR_VERSION))

def is_installed():
	if os.path.exists(BUILD_DIR):
		return True
	return False

def path():
	return os.path.join(BUILD_DIR, "bin")