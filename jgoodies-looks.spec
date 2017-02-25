%{?_javapackages_macros:%_javapackages_macros}

%define oname JGoodies
%define shortoname Looks
%define releasedate 20141123

%define bname %(echo %oname | tr [:upper:] [:lower:])
%define shortname %(echo %shortoname | tr [:upper:] [:lower:])

%define version 2.7.0
%define oversion %(echo %version | tr \. _)

Summary:	High-Fidelity Windows and Multi-Platform Look&Feels
Name:		%{bname}-%{shortname}
Version:	%{version}
Release:	1
License:	BSD
Group:		Development/Java
URL:		http://www.jgoodies.com/freeware/libraries/%{shortname}/
Source0:	http://www.jgoodies.com/download/libraries/%{shortname}/%{name}-%{oversion}-%{releasedate}.zip
# NOTE: Latest version of jgoodies libraries can't be freely download from
#	from the official site. However official maven repo provides some
#	more updated versions
# Source0:	https://repo1.maven.org/maven2/com/%{bname}/%{name}/%{version}/%{name}-%{version}-sources.jar
BuildArch:	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(com.jgoodies:jgoodies-common)
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(org.sonatype.oss:oss-parent:pom:)

%description
The JGoodies Looks make your Swing applications and applets look better.
The package consists of a Windows look&feel and the Plastic look&feel
family. These have been optimized for readability, precise micro-design
and usability.

The Looks requires Java 6 or later and the JGoodies Common library.

%files -f .mfiles
%doc README.html
%doc RELEASE-NOTES.txt
%doc LICENSE.txt

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{oname} %{shortoname}
Requires:	jpackage-utils

%description javadoc
API documentation for %{oname} %{shortoname}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q
# Extract sources
mkdir -p src/main/java/
pushd src/main/java/
%jar -xf ../../../%{name}-%{version}-sources.jar
popd

# Extract tests
mkdir -p src/test/java/
pushd src/test/java/
%jar -xf ../../../%{name}-%{version}-tests.jar
popd

# Delete prebuild JARs and docs
find . -name "*.jar" -delete
find . -name "*.class" -delete
rm -fr docs

# Fix resources path
%pom_xpath_inject "pom:build" "
<resources>
	<resource>
		<directory>src/main/java/</directory>
		<includes>
			<include>com/jgoodies/looks/common/**.png</include>
			<include>com/jgoodies/looks/plastic/icons/**/*.gif</include>
			<include>com/jgoodies/looks/plastic/icons/**/*.png</include>
		</includes>
	</resource>
</resources>"


# Fix jar-not-indexed warning
%pom_add_plugin :maven-jar-plugin . "<configuration>
	<archive>
		<index>true</index>
	</archive>
</configuration>"

# Fix Jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build

%install
%mvn_install

