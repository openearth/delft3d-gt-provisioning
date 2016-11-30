#!/bin/bash

# retrieve Unreclaimable slab from meminfo
slab=$(grep -e SUnreclaim: /proc/meminfo)
[[ $slab =~ ([0-9]+) ]]
used_slab="${BASH_REMATCH[1]}"

# retrieve uptime
seconds_up=$(awk '{print $1}' /proc/uptime)
seconds_up=${seconds_up%.*}

# retrieve running containers and count number of protected containers
protected_containers=$(docker ps | awk '{print $NF}' | grep -e delft3d -e preprocess -e export -e postprocess)
number_protected_containers=$(echo "$protected_containers" | wc -l)

# if unreclaimable slab is larger than 1GB
# or if uptime is over a week
# and no protected containers exists
# reboot the instance

if ([ "$used_slab" -gt $SLAB_LIMIT ] || [ "$seconds_up" -gt $UPTIME_LIMIT ]) && [ "$number_protected_containers" -eq 0 ]; then
        echo "reboot"
fi
