Summary:        XML-SAX Perl module
Name:           perl-XML-SAX
Version:        0.96
Release:        7%{?dist}

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/XML-SAX/
Source0:        http://www.cpan.org/authors/id/G/GR/GRANTM/XML-SAX-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(XML::NamespaceSupport)
# The following creates circular dependency, comment out for bootstrap:
BuildRequires:  perl(XML::LibXML) perl(XML::LibXML::Common)

Requires:       perl(:MODULE_COMPAT_%(perl -MConfig -e 'print $Config{version}'))
Requires:       perl(XML::LibXML) perl(XML::LibXML::Common)

%{?filter_setup:
%filter_from_requires /perl(XML::SAX::PurePerl::\(DTDDecls\|DocType\|EncodingDetect\|XMLDecl\))/d
%filter_from_provides /perl(XML::SAX::PurePerl)/d
%?perl_default_filter
}


%description
XML::SAX consists of several framework classes for using and building
Perl SAX2 XML parsers, filters, and drivers. It is designed around the
need to be able to "plug in" different SAX parsers to an application
without requiring programmer intervention. Those of you familiar with
the DBI will be right at home. Some of the designs come from the Java
JAXP specification (SAX part), only without the javaness.


%prep
%setup -q -n XML-SAX-%{version}


%build
echo N | %{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

touch $RPM_BUILD_ROOT%{perl_vendorlib}/XML/SAX/ParserDetails.ini

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ ! -f "%{perl_vendorlib}/XML/SAX/ParserDetails.ini" ] ; then
  perl -MXML::SAX -e \
    'XML::SAX->add_parser(q(XML::SAX::PurePerl))->save_parsers()' 2>/dev/null || :
else
  cp -p "%{perl_vendorlib}/XML/SAX/ParserDetails.ini" "%{perl_vendorlib}/XML/SAX/ParserDetails.ini.backup"
fi

%triggerun -- perl-XML-LibXML < 1.58-8
if [ -f "%{perl_vendorlib}/XML/SAX/ParserDetails.ini.backup" ] ; then
  mv "%{perl_vendorlib}/XML/SAX/ParserDetails.ini.backup" "%{perl_vendorlib}/XML/SAX/ParserDetails.ini"
fi

%preun
# create backup of ParserDetails.ini, therefore user's configuration is used
if [ $1 -eq 0 ] ; then
  perl -MXML::SAX -e \
    'XML::SAX->remove_parser(q(XML::SAX::PurePerl))->save_parsers()' || :
fi
[ -f "%{perl_vendorlib}/XML/SAX/ParserDetails.ini.backup" ] && \
rm -rf "%{perl_vendorlib}/XML/SAX/ParserDetails.ini.backup" || :

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%dir %{perl_vendorlib}/XML
%{perl_vendorlib}/XML/SAX.pm
%dir %{perl_vendorlib}/XML/SAX
%{perl_vendorlib}/XML/SAX/*.pm
%{perl_vendorlib}/XML/SAX/*.pod
%{perl_vendorlib}/XML/SAX/PurePerl
%{_mandir}/man3/XML::*.3pm*
%ghost %{perl_vendorlib}/XML/SAX/ParserDetails.ini
%exclude %{perl_vendorlib}/XML/SAX/placeholder.pl


%changelog
* Fri Feb  5 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.96-7
- XML-LibXML use triggers for XML::SAX update. Deleting of settings in
 ParserDetails.ini is solved by post and preun part, which create backup.
- Resolves: rhbz#562173

* Thu Nov 12 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.96-6
- post scriptlet needs to check whether the file is installed. When it isn't,
 then it's needed call for adding PurePerl parser
 http://perl-xml.sourceforge.net/faq/#parserdetails.ini

* Mon Oct 19 2009 Stepan Kasal <skasal@redhat.com> - 0.96-5
- use the filtering macros

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 28 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.96-3
- 478905 fix scriptlets

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Marcela Mašláňová <mmaslano@redhat.com> - 0.96-1
- update to 0.96, big leap in versioning

* Sun Mar  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-5
- Re-enable XML::LibXML BuildRequires

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-4
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-3.1
- temporarily disable BR against perl-XML-LibXML

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-3
- rebuild for new perl

* Sat Jul 07 2007 Robin Norwood <rnorwood@redhat.com> - 0.16-2
- Resolves: rhbz#247213
- Fix provides and requires scripts.

* Mon Jul 02 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.16-1
- Update to 0.16.
- Brings specfile closer to Fedora Perl template.
- Corrects Source0 URL (upstream maintainer has changed).
- Move Requires filter into spec, and add Provides filter.

* Tue Feb 13 2007 Robin Norwood <rnorwood@redhat.com> - 0.15-1
- New version: 0.15

* Fri Jun 09 2006 Jason Vas Dias <jvdias@redhat.com> - 0.14-2
- fix bug 194706: fails to build under (new!) mock

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 0.14-1
- upgrade to 0.14

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.13-1.1
- rebuild for new perl-5.8.8

* Mon Dec 19 2005 Jason Vas Dias <jvdias@redhat.com> - 0.13-1
- upgrade to 0.13

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sun Apr 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0.12-7
- #121167
- Handle ParserDetails.ini parser registration.
- Require perl(:MODULE_COMPAT_*).
- Own installed directories.

* Wed Oct 22 2003 Chip Turner <cturner@redhat.com> - 0.12-1
- Specfile autogenerated.

