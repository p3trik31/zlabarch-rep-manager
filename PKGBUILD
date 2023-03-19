# Maintainer: Your Name <your_email_address>

pkgname="zlabarch-rep-manager"
pkgver="1.0"
pkgrel="1"
pkgdesc="Aplikace pro správu lokálních repozitářů"
arch=("x86_64")
#url="https://github.com/username/repo"
depends=('python' 'tk' 'python-keyrings-alt' 'python-pillow' 'python-argparse')
source=("zlabarch-rep-manager.py")
sha512sums=("SKIP")

package() {
	mkdir -p "${pkgdir}/usr/bin"
	cp "${srcdir}/zlabarch-rep-manager.py" "${pkgdir}/usr/bin/zlabarch-rep-manager"
	chmod +x "${pkgdir}/usr/bin/zlabarch-rep-manager"



}
