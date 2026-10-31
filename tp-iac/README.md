# tp-iac

## Préparation et vérification

- `terraform init` (ou `make init`)
- `terraform fmt -recursive` (ou `make fmt`)
- `terraform validate` (ou `make validate`)

## Plan & déploiement

- `terraform plan` (ou `make plan`)

- Par défaut : `terraform apply` (ou `make apply`)
- Environnement dev : `terraform apply -var-file="dev.tfvars"`

## Destruction

- `terraform destroy` (ou `make destroy`)

## CI

Configuration GitHub actions pour vérifier le formatage et la valider la syntaxe.
