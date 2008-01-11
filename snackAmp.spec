%define name	snackAmp
%define version	3.1.2
%define release %mkrel 2

Summary:	Powerful, versatile music player
Name:		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Sound
URL: 		http://snackamp.sourceforge.net
Source: 	%{name}-%{version}.tar.bz2
Source1:	%{name}48.png
Source2:	%{name}32.png
Source3:	%{name}16.png
BuildRoot: 	%{_tmppath}/%{name}-buildroot
Requires:	tcl tk libsnack metakit-tcl

%description
SnackAmp is a multi-platform music player with normal music player abilities,
multi-user support, integrated web server, and a powerful auto-play list
feature. Currently mp3, wav, ogg vorbis,and many other sound files are
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
%setup -q -n %name.vfs
rm -fr `find -name CVS`

%install
rm -fr $RPM_BUILD_ROOT
rm -f lib/tablelist/*.txt
mkdir -p $RPM_BUILD_ROOT/%_libdir/%name
cp *.tcl $RPM_BUILD_ROOT/%_libdir/%name
cp -r lib $RPM_BUILD_ROOT/%_libdir/%name
mkdir -p $RPM_BUILD_ROOT/%_bindir
ln -s %_libdir/%name/%name.tcl $RPM_BUILD_ROOT/%_bindir/%name

sed -i 's|||' $RPM_BUILD_ROOT/%_libdir/%name/%name.tcl

chmod 644 $RPM_BUILD_ROOT/%_libdir/snackAmp/lib/bwidget/images/*
chmod 644 $RPM_BUILD_ROOT/%_libdir/snackAmp/lib/bwidget/lang/*
#chmod 644 $RPM_BUILD_ROOT/%_libdir/snackAmp/lib/bwidget/*.m4
chmod 644 $RPM_BUILD_ROOT/%_libdir/snackAmp/lib/bwidget/*.txt
#chmod 644 $RPM_BUILD_ROOT/%_libdir/snackAmp/lib/bwidget/*.in

chmod 644 $RPM_BUILD_ROOT/%_libdir/snackAmp/lib/*.tcl

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
cat %SOURCE1 > $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
cat %SOURCE2 > $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
cat %SOURCE3 > $RPM_BUILD_ROOT/%_miconsdir/%name.png

# Menu

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=SnackAmp
Comment=Music player
Exec=%{_bindir}/%{name} 
Icon=snackAmp
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Sound;AudioVideo;Audio;Player
EOF

%clean
rm -rf %buildroot/

%post
%{update_menus}

%postun
%{clean_menus}

%files
%defattr(-,root,root)
%_bindir/%name
%_libdir/%name
%{_datadir}/applications/mandriva-%{name}.desktop
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png
%defattr(644,root,root,755)
%doc readme.txt docs/*

