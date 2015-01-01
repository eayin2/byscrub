byscrub
=======
byscrub is a script for the `btrfs scrub` command. The script parses /proc/mounts for btrfs and will then
scrub all btrfs that it finds automatically and log errors to /var/log/byscrub.log and sends an email if an
error was found.
I recommend to run it e.g. weekly with anacron or systemd.timer.
