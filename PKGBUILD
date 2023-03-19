# Maintainer: Your Name <your_email_address>

pkgname=zlabarch-rep-manager
pkgver=1.0
pkgrel=1
pkgdesc="A package manager for managing packages in zlabarch repositories."
arch=('any')
url="https://github.com/username/repo"
#depends=('python' 'tk' 'python-keyring' 'python-pillow' 'python-argparse')
#source=("$pkgname-$pkgver.tar.gz::https://github.com/username/repo/archive/refs/tags/v$pkgver.tar.gz")

package() {
  mkdir -p "$pkgdir/usr/bin/"
  mkdir -p "$pkgdir/usr/share/zlabarch-rep-manager/assets/"
  install -m 755 zlabarch-rep-manager.py "$pkgdir/usr/bin/"
  install -m 644 assets/* "$pkgdir/usr/share/zlabarch-rep-manager/assets/"
}
