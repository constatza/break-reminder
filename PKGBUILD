# Maintainer: Your Name <youremail@example.com>
pkgname=break-reminder
pkgver=1.0.0
pkgrel=1
pkgdesc="Work hours break reminder daemon (user-level)"
arch=('any')
url="http://github.com/constatza/break-reminder.git"  # or your repository URL if available
license=('MIT')
depends=('python-notify2')
source=("break_reminder.py"
        "break_reminder.conf"
        "break-reminder.service")
md5sums=('SKIP' 'SKIP' 'SKIP')

package() {
  # Install the Python script to /usr/local/bin and mark it executable
  install -Dm755 "$srcdir/break_reminder.py" "$pkgdir/usr/local/bin/break_reminder.py"

  # Install the configuration file to /etc/xdg for system-wide defaults.
  # Users can override this by placing a config file in their $XDG_CONFIG_HOME.
  install -Dm644 "$srcdir/break_reminder.conf" "$pkgdir/etc/xdg/break-reminder.conf"

  # Install the systemd user service unit file to the proper directory.
  install -Dm644 "$srcdir/break-reminder.service" "$pkgdir/usr/lib/systemd/user/break-reminder.service"
}

