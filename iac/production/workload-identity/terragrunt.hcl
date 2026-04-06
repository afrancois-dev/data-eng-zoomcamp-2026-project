include "root" {
  path = find_in_parent_folders("root.hcl")
}

include "envcommon" {
  path = "${get_terragrunt_dir()}/../../_envcommon/workload-identity.hcl"
}

inputs = {}
