resource "null_resource" "drift_check" {
  provisioner "local-exec" {
    command = "python3 scripts/check_drift.py ${var.inventory_file}"
  }
}

resource "null_resource" "auto_remediate" {
  count = var.auto_remediate ? 1 : 0

  provisioner "local-exec" {
    command = "python3 scripts/push_loopback.py ${var.inventory_file}"
  }

  depends_on = [null_resource.drift_check]
}
