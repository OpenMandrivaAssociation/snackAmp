%define rel	2
%define beta	20070930
%if %beta
%define release		%mkrel 0.%{beta}.%{rel}
%else
%define release		%mkrel %{rel}
%endif

Summary:	Powerful, versatile music player
Name:		snackAmp
Version: 	3.1.3
Release: 	%{release}
License: 	GPLv2+
Group: 		Sound
URL: 		http://snackamp.sourceforge.net
Source0: 	http://snackamp.sourceforge.net/releases/%{name}-%{version}.tar.gz
Source1:	%{name}48.png
Source2:	%{name}32.png
Source3:	%{name}16.png
Patch0:		snackAmp-3.1.3-tcl8.6_time.patch
Requires:	tcl
Requires:	tk
Requires:	snack
Requires:	metakit-tcl
Requires:	tcl-tcllib
# for macros
BuildRequires:	tcl-devel
BuildRequires:	dos2unix
BuildArch:	noarch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SnackAmp is a multi-platform music player with normal music player abilities,
multi-user support, integrated web server, and a powerful auto-play list
feature. Currently mp3, wav, ogg vorbis, and many other sound files are
supported by SnackAmp. Both Tcl/Tk scripts and stand-alone executables (for
Windows and Linux) are available from sourceforge.

The motivation behind SnackAmp was to overcome the deficiency in other media
players to manage thousands (or tens of thousands) of mp3/ogg files in a both
powerful and easy to use manner without relying solely on ID3 tags to
categorize the music by genre or complete re-indexing of the media folders
when tags or file names are moved or modified. SnackAmp runs on a number of
platforms and has multi-user capabilities making it a natural fit for office
or educational environments. Being open source and written Tcl/Tk, the best
scripting language around, you can change it to suite your needs. SnackAmp
uses the wonderful Snack 2.1.6+ Sound toolkit written and maintained by Kåre
Sjölander. 

%prep
%setup -q -n %{name}.vfs
%patch0 -p0 -b .tcl86time
rm -fr `find -name CVS*`
find -name \*.tcl | xargs dos2unix -U

%install
rm -fr %{buildroot}
rm -f lib/tablelist/*.txt
mkdir -p %{buildroot}/%{tcl_sitelib}/%{name}
install -m 0644 *.tcl %{buildroot}/%{tcl_sitelib}/%{name}
cp -r lib %{buildroot}/%{tcl_sitelib}/%{name}
mkdir -p %{buildroot}/%{_bindir}
ln -s %{tcl_sitelib}/%{name}/%{name}.tcl %{buildroot}/%{_bindir}/%{name}

chmod 0755 %{buildroot}/%{tcl_sitelib}/%{name}/%{name}.tcl

chmod 644 %{buildroot}/%{tcl_sitelib}/%{name}/lib/bwidget/images/*
chmod 644 %{buildroot}/%{tcl_sitelib}/%{name}/lib/bwidget/lang/*
chmod 644 %{buildroot}/%{tcl_sitelib}/%{name}/lib/bwidget/*.txt
chmod 644 %{buildroot}/%{tcl_sitelib}/%{name}/lib/*.tcl

#icons
mkdir -p %{buildroot}/%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 0644 %{SOURCE1} %{buildroot}/%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m 0644 %{SOURCE2} %{buildroot}/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 0644 %{SOURCE3} %{buildroot}/%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# Menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=SnackAmp
Comment=Music player
Exec=soundwrapper %{_bindir}/%{name} 
Icon=snackAmp
Terminal=false
Type=Application
Categories=AudioVideo;Audio;Player
EOF

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{tcl_sitelib}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%defattr(644,root,root,755)
%doc readme.txt docs/*

