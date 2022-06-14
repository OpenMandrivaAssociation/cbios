%define         machines %{_datadir}/openmsx/machines

Name:           cbios
Version:        0.29a
Release:        1
Summary:        A third party BIOS compatible with the MSX BIOS
License:        BSD
Group:		Emulators
URL:            http://cbios.sourceforge.net/
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.zip
BuildArch:      noarch
BuildRequires:  pasmo

%description
C-BIOS is a BIOS compatible with the MSX BIOS written from scratch by BouKiCHi.
It is available for free, including its source code and can be shipped with MSX
emulators so they are usable out-of-the-box without copyright issues.

# Build c-bios support for different msx emulators as sub packages, cbios has
# support for blueMSX, NLMSX, openMSX, RuMSX but at the moment we only support
# openmsx (others not available for Linux yet).
%package openmsx
Summary:	C-BIOS support for openMSX
Requires:	cbios = %{version}-%{release}

%description openmsx
Adds C-BIOS support for openMSX, a third party MSX compatible BIOS.

%prep
%setup -q

sed -i 's/\r//' doc/*.txt

# Character encoding fixes
iconv -f iso8859-1 doc/cbios.txt -t utf8 > doc/cbios.conv \
    && /bin/mv -f doc/cbios.conv doc/cbios.txt

%build
%make_build

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{machines}
install -pm 0644 derived/bin/* %{buildroot}%{_datadir}/%{name}

# Install openmsx configuration and symlinks to cbios
cp -a configs/openMSX/C-BIOS_MSX* %{buildroot}%{machines}
for i in %{buildroot}%{_datadir}/%{name}/*.rom; do
    ln -s --target-directory=%{buildroot}%{machines} \
        ../../%{name}/$(basename $i)
done

%files
%{_datadir}/%{name}/
%doc doc/cbios.txt doc/chkram.txt

# We don't own the parent directories here, because they are owned by openmsx,
# also we don't set hardwareconfig.xml as %%config because they are not
# intended to be changed by the end user.
%files openmsx
%{machines}/*
%doc configs/openMSX/README.txt
