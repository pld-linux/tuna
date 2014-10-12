# TODO: python-ethtool
Summary:	Application tuning GUI and command line utility
Summary(pl.UTF-8):	Graficzny interfejs oraz narzędzie linii poleceń do dostrajania aplikacji
Name:		tuna
Version:	0.12
Release:	1
License:	GPL v2
Group:		Libraries/Python
Source0:	https://www.kernel.org/pub/software/utils/tuna/%{name}-%{version}.tar.xz
# Source0-md5:	a27ee9c3b8ea432fad9b69f0552dc3e8
URL:		https://rt.wiki.kernel.org/index.php/Tuna
BuildRequires:	gettext-devel
BuildRequires:	python-devel >= 2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
#Requires:	python-ethtool
Requires:	python-linux-procfs >= 0.4.5
Requires:	python-matplotlib
Requires:	python-pygobject
Requires:	python-pygtk-glade >= 2:2
Requires:	python-pygtk-gtk >= 2:2
Requires:	python-schedutils >= 0.2
Suggests:	python-inet_diag
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tune provides interface for changing scheduler and IRQ tunables, at
whole CPU and at per thread/IRQ level. Allows isolating CPUs for use
by a specific application and moving threads and interrupts to a CPU
by just dragging and dropping them. Operations can be done on CPU
sockets, understanding CPU topology.

Tuna can be also used as a command line utility.

%description -l pl.UTF-8
Tuna udostępnia interfejs do zmiany ustawień planisty oraz IRQ, na
poziomie całego procesora, jak i wątku/IRQ. Pozwala na izolowanie
procesorów do wykorzystania przez określone aplikacje oraz
przenoszenie wątków i przerwań na procesor poprzez przeciąganie ich.
Operacje mogą być wykonywane na gniazdach procesorów z uwzględnieniem
topologii.

Tuna może być używana także jako narzędzie linii poleceń.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/tuna,%{_bindir},%{_datadir}/tuna,%{_mandir}/man8,%{_datadir}/polkit-1/actions,%{_desktopdir}}

%{__python} setup.py install \
	--skip-build \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

cp -p tuna/tuna_gui.glade $RPM_BUILD_ROOT%{_datadir}/tuna
install tuna-cmd.py $RPM_BUILD_ROOT%{_bindir}/tuna
install oscilloscope-cmd.py $RPM_BUILD_ROOT%{_bindir}/oscilloscope
cp -pr help $RPM_BUILD_ROOT%{_datadir}/tuna/help
cp -p docs/tuna.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp -p etc/tuna/example.conf $RPM_BUILD_ROOT%{_sysconfdir}/tuna
cp -p etc/tuna.conf $RPM_BUILD_ROOT%{_sysconfdir}
cp -p org.tuna.policy $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions
cp -p tuna.desktop $RPM_BUILD_ROOT%{_desktopdir}

# l10n-ed message catalogues
for lng in `cat po/LINGUAS`; do
        po=po/"$lng.po"
        install -d $RPM_BUILD_ROOT%{_datadir}/locale/${lng}/LC_MESSAGES
        msgfmt $po -o $RPM_BUILD_ROOT%{_datadir}/locale/${lng}/LC_MESSAGES/%{name}.mo
done

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog docs/oscilloscope+tuna.html
%attr(755,root,root) %{_bindir}/oscilloscope
%attr(755,root,root) %{_bindir}/tuna
%{py_sitescriptdir}/tuna
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/tuna-%{version}-py*.egg-info
%endif
%{_datadir}/tuna
%dir %{_sysconfdir}/tuna
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tuna.conf
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/tuna/example.conf
%{_datadir}/polkit-1/actions/org.tuna.policy
%{_desktopdir}/tuna.desktop
%{_mandir}/man8/tuna.8*
