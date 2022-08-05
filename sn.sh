#! /bin/bash
# This script is applicable to all desktop PCs and servers.

# Save the email message (STDIN) to a file:
cat > /tmp/smartd.msg

# Now email the message to the user at address ADD:
echo -e "Subject:$SMARTD_SUBJECT\n$(cat /tmp/smartd.msg)" | msmtp -v -t $SMARTD_ADDRESS
