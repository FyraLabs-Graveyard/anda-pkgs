%define package_version 1.3-beta16
%define skia_version m102
%define skia_hash 861e4743af
# replace - with . in version number
%define package_version_stripped() (sed -e 's/-/./g' <<< "%{package_version}")

Name:           aseprite
Version:        1.3.beta16
Release:        1%{?dist}
Summary:        Summary here
URL:            https://www.aseprite.org/
Source0:        https://github.com/aseprite/aseprite/releases/download/v%{package_version}/Aseprite-v%{package_version}-Source.zip
Source1:        https://github.com/aseprite/skia/archive/refs/tags/%{skia_version}-%{skia_hash}.tar.gz
License:        https://github.com/aseprite/aseprite/blob/main/EULA.txt
BuildRequires:  gcc-c++ clang libcxx-devel cmake ninja-build libX11-devel libXcursor-devel libXi-devel mesa-libGL-devel fontconfig-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  libpng-devel
BuildRequires:  giflib-devel
BuildRequires:  libcurl-devel
BuildRequires:  zlib-devel
BuildRequires:  tinyxml-devel
BuildRequires:  pixman-devel
BuildRequires:  cmark-devel
BuildRequires:  libwebp-devel
BuildRequires:  fmt-devel
BuildRequires:  gn
Patch0:         shared-libwebp.patch
Patch1:         shared-fmt.patch
Patch2:         shared-libarchive.patch
Patch3:         skia.patch

%description
This is a very long description of aseprite.

%prep
%autosetup -c aseprite -p1
mkdir -p skia
tar -xf %{SOURCE1} --strip-components=1 -C skia

%build

echo Building Skia...

export _skiadir="$PWD/skia/obj"
env -C skia gn gen "$_skiadir" --args="`printf '%s ' \
is_debug=false is_official_build=true skia_build_fuzzers=false \
skia_enable_{pdf,skottie,skrive,sksl}=false \
skia_use_{libjpeg_turbo,libwebp}_{encode,decode}=false \
skia_use_{expat,xps,zlib,libgifcodec,sfntly}=false
ldflags += [\"-lpthread\"]`"
	ninja -C "$_skiadir" skia modules




%cmake \
    -DCMAKE_BUILD_TYPE=None \
    -DLAF_BACKEND=skia \
    -DENABLE_{UPDATER,WEBSOCKET}=OFF -DENABLE_SCRIPTING=ON -DLAF_WITH_EXAMPLES=OFF -DLAF_WITH_TESTS=OFF \
    -DSKIA_DIR=$PWD/skia \
    -DSKIA_LIBRARY_DIR="$_skiadir" -DSKIA_LIBRARY="$_skiadir/libskia.a" \
    -DUSE_SHARED_{CMARK,CURL,FMT,GIFLIB,JPEGLIB,ZLIB,LIBPNG,TINYXML,PIXMAN,FREETYPE,HARFBUZZ,LIBARCHIVE,WEBP}=YES \

%cmake_build

%install
%cmake_install

rm -rf %{buildroot}%{_prefix}/include/json11.hpp
rm -rf %{buildroot}%{_prefix}/include/tga.h
rm -rf %{buildroot}%{_prefix}/include/webp/
rm -rf %{buildroot}%{_prefix}/lib/libjson11.a
rm -rf %{buildroot}%{_prefix}/lib/libtga-lib.a
rm -rf %{buildroot}%{_prefix}/lib/libwebp*.a
rm -rf %{buildroot}%{_prefix}/lib/pkgconfig/json11.pc
rm -rf %{buildroot}%{_libdir}/libwebp*.a
rm -rf %{buildroot}%{_libdir}/pkgconfig/
rm -rf %{buildroot}%{_datadir}/WebP/

install -vDm 644 src/desktop/linux/aseprite.desktop "%{buildroot}/%{_datadir}/applications/%{name}.desktop"

%files
%{_bindir}/aseprite
%{_datadir}/aseprite/
%license EULA.txt
%{_datadir}/applications/%{name}.desktop

%changelog
* Mon Jun 13 2022 Cappy Ishihara <cappy@cappuchino.xyz> - 1.3-beta16-1.um36
- Initial release

