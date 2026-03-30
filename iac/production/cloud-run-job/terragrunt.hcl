include "root" {
  path = find_in_parent_folders("root.hcl")
}

include "envcommon" {
  path   = "../../_envcommon/cloud-run-job.hcl"
  expose = true
}
