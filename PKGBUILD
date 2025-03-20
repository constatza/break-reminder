# Maintainer: Your Name <youremail@example.com>
pkgname=break-reminder
pkgver=1.0.0
pkgrel=1
pkgdesc="Work hours break reminder daemon (system-wide)"
arch=('any')
url="http://localrepo"  # or your repository URL if available
license=('MIT')
depends=('python-notify2')
source=("break_reminder.py"
        "break_reminder.conf"
        "break-reminder.service")
md5sums=('SKIP' 'SKIP' 'SKIP')

package() {
  # Install the Python script to /usr/local/bin and mark it executable
  install -Dm755 "$srcdir/break_reminder_work_async.py" "$pkgdir/usr/local/bin/break_reminder_work_async.py"

  # Install the configuration file to /etc
  install -Dm644 "$srcdir/break_reminder.conf" "$pkgdir/etc/break_reminder.conf"

  # Install the systemd service unit file to /etc/systemd/system
  install -Dm644 "$srcdir/break-reminder.service" "$pkgdir/etc/systemd/system/break-reminder.service"
}
