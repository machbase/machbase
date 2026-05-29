#!/usr/bin/env bash

# Example environment file used with machclusterctl-sample-defaults.yaml
# Usage:
#   source ./machclusterctl-sample-defaults.env.sh
#   machclusterctl validate -f ./machclusterctl-sample-defaults.yaml
#
# Notes:
# - Write path values as absolute paths.
# - validate fails if home_path is not absolute after substitution.

export CLUSTER_NAME="prod-cluster"

# Source package archive path kept outside the coordinator home.
export MACHBASE_PACKAGE_PATH="/home/machbase/packages/machbase-ent-release-lightweight.tgz"
export MACHBASE_SSH_USER="machbase"
export MACHBASE_SSH_KEY="id_rsa_cluster"

export COORD_HOME_BASE="/home/machbase"
export DEPLOYER_HOME_BASE="/home/machbase"
export LOOKUP_HOME_BASE="/home/machbase"
export BROKER_HOME_BASE="/home/machbase"
export WAREHOUSE_HOME_BASE="/home/machbase"

export COORD_CLUSTER_PORT="5101"
export COORD_HTTP_ADMIN_PORT="5102"
export DEPLOYER_CLUSTER_PORT="5201"
export DEPLOYER_HTTP_ADMIN_PORT="5202"
export LOOKUP_CLUSTER_PORT="5301"
export LOOKUP_HTTP_ADMIN_PORT="5302"
export BROKER_SERVICE_PORT="5656"
export BROKER_HTTP_ADMIN_PORT="5657"
export WAREHOUSE_SERVICE_PORT="5500"
export WAREHOUSE_HTTP_ADMIN_PORT="5502"

# SERVER*_HOST is an IP or DNS name without the SSH user.
# YAML combines it as ${MACHBASE_SSH_USER}@${SERVER*_HOST}.
export SERVER1_HOST="192.168.0.83"
export SERVER2_HOST="192.168.0.84"
export SERVER3_HOST="192.168.0.85"
export SERVER4_HOST="192.168.0.86"

export COORD2_CLUSTER_PORT="5111"
export COORD2_HTTP_ADMIN_PORT="5112"

export DEPLOYER2_CLUSTER_PORT="5211"
export DEPLOYER2_HTTP_ADMIN_PORT="5212"

export LOOKUP_SLAVE_CLUSTER_PORT="5321"
export LOOKUP_SLAVE_HTTP_ADMIN_PORT="5322"

export BROKER1_CLUSTER_PORT="5401"
export BROKER2_CLUSTER_PORT="5411"
export BROKER2_HTTP_ADMIN_PORT="5412"

export WAREHOUSE_G1_HOME="/home/machbase/warehouse_g1"
export WAREHOUSE_G1_1_CLUSTER_PORT="5501"
export WAREHOUSE_G1_1_HTTP_ADMIN_PORT="5502"
export WAREHOUSE_G1_2_CLUSTER_PORT="5511"
export WAREHOUSE_G1_2_HTTP_ADMIN_PORT="5512"

export WAREHOUSE_G2_HOME="/home/machbase/warehouse_g2"
export WAREHOUSE_G2_SERVICE_PORT="5600"
export WAREHOUSE_G2_1_CLUSTER_PORT="5601"
export WAREHOUSE_G2_1_HTTP_ADMIN_PORT="5602"
export WAREHOUSE_G2_2_CLUSTER_PORT="5611"
export WAREHOUSE_G2_2_HTTP_ADMIN_PORT="5612"
