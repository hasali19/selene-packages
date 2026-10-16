sources_hook = $(dir $(spec))sources.sh

.PHONY: srpm
srpm:
	dnf -y install rpmdevtools
	spectool -g -C $(outdir) $(spec)
	find $(dir $(spec)) -maxdepth 1 -type f ! -name '*.spec' ! -name sources.sh -exec cp -p -t $(outdir) {} +
	if [ -f $(sources_hook) ]; then bash $(sources_hook) $(outdir) $(spec); fi
	rpmbuild -bs $(spec) \
		--define "_sourcedir $(outdir)" \
		--define "_srcrpmdir $(outdir)"
