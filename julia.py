
MAJOR_VERSION="0.6"
MINOR_VERSION="2"
REVISION="d386e40c17"
BUILD_DIR=os.path.join(os.getcwd(), "julia-${REVISION}".replace("${REVISION}", "d386e40c17"))

def install():
	os.system('wget https://julialang-s3.julialang.org/bin/linux/x64/${MAJOR}/julia-${MAJOR}.${MINOR}-linux-x86_64.tar.gz'.replace("${MAJOR}", MAJOR_VERSION).replace("${MINOR}", MINOR_VERSION))
	os.system('tar xvf julia-${MAJOR}.${MINOR}-linux-x86_64.tar.gz'.replace("${MAJOR}", MAJOR_VERSION).replace("${MINOR}", MINOR_VERSION))

def path():
	return os.path.join(BUILD_DIR, "bin")