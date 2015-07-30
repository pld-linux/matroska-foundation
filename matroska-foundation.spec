Summary:	libEBML2 and libMatroska2 libraries
Summary(pl.UTF-8):	Biblioteki libEBML2 oraz libMatroska2
Name:		matroska-foundation
Version:	0
%define	snap	20150326
%define	gitref	29d8f2b2d0e939adfe6941af5f7f7f02344252fb
Release:	0.%{snap}.1
License:	BSD
Group:		Libraries
Source0:	https://github.com/Matroska-Org/foundation-source/archive/%{gitref}/foundation-source-%{gitref}.tar.gz
# Source0-md5:	00083d08cb517aa060c1ca0b8f839b8a
Patch0:		%{name}-shared.patch
Patch1:		%{name}-format.patch
URL:		https://github.com/Matroska-Org/
BuildRequires:	libstdc++-devel
%ifarch %{ix86} %{x8664} x32
BuildRequires:	yasm
%endif
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libEBML2 and libMatroska2 libraries.

%description -l pl.UTF-8
Biblioteki libEBML2 oraz libMatroska2.

%package devel
Summary:	Header files for Matroska 2 libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Matroska 2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Matroska 2 libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Matroska 2.

%prep
%setup -q -n foundation-source-%{gitref}
%patch0 -p1
%patch1 -p1

%{__sed} -i -e 's/^EBML_DLL /MATROSKA_DLL /' libmatroska2/matroska/matroska.h

# use system
%{__rm} -r corec/corec/helpers/zlib libmatroska2/bzip2

%{__sed} -i -e 's/\(-O3 \|-m32 \|-m64 \|-march=i486 \|-msse \|-mmx \|-Wl,--strip-all\)//g' corec/tools/coremake/gcc_linux.build

%build
%{__make} -C corec/tools/coremake \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	CPPFLAGS="%{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}"

corec/tools/coremake/coremake -v \
%ifarch %{ix86} x32
	gcc_linux \
%endif
%ifarch %{x8664}
	gcc_linux_x64 \
%endif
%ifarch %{arm}
	gcc_linux_arm \
%endif
%ifarch mips
	gcc_linux_mips \
%endif
%ifarch ppc
	gcc_linux_ppc
%endif

%{__make} -C spectool \
	V=1

cd spectool
../release/gcc_linux/data2lib2
%{__mv} matroska_sem.c ../libmatroska2
%{__mv} matroska_sem.h ../libmatroska2/matroska
cd ..

%{__make} -j1 \
	V=1 \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	STRIP=true

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

install release/gcc_linux*/mkclean $RPM_BUILD_ROOT%{_bindir}/mkvclean
install release/gcc_linux*/mkvalidator $RPM_BUILD_ROOT%{_bindir}
install release/gcc_linux*/mkvtree $RPM_BUILD_ROOT%{_bindir}
install release/gcc_linux*/libebml2.so $RPM_BUILD_ROOT%{_libdir}
install release/gcc_linux*/libmatroska2.so $RPM_BUILD_ROOT%{_libdir}

cp -a libebml2/ebml $RPM_BUILD_ROOT%{_includedir}
cp -a libmatroska2/matroska $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_includedir}/corec/{array,helpers/charconvert,helpers/date,helpers/file,helpers/parser,multithread,node,str}
cp -p config.h corec/corec/{corec,err,helper,memalloc,memheap,portab}.h $RPM_BUILD_ROOT%{_includedir}/corec
cp -p corec/tools/coremake/config_helper.h $RPM_BUILD_ROOT%{_includedir}/corec
cp -p corec/corec/array/array.h $RPM_BUILD_ROOT%{_includedir}/corec/array
cp -p corec/corec/helpers/charconvert/charconvert.h $RPM_BUILD_ROOT%{_includedir}/corec/helpers/charconvert
cp -p corec/corec/helpers/date/date.h $RPM_BUILD_ROOT%{_includedir}/corec/helpers/date
cp -p corec/corec/helpers/file/{file,streams}.h $RPM_BUILD_ROOT%{_includedir}/corec/helpers/file
cp -p corec/corec/helpers/parser/{buffer,dataheap,hotkey,nodelookup,parser,strtab,strtypes,urlpart}.h $RPM_BUILD_ROOT%{_includedir}/corec/helpers/parser
cp -p corec/corec/multithread/multithread.h $RPM_BUILD_ROOT%{_includedir}/corec/multithread
cp -p corec/corec/node/{node,nodebase,nodetools,nodetree}.h $RPM_BUILD_ROOT%{_includedir}/corec/node
cp -p corec/corec/str/str.h $RPM_BUILD_ROOT%{_includedir}/corec/str

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mkvclean
%attr(755,root,root) %{_bindir}/mkvalidator
%attr(755,root,root) %{_bindir}/mkvtree
%attr(755,root,root) %{_libdir}/libebml2.so
%attr(755,root,root) %{_libdir}/libmatroska2.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/corec
%{_includedir}/ebml
%{_includedir}/matroska
