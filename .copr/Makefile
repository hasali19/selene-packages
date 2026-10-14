.PHONY: srpm
srpm:
	dnf -y install rpmdevtools
	spectool -g -C $(outdir) $(spec)
	rpmbuild -bs $(spec) \
		--define "_sourcedir $(outdir)" \
		--define "_srcrpmdir $(outdir)"
