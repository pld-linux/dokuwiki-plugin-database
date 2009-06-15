%define		plugin		database
Summary:	Design your own database and manage the data within the wiki
Summary(pl.UTF-8):	Wtyczka database dla DokuWiki
Name:		dokuwiki-plugin-%{plugin}
Version:	1.0.4
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://www.langhamassociates.com/media/database.tgz
# Source0-md5:	14ae5bb2f6c40a525220a815611892ee
URL:		http://wiki.splitbrain.org/plugin:database
BuildRequires:	rpmbuild(macros) >= 1.520
BuildRequires:	sed >= 4.0
Requires:	dokuwiki >= 20061106
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir	/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_rpmhome}/dokuwiki-find-lang.sh %{buildroot}

%description
The database Plugin lets you create tables and columns and to populate
them with content.

The content can then be sorted and filtered by any of the columns.

There are a number of built-in lookups such as Gender, i.e. Male and
Female, Title, i.e. Mr., Ms, etc.

You can also use the contents of one table as a reference table, for
example a table of countries can be used so that the name of the
country is only held once in one table and other tables refer to it...

%prep
%setup -q -cn %{plugin}
%{__sed} -i -e 's,\r$,,' lib/plugins/%{plugin}/*.php

version=$(awk -Fv '$0 == " * v%{version}"{print $2}' lib/plugins/%{plugin}/action.php)
if [ "$version" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a lib/plugins/%{plugin}/* $RPM_BUILD_ROOT%{plugindir}
rm -f $RPM_BUILD_ROOT%{plugindir}/{CREDITS,changelog}
rm -f $RPM_BUILD_ROOT%{plugindir}/{COPYING,README,VERSION}

# find locales
%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{plugindir}
%{plugindir}/*.php
%{plugindir}/images
