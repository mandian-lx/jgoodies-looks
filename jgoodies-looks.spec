%define shortname looks

Summary:	Free high-fidelity Windows and multi-platform appearance
Name:		jgoodies-looks
Version:	2.2.1
Release:	%mkrel 0.0.4
Group:		Development/Java
License:	BSD
URL:		http://www.jgoodies.com/freeware/looks/
# Unfortunately, the filename has the version in an annoying way
Source0:	http://www.jgoodies.com/download/libraries/%{shortname}/%{shortname}-2_2_1.zip
# Source1: %{name}.README
Patch0:		%{name}-build.patch
BuildRequires:	jpackage-utils >= 0:1.6
BuildRequires:	java-rpmbuild >= 0:1.4
BuildRequires:	ant
Requires:	java >= 0:1.4
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The JGoodies look&feels make your Swing applications and applets look better.
They have been optimized for readability, precise micro-design and usability.

Main Benefits:

* Improved readability, legibility and in turn usability.
* Improved aesthetics - looks good on the majority of desktops
* Simplified multi-platform support
* Precise micro-design

%package javadoc
Summary:	Javadoc documentation for JGoodies Looks
Group:		Development/Java

%description javadoc
The JGoodies look&feels make your Swing applications and applets look better.
They have been optimized for readability, precise micro-design and usability.

This package contains the Javadoc documentation for JGoodies Looks.

%prep
%setup -q -n %{shortname}-%{version}
%patch0 -p1

# unzip the look&feel settings from bundled jar before we delete it
# (taken from Gentoo ebuild)
unzip -j %{shortname}-%{version}.jar META-INF/services/javax.swing.LookAndFeel \
|| die "unzip of javax.swing.LookAndFeel failed"
# and rename it to what build.xml expects
mv javax.swing.LookAndFeel all.txt

# Delete pre-generated stuff we don't want
rm %{shortname}-%{version}.jar
rm -r docs/api

%build
%ant -Ddescriptors.dir=. compile jar javadoc

%install
rm -rf %{buildroot}
install -dp %{buildroot}%{_javadir} \
        %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -p build/%{shortname}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
cp -pr build/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
# install -m 644 %SOURCE1 README_RPM.txt
# Fix the line endings!
for file in *.txt *.html docs/*.* docs/guide/*.*; do
    sed -i 's/\r//' $file
done
cd %{buildroot}%{_javadocdir}
ln -s %{name}-%{version} %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc RELEASE-NOTES.txt LICENSE.txt README.html docs/
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}
