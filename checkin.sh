#!/bin/bash
# Save the current timestamp to your checkin file
date +%s > "$(jq -r .checkin_file config.json)"
echo "Checked in"
