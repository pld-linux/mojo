%include	/usr/lib/rpm/macros.perl
Summary:	A Web-based mailing list manager
Summary(pl):	Menad¿er list mailowych operty o www
Name:		mojo
Version:	2.8.3
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://prdownloads.sourceforge.net/mojomail/%{name}-%(echo %{version} | sed -e 's#\.#_#g').tar.gz
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

%prep
%setup -q -n %{name}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d  $RPM_BUILD_ROOT{%{_mojodir}/{extensions,plugins},%{_mojovars},%{_sysconfdir}/httpd}

install %{name}.cgi $RPM_BUILD_ROOT%{_mojodir}
cp -R MOJO $RPM_BUILD_ROOT%{_mojodir}
install plugins/* $RPM_BUILD_ROOT%{_mojodir}/plugins
install extensions/* $RPM_BUILD_ROOT%{_mojodir}/extensions

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
%dir %{_mojodir}
%dir %{_mojodir}/extensions
%dir %{_mojodir}/MOJO
%dir %{_mojodir}/plugins
%attr(755,root,root) %{_mojodir}/*.cgi
%attr(755,root,root) %{_mojodir}/plugins/*.cgi
%attr(755,root,root) %{_mojodir}/extensions/*.pl
%attr(755,root,root) %{_mojodir}/MOJO/*
%attr(755,http,http) %dir %{_mojovars}
# KJM - don't include half of the perl....
%exclude %{_mojodir}/MOJO/perllib
