%define shortname looks
%define sun_jvm 0

Name: jgoodies-looks
Summary: Free high-fidelity Windows and multi-platform appearance
URL: http://www.jgoodies.com/freeware/looks/
Group: Development/Java
Version: 2.2.1
Release: 4
License: BSD

BuildRequires: jpackage-utils >= 0:1.6
BuildRequires: java-devel >= 0:1.4
BuildRequires: ant
Requires: java >= 0:1.4
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

# Unfortunately, the filename has the version in an annoying way
Source0: http://www.jgoodies.com/download/libraries/%{shortname}/%{shortname}-2_2_1.zip
# Let the build work without a bootclasspath
Patch0: %{name}-build.patch
# Remove some classes that depend on com.sun packages
Patch1: %{name}-no-com-sun.patch
# Remove some included JDK source
Patch2: %{name}-remove-jdk-stuff.patch
# Don't put a special manifest into the demo jar
Patch3: %{name}-demo-manifest.patch

%description
The JGoodies look&feels make your Swing applications and applets look better.
They have been optimized for readability, precise micro-design and usability.

Main Benefits:

* Improved readability, legibility and in turn usability.
* Improved aesthetics - looks good on the majority of desktops
* Simplified multi-platform support
* Precise micro-design

%package javadoc
Summary: Javadoc documentation for JGoodies Looks
Group: Development/Java
Requires: %{name} = %{version}-%{release}
%description javadoc
The JGoodies look&feels make your Swing applications and applets look better.
They have been optimized for readability, precise micro-design and usability.

This package contains the Javadoc documentation for JGoodies Looks.


%package demo
Summary: Demo applications for the JGoodies look&feels
Group: Development/Java
Requires: %{name} = %{version}-%{release}
%description demo
This package contains demo applications for the JGoodies look&feels,
including the "uif_lite" classes.

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

# Delete the whole Windows L&F because it depends on com.sun.java packages
# (Unless we're compiling with a Sun JVM)
%if %{sun_jvm}
%else
%patch1 -p1
rm -r src/core/com/jgoodies/looks/windows
%endif

# Delete a file that's a copy of something distributed by Sun, and patch the files that
# use it so they don't.
rm src/core/com/jgoodies/looks/common/ExtBasicArrowButtonHandler.java
%patch2 -p1

%patch3 -p1

%build
%ant -Ddescriptors.dir=. compile jar javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -dp $RPM_BUILD_ROOT%{_javadir} \
        $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -p build/%{shortname}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
cp -p build/demo.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-demo-%{version}.jar
ln -s %{name}-demo-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-demo.jar
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
# install -m 644 %SOURCE1 README_RPM.txt
# Fix the line endings!
for file in *.txt *.html docs/*.* docs/guide/*.*; do
    sed -i 's/\r//' $file
done
cd $RPM_BUILD_ROOT%{_javadocdir}
ln -s %{name}-%{version} %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%doc RELEASE-NOTES.txt LICENSE.txt README.html docs/

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%{_javadir}/%{name}-demo.jar
%{_javadir}/%{name}-demo-%{version}.jar

