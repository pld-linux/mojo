# TODO: config file cannot be in /usr/share!
%include	/usr/lib/rpm/macros.perl
Summary:	A Web-based mailing list manager
Summary(pl):	Zarz±dca list mailowych operty o www
Name:		mojo
Version:	2.8.3
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/mojomail/%{name}-%(echo %{version} | sed -e 's#\.#_#g').tar.gz
Source1:	%{name}.conf
Patch0:		%{name}-config.patch
URL:		http://mojo.skazat.com/
BuildRequires:	perl
Requires(post,postun):	apache
Requires(post,postun):	grep
Requires(postun):	fileutils
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_mojodir	/usr/share/%{name}
%define		_mojovars	/var/lib/%{name}

%define		_noautoreq	'perl(to)'

%description
Mojo Mail is a light-weight Web-based email mailing list manager. It
supports announce-only lists and group discussion lists, as well as
archiving, double opt-in subscriptions, and double opt-out
unsubscriptions. List mailings can be sent using sendmail, qmail, or
even with a straight SMTP connection (either all at once, or in timed
batches). All list administration can be done through your browser via
Mojo Mail's administrative control panel. Creating new lists and
administrating them is easy. Mojo Mail is a great alternative to
programs such as Majordomo if you want to give more control to the
actual list owners, who may not have much experience with such
applications. Mojo Mail can be run simply as a CGI script and needs no
special modules installed. The entire look of html pages created by
Mojo Mail can be customized with any template you can provide, on a
list by list basis.

%description -l pl
Mojo Mail to lekki zarz±dca list e-mailowych oparty na WWW. Obs³uguje
listy wy³±cznie anonsowe oraz listy dyskusyjne, a tak¿e
archiwizowanie, podwójn± subskrypcjê oraz podwójne wypisywanie.
Wiadomo¶ci mog± byæ wysy³ane przy u¿yciu sendmaila, qmaila lub nawet
bezpo¶redniego po³±czenia SMTP (wszystkie naraz lub w paczkach co
jaki¶ czas). Ca³a administracja listami mo¿e byæ wykonywana z poziomu
przegl±darki poprzez administracyjny panel kontrolny Mojo Maila.
Tworzenie nowych list i administrowanie nimi jest ³atwe. Mojo Mail
jest dobr± alternatyw± dla programów typu Majordomo, je¶li chcemy daæ
wiêcej kontroli w³a¶ciwym w³a¶cicielom list, którzy mog± nie mieæ zbyt
du¿ego do¶wiadczenia z tego typu aplikacjami. Mojo Mail mo¿e byæ
uruchamiane po prostu jako skrypt CGI i nie wymaga zainstalowanych
¿adnych specjalnych modu³ów. Ca³y wygl±d stron HTML tworzonych przez
Mojo Maila mo¿e byæ zmieniony na poziomie list przez dostarczenie
dowolnego szablonu.

%prep
%setup -q -n %{name}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
# KJM - don't include half of the perl....
rm -rf MOJO/perllib
install -d  $RPM_BUILD_ROOT{%{_mojodir}/{extensions,plugins},%{_mojovars},%{_sysconfdir}/httpd}

install %{name}.cgi $RPM_BUILD_ROOT%{_mojodir}
cp -R MOJO $RPM_BUILD_ROOT%{_mojodir}
install plugins/* $RPM_BUILD_ROOT%{_mojodir}/plugins
install extensions/* $RPM_BUILD_ROOT%{_mojodir}/extensions
ln -s %{_mojodir}/MOJO/Config.pm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/%{name}_Config.pm

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	if [ -f /etc/httpd/httpd.conf ] && \
	    ! grep -q "^Include.*/%{name}.conf" /etc/httpd/httpd.conf; then
		echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%postun
if [ "$1" = "0" ]; then
	umask 027
	grep -E -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
		/etc/httpd/httpd.conf.tmp
	mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
	        /etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README.txt extras/{documentation/{html_version,pod_source},Flash,scripts,SQL,templates,testing}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/%{name}.conf
%{_sysconfdir}/httpd/%{name}_Config.pm
%dir %{_mojodir}
%dir %{_mojodir}/extensions
%dir %{_mojodir}/plugins
%dir %{_mojodir}/MOJO
%dir %{_mojodir}/MOJO/App
%dir %{_mojodir}/MOJO/Logging
%dir %{_mojodir}/MOJO/Mail
%dir %{_mojodir}/MOJO/MailingList
%dir %{_mojodir}/MOJO/Security
%dir %{_mojodir}/MOJO/Template
%attr(755,root,root) %{_mojodir}/*.cgi
%attr(755,root,root) %{_mojodir}/plugins/*.cgi
%attr(755,root,root) %{_mojodir}/extensions/*.pl
# FIXME: config file cannot be in /usr/share
%attr(750,http,http) %config(noreplace) %verify(not size mtime md5) %{_mojodir}/MOJO/Config.pm
%attr(755,root,root) %{_mojodir}/MOJO/MailingList.pm
%attr(755,root,root) %{_mojodir}/MOJO/*/*
%attr(755,http,http) %dir %{_mojovars}
