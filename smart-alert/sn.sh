#! /bin/bash
# This script is applicable to all desktop PCs and servers.

# Save the email message (STDIN) to a file:
cat > /tmp/smartd.msg

# $SMARTD_ADDRESS is determined by the address argument ADD of the '-m' Directive
echo -e "Subject:$SMARTD_SUBJECT\n$(cat /tmp/smartd.msg)" | msmtp -v -t $SMARTD_ADDRESS
