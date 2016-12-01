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

if [[ -z $protected_containers ]]; then
        number_protected_containers=0
else
        number_protected_containers=$(echo "$protected_containers" | wc -l)
fi

# retrieve instand id
instance_id=$(wget -q -O - http://instance-data/latest/meta-data/instance-id)

# if unreclaimable slab is larger than 1GB
# or if uptime is over 12 hours
# and no protected containers exists
# terminate the instance

if ([ "$used_slab" -gt $SLAB_LIMIT ] || [ "$seconds_up" -gt $UPTIME_LIMIT ]) && [ "$number_protected_containers" -eq 0 ]; then
        aws ec2 terminate-instances --instance-ids $instance_id
fi
