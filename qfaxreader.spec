%define name	qfaxreader
%define version 0.3.1
%define release %mkrel 5

Name: 	 	%{name}
Summary: 	Multipage TIFF/fax viewer
Version: 	%{version}
Epoch:		1
Release: 	%{release}

Source:		http://prdownloads.sourceforge.net/qfaxreader/%{name}-%{version}.tar.bz2
URL:		http://qfaxreader.sourceforge.net/
License:	GPL
Group:		Graphics
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	pkgconfig imagemagick qt3-devel tiff-devel gdbm-devel

%description
QFaxReader is a monochrome multipage .TIFF files visualisation utility
designed for viewing faxes.
    * Handle multi page fax files
    * Correctly display fax images in any quality (normal or fine)
    * Printing fax files
    * Image transformation (rotate left, rotate right, vertical flip)
    * Zoom fax images
    * Sidebar with easy navigation through directories
    * AutoRefresh + notification for new facsimiles
    * Aliases database for replacing faxes id's with real name
    * Export in all formats which your QT have support
    * Fullscreen mode

%prep
%setup -q
perl -pi -e 's/QTDIR\/lib/QTDIR\/%_lib/g' configure

%build
%configure2_5x --with-kdeico=%_iconsdir
make
										
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %buildroot/%_iconsdir/hicolor/16x16/apps/
mkdir -p %buildroot/%_iconsdir/hicolor/22x22/apps/
mkdir -p %buildroot/%_iconsdir/hicolor/32x32/apps/
%makeinstall_std DOCDIR=$(DESTDIR)/%_docdir
rm -fr $RPM_BUILD_ROOT/%_docdir

#menu

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=QFaxReader
Comment=Multipage TIFF viewer
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Graphics;Graphics;Viewer;
MimeType=image/tiff
EOF


#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 src/pixmaps/icon.xpm $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 src/pixmaps/icon.xpm $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 src/pixmaps/icon.xpm $RPM_BUILD_ROOT/%_miconsdir/%name.png

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%update_desktop_database
%endif
		
%if %mdkversion < 200900
%postun
%clean_menus
%clean_desktop_database
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README TODO
%{_bindir}/%name
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png


