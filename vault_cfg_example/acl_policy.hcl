path "terraform/creds/a-role-name" {
    capabilities = ["read"]
}

path "terraform/config" {
    capabilities = ["update"]
}

path "terraform/rotate-role/a-role-name" {
    capabilities = ["update"]
}